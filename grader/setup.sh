#!/usr/bin/env bash

# Install additional packages
# xvfb:
#   - a virtual frame buffer that us to draw on the "screen" for turtle
#     graphics and matplotlib
# ghostscript:
#   - provides postscript support for saving the turtle graphics canvas and
#     matplotlib plots
# tesseract-ocr:
#   - Optical character recognition for character writing tests
# tmux:
#   - terminal multiplexer to aid in debugging
apt-get install -y xvfb ghostscript tesseract-ocr tmux

# Summer 2025: Install python3.13 to match student's Python version.
add-apt-repository ppa:deadsnakes/ppa
apt-get update && apt-get install -y python3.13 python3.13-tk python3.13-venv

# Run the auto-grader in a python 3.13 virtual environment.  Otherwise we can't
# install pytesseract because it depends on an up-to-date setuptools, but
# updating setuptools outside of a virtual environment breaks Gradescope.
python3.13 -m venv env
source env/bin/activate

# Upgrade pip, then install wheel so we won't have to build other requirements.
python3.13 -m pip install --upgrade pip wheel
python3.13 -m pip install git+https://github.com/pritchettk/generic-grader git+https://github.com/pritchettk/gradescope-utils-extended pandas faker opencv-python
