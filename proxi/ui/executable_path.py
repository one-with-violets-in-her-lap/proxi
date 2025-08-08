import os
import sys

if getattr(sys, "frozen", False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path = getattr(sys, "_MEIPASS")
else:
    application_path = os.path.abspath("./")


def build_path_from_executable(*path_parts: str):
    return os.path.abspath(os.path.join(application_path, *path_parts))
