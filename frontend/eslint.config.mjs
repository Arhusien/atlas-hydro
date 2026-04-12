import tsParser from "@typescript-eslint/parser";
import withNuxt from "./.nuxt/eslint.config.mjs";

export default withNuxt({
    files: [
        "**/*.{js,mjs,cjs,ts,tsx,mts,cts}",
    ],
    languageOptions: {
        parser: tsParser,
    },
    rules: {
        "vue/multi-word-component-names": "off",
        "vue/singleline-html-element-content-newline": "error",
        "vue/multiline-html-element-content-newline": "error",
        "no-console": process.env.NODE_ENV === "production" ? "warn" : "off",
        "@stylistic/indent": [
            "error",
            4,
        ],
        "quotes": [
            "error",
            "double",
        ],
        "semi": [
            "error",
            "always",
        ],
    },
}, {
    files: [
        "**/*.vue",
    ],
    rules: {
        "indent": "off",
        "@stylistic/indent": "off",
        "vue/script-indent": [
            "error", 2, {
                baseIndent: 1,
            },
        ],
    },
});
