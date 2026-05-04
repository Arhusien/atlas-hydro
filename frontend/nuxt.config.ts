import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
    modules: [
        "@nuxt/eslint",
        "@nuxt/a11y",
        "@nuxt/hints",
        "@nuxt/ui",
        "@nuxtjs/leaflet",
        "@nuxtjs/i18n",
        "@nuxtjs/seo",
        "@nuxtjs/device",
        "@vueuse/nuxt",
    ],
    ssr: true,
    components: [
        {
            path: "~/components/ui",
            prefix: "UI",
            pathPrefix: false,
        },
        "~/components",
    ],
    devtools: {
        enabled: true,
    },
    app: {
        head: {
            htmlAttrs: {
                class: "dark",
                style: "color-scheme: dark;",
            },
            meta: [
                {
                    name: "color-scheme",
                    content: "dark",
                },
            ],
            link: [
                {
                    rel: "icon",
                    href: "/favicon-dark.ico",
                    type: "image/x-icon",
                },
                {
                    rel: "manifest",
                    href: "/app.webmanifest",
                },
            ],
        },
    },
    css: [
        "./app/assets/css/main.css",
    ],
    site: {
        url: "https://www.atlashydro.ca",
        name: "Atlas Hydro",
        description: "Atlas Hydro répertorie les installations d'Hydro-Québec et les territoires liés au réseau.",
        defaultLocale: "fr",
    },
    ui: {
        colorMode: false,
    },
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
        build: {
            rollupOptions: {
                output: {
                    manualChunks: {
                        chartjs: ["chart.js", "vue-chartjs", "chartjs-adapter-date-fns"],
                    },
                },
            },
        },
        optimizeDeps: {
            include: [
                "leaflet",
                "geolib",
                "luxon",
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
    icon: {
        clientBundle: {
            scan: true,
        },
    },
    ogImage: {
        zeroRuntime: true,
    },
    seo: {
        meta: {
            themeColor: "#171717",
            ogImage: "https://www.atlashydro.ca/img/Logo.png",
            twitterCard: "summary",
        },
    },
    sitemap: {
        xsl: false,
    },
});
