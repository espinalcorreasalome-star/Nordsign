import sys
from pathlib import Path

def ruta_recurso(*partes: str)-> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_dir= Path(sys._MEIPASS)
    else:
        base_dir=Path(__file__).resolve().parent.parent
    return base_dir.joinpath(*partes)