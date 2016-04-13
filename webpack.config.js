
'use strict';

var path = require('path');

module.exports = {
	entry: [
		'webpack/hot/only-dev-server',
		'webpack-dev-server/client?http://localhost:4188',
		path.resolve(__dirname, 'static/index.js')
	],
	output: {
		path: path.resolve(__dirname, 'static/build'),
		filename: 'bundle.js',
		publicPath: '/static/'
	},
	module: {
		loaders: [{
			test: /\.jsx?$/,
			loader: 'babel-loader'
		}, {
			test: /\.css$/, // Only .css files
			loader: 'style!css' // Run both loaders
		}]
	}
};
