#!/usr/bin/env node
// kevin — Claude Code SessionStart hook.
// Prints the Kevin voice rules to stdout; Claude Code injects stdout as
// hidden session context, so the persona loads every session.
// kevin-voice.md is the single source of truth, shared with the benchmark.

const fs = require('fs');
const path = require('path');

const voicePath = path.join(__dirname, '..', 'kevin-voice.md');

try {
  process.stdout.write(fs.readFileSync(voicePath, 'utf8'));
} catch (e) {
  process.stdout.write('KEVIN MODE ACTIVE — voice file missing at ' + voicePath);
}
