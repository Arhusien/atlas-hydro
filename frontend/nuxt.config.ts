import tailwindcss from "@tailwindcss/vite";

const faviconPaths = [
    "android-chrome-192x192.png",
    "android-chrome-512x512.png",
    "apple-touch-icon.png",
    "favicon-16x16.png",
    "favicon-32x32.png",
    "favicon.ico",
];

const faviconLinks = faviconPaths.flatMap((name) => {
    const isIco = name.endsWith(".ico"),
        type = isIco ? "image/x-icon" : "image/png",
        rel = name.includes("apple-touch-icon") ? "apple-touch-icon" : "icon",
        size = isIco ? undefined : name.match(/(\d+x\d+)/)?.[0];

    const baseLink = {
        rel,
        type,
        size,
    };

    return [
        {
            ...baseLink,
            href: `/img/favicon/dark/${name}`,
            media: "(prefers-color-scheme: light)",
        },
        {
            ...baseLink,
            href: `/img/favicon/light/${name}`,
            media: "(prefers-color-scheme: dark)",
        },
    ];
});

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
            title: "Atlas Hydro",
            link: [
                ...faviconLinks,
            ],
        },

    },
    css: [
        "./app/assets/css/main.css",
    ],
    colorMode: {
        preference: "dark",
    },
    routeRules: {
        "/api/static/**/*.geojson": {
            headers: {
                "Content-Type": "application/json",
                "Content-Disposition": "inline",
            },
        },
        "/api/static/**": {
            proxy: `${process.env.NUXT_BACKEND_API_BASE}/static/**`,
        },
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
});
