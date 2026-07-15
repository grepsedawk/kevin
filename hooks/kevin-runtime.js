const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');

const voicePath = path.join(__dirname, '..', 'kevin-voice.md');

function dataDir() {
  if (process.env.PLUGIN_DATA) return process.env.PLUGIN_DATA;
  if (process.env.CLAUDE_PLUGIN_DATA) return process.env.CLAUDE_PLUGIN_DATA;
  if (process.env.CLAUDE_CONFIG_DIR) return path.join(process.env.CLAUDE_CONFIG_DIR, 'kevin');
  return path.join(os.homedir(), '.claude', 'kevin');
}

function statePath(sessionId) {
  const id = crypto.createHash('sha256').update(String(sessionId || 'unknown')).digest('hex');
  return path.join(dataDir(), 'sessions', `${id}.off`);
}

function setDisabled(sessionId) {
  try {
    const file = statePath(sessionId);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, 'off', { mode: 0o600 });
  } catch {}
}

function clearDisabled(sessionId) {
  try {
    fs.unlinkSync(statePath(sessionId));
  } catch {}
}

function isDisabled(sessionId) {
  try {
    return fs.readFileSync(statePath(sessionId), 'utf8').trim() === 'off';
  } catch {
    return false;
  }
}

function voice() {
  try {
    return fs.readFileSync(voicePath, 'utf8');
  } catch {
    return 'KEVIN MODE ACTIVE. Use the fewest words that still carry the meaning.';
  }
}

function voiceReminder() {
  return 'Use Kevin voice for prose: fewest clear words, no filler, hedging, pleasantries, or narration. Keep code, commands, commit and PR text, security warnings, and irreversible-action instructions in full plain language.';
}

function writeContext(event, context) {
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: event,
      additionalContext: context,
    },
  }));
}

function readInput(callback) {
  let input = '';
  let finished = false;

  function finish() {
    if (finished) return;
    finished = true;

    try {
      callback(JSON.parse(input.replace(/^\uFEFF/, '')));
    } catch {
      callback({});
    }
  }

  process.stdin.on('data', (chunk) => { input += chunk; });
  process.stdin.on('end', finish);
  process.stdin.on('error', () => {
    finish();
    process.exit(0);
  });
  setTimeout(() => {
    finish();
    process.exit(0);
  }, 1000).unref();
}

module.exports = {
  clearDisabled,
  isDisabled,
  readInput,
  setDisabled,
  voice,
  voiceReminder,
  writeContext,
};
