export default defineAppConfig({
    ui: {
        colors: {
            neutral: "neutral",
        },
        button: {
            compoundVariants: [
                {
                    color: "neutral",
                    variant: "solid",
                    class: "text-default bg-default hover:bg-default/90 active:bg-default/90 disabled:bg-default aria-disabled:bg-default focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-default",
                },
            ],
        },
    },
});
