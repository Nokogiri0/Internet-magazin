// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    modules: [
        "nuxt-icon",
        "@element-plus/nuxt",
        "@nuxtjs/tailwindcss",
        "@nuxtjs/google-fonts",
        "@pinia/nuxt",
        "nuxt-swiper",
        "@nuxt/devtools",
        "nuxt-typed-router",
    ],
    ssr: true,
    devtools: { enabled: true, vscode: {} },
    nuxtTypedRouter: {
        strict: true,
    },

    googleFonts: {
        families: {
            "Open+Sans": true,
            Comfortaa: true,
        },
        download: true,
    },
    nitro: {
        devProxy: {
            "/api": {
                target: "http://localhost:8000/api",
                changeOrigin: true,
                prependPath: true,
                cookieDomainRewrite: false,
            },
            "/api/docs": {
                target: "http://localhost:8000/docs",
                changeOrigin: true,
                prependPath: true,
            },
        },
    },
    runtimeConfig: {
        public: {
            MAX_FIRSTNAME_LENGTH: Number(process.env.VITE_MAX_FIRSTNAME_LENGTH),
            MAX_LASTNAME_LENGTH: Number(process.env.VITE_MAX_LASTNAME_LENGTH),
            MAX_PASSWORD_LENGTH: Number(process.env.VITE_MAX_PASSWORD_LENGTH),
            MIN_PASSWORD_LENGTH: Number(process.env.VITE_MIN_PASSWORD_LENGTH),
            MIN_USERNAME_LENGTH: Number(process.env.VITE_MIN_USERNAME_LENGTH),
            MAX_USERNAME_LENGTH: Number(process.env.VITE_MAX_USERNAME_LENGTH),
        },
    },
    css: ["@/assets/styles/global.scss"],
    vite: {
        css: {
            preprocessorOptions: {
                scss: {
                    additionalData: [
                        '@use "@/assets/styles/_colors.scss" as *;',
                        '@use "@/assets/styles/helpers.scss" as *;',
                        '@use "@/assets/styles/breakpoints.scss" as *;',
                    ].join(""),
                },
            },
        },
    },
    plugins: [
        { src: "~/plugins/vue-toastification.js", mode: `client` },
        { src: "~/plugins/api.js" },
        { src: "~/plugins/refreshToken.js", mode: `client` },
    ],
});
