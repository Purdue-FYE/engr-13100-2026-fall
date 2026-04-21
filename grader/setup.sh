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

mkdir -p /root/.ssh
cp /autograder/source/deploy_key /root/.ssh/deploy_key
chmod 600 /root/.ssh/deploy_key

# Create an SSH config file telling git to use this key for GitHub
cat << 'EOF' > /root/.ssh/config
Host github.com
    IdentityFile /root/.ssh/deploy_key
    IdentitiesOnly yes
EOF

# Add GitHub to known_hosts to prevent "host key verification failed" errors
ssh-keyscan -t rsa,ed25519 github.com >> /root/.ssh/known_hosts

# Run the auto-grader in a python 3.13 virtual environment.  Otherwise we can't
# install pytesseract because it depends on an up-to-date setuptools, but
# updating setuptools outside of a virtual environment breaks Gradescope.
python3.13 -m venv env
source env/bin/activate

# Upgrade pip, then install wheel so we won't have to build other requirements.
python3.13 -m pip install --upgrade pip wheel
python3.13 -m pip install git+https://github.com/pritchettk/generic-grader git+https://github.com/pritchettk/gradescope-utils-extended pandas faker opencv-python

# Clone autograder files from GitHub
git clone --no-checkout --depth 1 --sparse git@github.com:your-organization/your-repo.git /autograder/my_grader_repo

cd /autograder/my_grader_repo

git sparse-checkout set
git checkout main