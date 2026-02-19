notes = " "

labels = [
    "Soil moisture (%)",
    "Rain forecast (mm)",
    "Maintenance required",
    "Low pressure",
]

cases = {
    ## maintenance required → DO NOT IRRIGATE
    1: {
        "callable": "main",
        "entries": [15, 0, "yes", "no"],
    },
    ## low pressure → DO NOT IRRIGATE (overrides rain and soil)
    2: {
        "callable": "main",
        "entries": [5, 23, "no", "yes"],
    },
    ## significant rain → DELAY (overrides soil)
    3: {
        "callable": "main",
        "entries": [15, 23, "no", "no"],
    },
    ## RUN FULL (soil < 20%, low rain)
    4: {
        "callable": "main",
        "entries": [15, 0, "no", "no"],
    },
    ## RUN REDUCED (25% > soil ≥ 20%, low rain)
    5: {
        "callable": "main",
        "entries": [21, 0, "no", "no"],
    },
    ## SKIP - DO NOT IRRIGATE (soil ≥ 25%, low rain)
    6: {
        "callable": "main",
        "entries": [36, 10, "no", "no"],
    }
}