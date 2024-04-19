document.onload = function () {
    const picker = new easepick.create({
        // element: "#datepicker",
        element: ".datepicker",
        css: [
            "https://cdn.jsdelivr.net/npm/@easepick/bundle@1.2.1/dist/index.css"
        ],
        zIndex: 10,
        lang: "ru-RU",
        AmpPlugin: {
            dropdown: {
                months: true,
                years: true,
                minYear: 2000,
                maxYear: 2050
            }
        },
        plugins: [
            "AmpPlugin",
            "RangePlugin",
            "LockPlugin",
            "PresetPlugin"
        ]
    })
    console.log("ASS")
    alert('If you see this alert, then your custom JavaScript script has run!')
}
