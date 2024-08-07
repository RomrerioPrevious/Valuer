import PyInstaller.__main__
from pathlib import Path
from icecream import ic

HERE = Path(__file__).parent.absolute()
path_to_main = str(HERE / "main.py")


def install():
    PyInstaller.__main__.run([
        path_to_main,
        "--onefile",
        "--windowed",
        "-n valuer",
        "--icon=valuer/resources/style/valuer.ico"
    ])
