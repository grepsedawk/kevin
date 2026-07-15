#!/usr/bin/env node
const {
  clearDisabled,
  readInput,
  setDisabled,
  voice,
  writeContext,
} = require('./kevin-runtime');

const deactivate = /^(stop kevin|normal mode)[.!?]*$/i;
const activate = /^(start kevin|kevin mode|talk like kevin)[.!?]*$/i;

readInput((input) => {
  const prompt = String(input.prompt || '').trim();

  if (deactivate.test(prompt)) {
    setDisabled(input.session_id);
    writeContext('UserPromptSubmit', 'KEVIN MODE OFF. Use normal prose until reactivated.');
    return;
  }

  if (activate.test(prompt)) {
    clearDisabled(input.session_id);
    writeContext('UserPromptSubmit', voice());
  }
});
