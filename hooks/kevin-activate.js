#!/usr/bin/env node
const {
  clearDisabled,
  isDisabled,
  readInput,
  voice,
  voiceReminder,
  writeContext,
} = require('./kevin-runtime');

readInput((input) => {
  const source = input.source || 'startup';

  if (source === 'startup' || source === 'clear') {
    clearDisabled(input.session_id);
  } else if (isDisabled(input.session_id)) {
    return;
  }

  writeContext('SessionStart', source === 'compact' ? voiceReminder() : voice());
});
