const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');
const { spawn, spawnSync } = require('node:child_process');

const root = path.join(__dirname, '..');
const hooksDir = path.join(root, 'hooks');

function run(script, pluginData, input = {}) {
  return spawnSync(process.execPath, [path.join(hooksDir, script)], {
    env: {
      ...process.env,
      PLUGIN_DATA: pluginData,
      CLAUDE_PLUGIN_DATA: pluginData,
    },
    input: JSON.stringify(input),
    encoding: 'utf8',
  });
}

function output(result) {
  assert.equal(result.status, 0, result.stderr);
  return result.stdout ? JSON.parse(result.stdout) : null;
}

function context(result) {
  return output(result)?.hookSpecificOutput?.additionalContext;
}

test('hook config covers parent threads, prompts, and subagents', () => {
  const config = JSON.parse(fs.readFileSync(path.join(hooksDir, 'hooks.json'), 'utf8'));
  const claudeManifest = JSON.parse(fs.readFileSync(
    path.join(root, '.claude-plugin', 'plugin.json'),
    'utf8',
  ));
  assert.equal(claudeManifest.hooks, './hooks/hooks.json');

  assert.deepEqual(Object.keys(config.hooks).sort(), [
    'SessionStart',
    'SubagentStart',
    'UserPromptSubmit',
  ]);
  assert.equal(config.hooks.SessionStart[0].matcher, 'startup|resume|clear');
  assert.equal(config.hooks.SessionStart[1].matcher, 'compact');
  assert.equal(config.hooks.SessionStart[0].hooks[0].statusMessage, 'Loading Kevin...');
  assert.equal(config.hooks.SessionStart[1].hooks[0].statusMessage, undefined);
  assert.equal(config.hooks.SubagentStart[0].hooks[0].statusMessage, undefined);
  assert.equal(config.hooks.UserPromptSubmit[0].hooks[0].statusMessage, undefined);

  for (const groups of Object.values(config.hooks)) {
    for (const hook of groups.flatMap((group) => group.hooks)) {
      assert.match(hook.command, /^node /);
      assert.doesNotMatch(hook.command, /\bsh\s+-c\b|\bcommand\s+-v\b|&&|\|\|/);
      assert.match(hook.commandWindows, /\$env:CLAUDE_PLUGIN_ROOT/);

      const script = hook.command.match(/hooks\/([\w.-]+\.js)/)?.[1];
      assert.ok(script, `missing hook script in ${hook.command}`);
      assert.ok(fs.existsSync(path.join(hooksDir, script)), `${script} does not exist`);
    }
  }
});

test('SessionStart injects the full voice rules', () => {
  const data = fs.mkdtempSync(path.join(os.tmpdir(), 'kevin-hooks-'));
  const result = run('kevin-activate.js', data, {
    session_id: 'session-one',
    source: 'startup',
  });

  assert.match(context(result), /KEVIN MODE ACTIVE/);
  assert.match(context(result), /Drop the voice for/);
});

test('compaction gets a short reminder without the activation banner', () => {
  const data = fs.mkdtempSync(path.join(os.tmpdir(), 'kevin-hooks-'));
  const result = run('kevin-activate.js', data, {
    session_id: 'session-compact',
    source: 'compact',
  });
  const reminder = context(result);

  assert.match(reminder, /Use Kevin voice for prose/);
  assert.doesNotMatch(reminder, /KEVIN MODE ACTIVE/);
  assert.ok(reminder.length < 300);
});

test('off and on commands are session-scoped', () => {
  const data = fs.mkdtempSync(path.join(os.tmpdir(), 'kevin-hooks-'));
  const session = { session_id: 'session-two' };

  let result = run('kevin-prompt.js', data, { ...session, prompt: 'normal mode' });
  assert.match(context(result), /KEVIN MODE OFF/);

  result = run('kevin-subagent.js', data, { ...session, agent_type: 'general' });
  assert.equal(output(result), null);

  result = run('kevin-subagent.js', data, {
    session_id: 'another-session',
    agent_type: 'general',
  });
  assert.match(context(result), /Use Kevin voice for prose/);
  assert.doesNotMatch(context(result), /KEVIN MODE ACTIVE/);

  result = run('kevin-activate.js', data, { ...session, source: 'compact' });
  assert.equal(output(result), null);

  result = run('kevin-prompt.js', data, { ...session, prompt: 'talk like kevin' });
  assert.match(context(result), /KEVIN MODE ACTIVE/);

  result = run('kevin-subagent.js', data, { ...session, agent_type: 'general' });
  assert.match(context(result), /Use Kevin voice for prose/);
  assert.doesNotMatch(context(result), /KEVIN MODE ACTIVE/);
});

test('incidental mentions do not switch modes', () => {
  const data = fs.mkdtempSync(path.join(os.tmpdir(), 'kevin-hooks-'));
  const result = run('kevin-prompt.js', data, {
    session_id: 'session-three',
    prompt: 'Add a normal mode toggle to this screen',
  });

  assert.equal(output(result), null);
  assert.match(context(run('kevin-subagent.js', data, {
    session_id: 'session-three',
    agent_type: 'general',
  })), /Use Kevin voice for prose/);
});

test('a new startup resets a disabled session', () => {
  const data = fs.mkdtempSync(path.join(os.tmpdir(), 'kevin-hooks-'));
  const session = { session_id: 'session-four' };

  output(run('kevin-prompt.js', data, { ...session, prompt: 'stop kevin' }));
  const result = run('kevin-activate.js', data, { ...session, source: 'startup' });
  assert.match(context(result), /KEVIN MODE ACTIVE/);
});

test('stdin-reading hooks do not hang when stdin stays open', async () => {
  const data = fs.mkdtempSync(path.join(os.tmpdir(), 'kevin-hooks-'));
  const child = spawn(process.execPath, [path.join(hooksDir, 'kevin-prompt.js')], {
    env: { ...process.env, PLUGIN_DATA: data },
    stdio: ['pipe', 'ignore', 'ignore'],
  });

  const code = await new Promise((resolve, reject) => {
    const guard = setTimeout(() => {
      child.kill('SIGKILL');
      reject(new Error('hook hung on open stdin'));
    }, 3000);
    child.on('exit', (value) => {
      clearTimeout(guard);
      resolve(value);
    });
    child.on('error', reject);
  });

  assert.equal(code, 0);
});
