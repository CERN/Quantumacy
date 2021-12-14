import colors from "vuetify/es5/util/colors";

export default {
  srcDir: "client/",
  ssr: false,
  server: {
    port: process.env.PORT
  },
  head: {
    titleTemplate: "%s - Homomorphic Encryption with Medical Data",
    title: "HEwMD",
    htmlAttrs: {
      lang: "en"
    },
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { hid: "description", name: "description", content: "" },
      { name: "format-detection", content: "telephone=no" }
    ],
    link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }]
  },

  css: [],

  components: true,

  buildModules: [
    "@nuxtjs/eslint-module",
    "@nuxtjs/vuetify",
    "@nuxtjs/dotenv"
  ],
  env: {
    HOMOMORPHIC_BACKEND: process.env.HOMOMORPHIC_BACKEND
  },

  modules: ["@nuxtjs/axios"],
  plugins: [],

  vuetify: {
    customVariables: ["~/assets/variables.scss"],
    theme: {
      dark: true,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        }
      }
    }
  },

  build: {}
};
