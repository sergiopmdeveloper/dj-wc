const path = require('path');

const common = {
  entry: './src/index.ts',
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: ['.ts', '.js'],
  },
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, '../static/js'),
  },
};

const development = {
  ...common,
  mode: 'development',
  devtool: 'inline-source-map',
  devServer: {
    contentBase: path.join(__dirname, '../static'),
    compress: true,
    port: 9000,
    hot: true,
  },
};

const production = {
  ...common,
  mode: 'production',
};

module.exports = (env) => {
  if (env.production) {
    return production;
  }

  return development;
};
