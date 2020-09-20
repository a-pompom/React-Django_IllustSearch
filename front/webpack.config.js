const path = require('path');

module.exports = {
    
    // 開発用モード
    mode: "development",
    // App.tsxファイルを起点にビルド
    entry: "./src/index.tsx",
    
    // 出力設定
    output: {
        // 出力先のパス
        path: `${__dirname}/public`,
        // バンドル結果の出力名
        filename: "script.js"
    },
	devServer: {
        contentBase: path.join(__dirname, 'public'),
        compress: true,
        port: 3000,
		host:"0.0.0.0"
    },
    module: {
        rules: [
            {
                // 拡張子がts, tsxを対象
                // コンパイルルールとして、TypeScriptを利用
                test: /\.tsx?$/,
                use: "ts-loader"
            }
        ]
    },
    // importで省略できる拡張子
    resolve:  {
        extensions: [".ts", ".tsx", ".js", ".json"],
        modules: [
              path.resolve('./src'),
              path.resolve('./node_modules')
        ]
    }
}
