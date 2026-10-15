# Import gitpython into the freecad appImage environment
# From the Freecad python console, run:
# exec(open("/<file path..>/install_gitPython.py").read())

import os
import subprocess
import FreeCAD as App
import addonmanager_utilities as utils

# 1. Define the module you want to install
module_to_install = "gitpython"

# 2. Get the AppImage's internal Python executable and the user vendor directory
python_exe = App.getHomePath() + "bin/python"
vendor_path = utils.get_pip_target_directory()

# 3. Construct and run the pip command
cmd = [python_exe, "-m", "pip", "install", "--target", vendor_path, module_to_install]

print(f"Installing {module_to_install} to {vendor_path}...")
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("Installation successfully completed!")
else:
    print("Error during installation:\n", result.stderr)

