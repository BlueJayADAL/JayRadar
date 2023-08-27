module.exports = {
  root: true,
  parser: '@typescript-eslint/parser',
  settings: {
    'import/resolver': {
      typescript: {},
    },
  },
  plugins: ['react-prefer-function-component', 'import', 'jsdoc', '@typescript-eslint'],
  extends: [
    'airbnb',
    'plugin:@typescript-eslint/recommended',
  ],
  rules: {
    'react/react-in-jsx-scope': 'off',
    'react/jsx-uses-react': 'off',
    'react/jsx-filename-extension': [1, { extensions: ['.ts', '.tsx'] }],
    'react/jsx-uses-vars': 'error',
    'react-prefer-function-component/react-prefer-function-component': ['error'],
    'react/require-default-props': 'off',
    'import/no-duplicates': 'error',
    'import/no-named-as-default': 'error',
    'import/no-named-as-default-member': 'error',
    'import/no-extraneous-dependencies': 'error',
    'import/extensions': 'off',
    'no-use-before-define': 'off',
    'jsx-a11y/label-has-associated-control': 'off',
    'no-console': 'off',
    'jsdoc/require-jsdoc': ['error', {
      require: {
        FunctionDeclaration: true,
        ArrowFunctionExpression: true,
        FunctionExpression: true,
      },
    }],
    'jsdoc/require-description': 2,
    'jsdoc/no-types': 2,
    'jsdoc/check-alignment': 2,
    'jsdoc/check-indentation': 2,
    '@typescript-eslint/no-use-before-define': 'off',
    'react/prop-types': 'off',
    '@typescript-eslint/indent': ['error', 2],
  },
  env: {
    browser: true,
    es2020: true,
  },
};
