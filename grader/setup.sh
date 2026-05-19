#!/usr/bin/env bash
# Install additional packages
# xvfb: a virtual frame buffer for turtle graphics and matplotlib
# ghostscript: postscript support for saving the turtle graphics canvas
# tesseract-ocr: Optical character recognition for character writing tests
# tmux: terminal multiplexer to aid in debugging
apt-get install -y xvfb ghostscript tesseract-ocr tmux

# Install python3.13 to match student's Python version.
add-apt-repository ppa:deadsnakes/ppa
apt-get update && apt-get install -y python3.13 python3.13-tk python3.13-venv

# Setup SSH for GitHub Access
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

# Run the auto-grader in a python 3.13 virtual environment.
python3.13 -m venv /autograder/venv
source /autograder/venv/bin/activate

# Upgrade pip, then install wheel and required packages
python3.13 -m pip install --upgrade pip wheel
python3.13 -m pip install git+https://github.com/pritchettk/generic-grader git+https://github.com/pritchettk/gradescope-utils-extended pandas faker opencv-python jinja2 pyyaml
