#!/usr/bin/env node
const { isDisabled, readInput, voice, writeContext } = require('./kevin-runtime');

readInput((input) => {
  if (!isDisabled(input.session_id)) {
    writeContext('SubagentStart', voice());
  }
});
