module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // enforce type(scope): subject
    'type-enum': [2, 'always', [
      'feat', 'fix', 'chore', 'docs', 'style', 'refactor', 'perf', 'test'
    ]],
  },
};
