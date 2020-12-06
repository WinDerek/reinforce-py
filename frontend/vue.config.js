// Documentation: https://cli.vuejs.org/config/#vue-config-js

module.exports = {
  // Proxy all webpack dev-server requests starting with /api
  // to our backend (localhost:41552) using http-proxy-middleware
  // see https://cli.vuejs.org/config/#devserver-proxy
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:41552',
        ws: true,
        changeOrigin: true
      }
    }
  },

  // Disable production source map
  productionSourceMap: false,

  outputDir: './dist',
}
