import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "excludes": ["unittest"],
    "zip_include_packages": ["encodings", "PySide6"],
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

# setup(
#     name="Client",
#     version="0.1",
#     description="My GUI application!",
#     options={"build_exe": build_exe_options},
#     executables=[Executable("Client.py", base=base)],
# )

# setup(
#     name="Server",
#     version="0.1",
#     description="My GUI application!",
#     options={"build_exe": build_exe_options},
#     executables=[Executable("Server.py", base=base)],
# )

setup(
    name="ConnectionTester",
    version="0.1",
    description="My GUI application!",
    options={"build_exe": build_exe_options},
    executables=[Executable("testConnect.py", base=base)],
)