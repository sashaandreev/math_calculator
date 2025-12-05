module.exports = {
  testEnvironment: 'jsdom',
  roots: ['<rootDir>/tests'],
  testMatch: ['**/test_frontend_*.js'],
  setupFilesAfterEnv: ['<rootDir>/tests/jest.setup.js'],
  transformIgnorePatterns: [
    'node_modules/(?!(jsdom)/)',
  ],
  moduleNameMapper: {
    '^mathinput/(.*)$': '<rootDir>/mathinput/static/mathinput/$1',
  },
  collectCoverageFrom: [
    'mathinput/static/mathinput/js/**/*.js',
    '!mathinput/static/mathinput/js/**/*.min.js',
  ],
  coverageDirectory: 'tests/coverage',
  verbose: true,
};

