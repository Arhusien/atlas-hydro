import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
    modules: [
        "@nuxt/eslint",
        "@nuxt/a11y",
        "@nuxt/hints",
        "@nuxt/ui",
        "@nuxtjs/leaflet",
        "@nuxtjs/i18n",
        "@nuxtjs/robots",
        "@nuxtjs/sitemap",
        "@pinia/nuxt",
    ],
    ssr: false,
    devtools: {
        enabled: true,
    },
    css: [
        "./app/assets/css/main.css",
    ],
    routeRules: {
        "/api/**": {
            proxy: `${process.env.NUXT_BACKEND_API_BASE}/api/**`,
        },
    },
    compatibilityDate: "2025-07-15",
    vite: {
        plugins: [
            tailwindcss(),
        ],
        optimizeDeps: {
            include: [
                "leaflet",
                "geolib",
                "@lucide/vue",
            ],
        },
    },
    eslint: {
        config: {
            stylistic: {
                indent: 2,
                quotes: "double",
                semi: true,
            },
        },
    },
    i18n: {
        strategy: "no_prefix",
        defaultLocale: "fr",
        locales: [
            "fr",
        ],
    },
});
