const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: "/static/",
  chainWebpack: (config) => {
    config.plugin("html").tap((args) => {
      args[0].title = "trim-减简";
      return args;
    });
  },
});
