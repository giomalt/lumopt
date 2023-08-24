import os

folder_path = "lumopt"

for subdir, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(subdir, file)
        if file_path.endswith(".py"):
            with open(file_path, "r") as f:
                file_contents = f.read()
            file_contents = file_contents.replace("import lumapi", "from fdtd.lumerical import lumapi")
            file_contents = file_contents.replace("from lumapi import FDTD", "from fdtd.lumerical import lumapi\nFDTD = lumapi.FDTD")
            file_contents = file_contents.replace("from lumapi import MODE", "from fdtd.lumerical import lumapi\nMODE = lumapi.MODE")
            with open(file_path, "w") as f:
                f.write(file_contents)