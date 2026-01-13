import qrcode

qrcode.make(
    "https://purdue-engr-13300.github.io/2026-spring/intro.html",
    version=1,  # smallest version
    box_size=8,  # size of the boxes
    border=2,
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # low error correction
).save("source/_static/qr_code.png")
