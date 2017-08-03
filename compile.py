import sys
from cx_Freeze import setup, Executable

target = Executable(
    script="application.py",
    base="Win32GUI",
    icon="masil.ico"
    )

setup(
    name = "masil",
    version = "1.0",
    description = "Manages reservations and customer info at Masil.",
    author="Jungkyu Park",
    executables = [target])