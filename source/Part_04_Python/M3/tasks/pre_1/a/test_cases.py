notes = " "

labels = ["Input 1", "Input 2", "Input 3"]

cases = {
    1: {
        "callable": "main",
        "entries": [5, 2, 0],  # multiple numbers then stop
    },
    2: {
        "callable": "main",
        "entries": [3, 0],  # single number then stop
    },
    3: {
        "callable": "main",
        "entries": [0],  # immediately exit
    },
}
