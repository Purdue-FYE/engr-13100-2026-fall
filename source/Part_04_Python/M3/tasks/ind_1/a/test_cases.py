notes = " "

labels = ["List of Items"]

cases = {
    1: {
        "callable": "main",
        "entries": ["normal,fragile,heavy,error,normal"],
    },
    2: {
        "callable": "main",
        "entries": ["heavy,fragile,error,error,heavy,normal,fragile,normal"],
    },
    # TEST ERROR COUNTING AND INSPECTION ALERT
    3: {
        "callable": "main",
        "entries": ["error,normal,error,error,fragile,normal"],
    }
}