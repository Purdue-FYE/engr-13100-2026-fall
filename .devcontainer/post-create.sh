# Install uv and Python dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

git remote add engr-13100-2026-fall https://github.com/Purdue-FYE/engr-13100-2026-fall.git
pre-commit install

# # Install MATLAB X11 dependencies
# #
# # MATLAB requires several graphical libraries to run that are not installed by
# # default in the container. Without them, the installer fails with ambiguous
# # messages like
# #
# #    terminate called after throwing an instance of 'std::runtime_error'
# #         what(): Unable to launch the MATLABWindow application
# #    Aborted

# # To help determine which libraries are missing, we can run MATLABWindow
# # directly like this:
# #
# #    ./bin/glnxa64/MATLABWindow
# #
# # Then we find the packages that provide the missing libraries and install each
# # of them.
# #
# # References:
# # https://www.mathworks.com/matlabcentral/answers/540707-why-does-matlab-fail-to-install-with-a-std-runtime_error-what-unable-to-launch-the-matlabwind#answer_445082
# # https://packages.ubuntu.com/
# sudo apt-get update && sudo apt-get install -y libgtk2.0-0 libatk-bridge2.0-0 libdrm2 libgbm1 libasound2 libgl1-mesa-glx libxt6

# # Enable write access to default MATLAB install locations.
# sudo mkdir -p /usr/local/MATLAB && sudo chown vscode:vscode /usr/local/MATLAB
# sudo chown vscode:vscode /usr/local/bin

# # Download and unzip the MATLAB installer from the latest release.
# gh release download --dir matlab -p matlab*.zip --repo github.com/Purdue-ENGR-13300/homework
# unzip -uo matlab/matlab*.zip -d matlab
# rm matlab/matlab*.zip

# # For matlab_service monitor
# sudo apt-get install -y netcat-traditional
