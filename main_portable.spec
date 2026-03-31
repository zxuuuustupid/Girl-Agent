# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path


project_root = Path.cwd()
src_dir = project_root / "src"
assets_dir = project_root / "assets"

datas = [
    (str(assets_dir), "assets"),
    (str(src_dir / "gui" / "qml"), "gui/qml"),
]

hiddenimports = [
    "PySide6.QtCore",
    "PySide6.QtGui",
    "PySide6.QtQml",
    "PySide6.QtQuick",
    "PySide6.QtQuickControls2",
]


a = Analysis(
    ["src/main_gui.py"],
    pathex=[str(src_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[str(src_dir / "runtime_hooks" / "pyi_dll_path.py")],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="GirlAgentPortable",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=str(assets_dir / "heart.ico"),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="GirlAgentPortable",
)
