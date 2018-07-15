from cx_Freeze import setup, Executable
import sys
base = 'WIN32GUI' if sys.platform == "win32" else None


executables = [Executable("TCGAD.py", base=base, icon='dna.ico')]

packages = []
include_files=["down.PNG"]
options = {
    'build_exe': {
        'packages':packages,
        'include_files': include_files
    },

}

setup(
    name = "TCGAD",
    options = options,
    version = "1.0",
    description = 'TCGA downloader',
    executables = executables
)