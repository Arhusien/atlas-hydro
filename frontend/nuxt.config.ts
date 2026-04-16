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
            href: `/favicon/dark/${name}`,
            media: "(prefers-color-scheme: light)",
        },
        {
            ...baseLink,
            href: `/favicon/light/${name}`,
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
        "@vueuse/nuxt",
        "@pinia/nuxt",
    ],
    ssr: false,
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
                "luxon",
                "chart.js",
                "chartjs-adapter-date-fns",
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
