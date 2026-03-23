import tailwindcss from "@tailwindcss/vite";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    modules: [
        "@nuxt/eslint",
        "@nuxt/a11y",
        "@nuxt/hints",
        "@nuxt/scripts",
        "@nuxt/image",
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
    compatibilityDate: "2025-07-15",
    vite: {
        plugins: [
            tailwindcss(),
        ],
        optimizeDeps: {
            include: [
                "leaflet",
                "lucide",
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
});
