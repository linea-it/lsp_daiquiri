const path = require('path');

var execSync = require('child_process').execSync;
var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

var daiquiri_path = execSync('python manage.py daiquiri_path').toString().trim();

module.exports = {
    entry: {
        'base': path.resolve(daiquiri_path, 'core/static/core/lib/base.js'),
        'examples': path.resolve(daiquiri_path, 'query/static/query/lib/examples.js'),
        'messages': path.resolve(daiquiri_path, 'contact/static/contact/lib/messages.js'),
        'metadata': path.resolve(daiquiri_path, 'metadata/static/metadata/lib/metadata.js'),
        'query': path.resolve(daiquiri_path, 'query/static/query/lib/query.js'),
        'serve': path.resolve(daiquiri_path, 'serve/static/serve/lib/serve.js'),
        'users': path.resolve(daiquiri_path, 'auth/static/auth/lib/users.js')
    },
    output: {
        path: __dirname + '/vendor/lib/',
        filename: '[name].js'
    },
    module: {
        rules: [
            // add a rule to use the ExtractTextPlugin for css files
            {
                test: /\.css$/,
                use: ExtractTextPlugin.extract({
                    fallback: 'style-loader',
                    use: 'css-loader'
                })
            },
            // add a rule to copy the font files
            {
                test: /\.(ttf|eot|svg|woff|woff2)$/,
                use: [{
                    'loader': 'file-loader',
                    'options': {}
                }]
            }
        ]
    },
    resolve: {
        // look for the modules in the local `node_modules` directory
        modules: [path.resolve(__dirname, 'node_modules')]
    },
    plugins: [
        new webpack.optimize.UglifyJsPlugin({minimize: true}),
        new ExtractTextPlugin('[name].css'),
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery'
        })
    ]
};
