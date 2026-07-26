from pathlib import Path

from PyInstaller.utils.hooks import collect_all


# Carpeta principal del proyecto
BASE_DIR = Path(SPECPATH)


ctk_datas, ctk_binaries, ctk_hiddenimports = collect_all(
    "customtkinter"
)

mp_datas, mp_binaries, mp_hiddenimports = collect_all(
    "mediapipe"
)

sk_datas, sk_binaries, sk_hiddenimports = collect_all(
    "sklearn"
)

scipy_datas, scipy_binaries, scipy_hiddenimports = collect_all(
    "scipy"
)



datas = [
    (
        str(BASE_DIR / "modelo_lsc.pkl"),
        "."
    ),
    (
        str(BASE_DIR / "demo" / "recursos"),
        "demo/recursos"
    ),
]

datas += ctk_datas
datas += mp_datas
datas += sk_datas
datas += scipy_datas


binaries = []

binaries += ctk_binaries
binaries += mp_binaries
binaries += sk_binaries
binaries += scipy_binaries


hiddenimports = [
    "sklearn",
]

hiddenimports += ctk_hiddenimports
hiddenimports += mp_hiddenimports
hiddenimports += sk_hiddenimports
hiddenimports += scipy_hiddenimports



a = Analysis(
    [str(BASE_DIR / "demo" / "app.py")],

    pathex=[
        str(BASE_DIR),
        str(BASE_DIR / "demo"),
    ],

    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,

    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],

    noarchive=False,
    optimize=0,
)


pyz = PYZ(a.pure)



exe = EXE(
    pyz,
    a.scripts,

    [],

    exclude_binaries=True,

    name="LASIC",

    debug=False,
    bootloader_ignore_signals=False,

    strip=False,
    upx=True,

    console=False,

    disable_windowed_traceback=False,
)




coll = COLLECT(
    exe,

    a.binaries,
    a.datas,

    strip=False,
    upx=True,

    upx_exclude=[],

    name="LASIC",
)