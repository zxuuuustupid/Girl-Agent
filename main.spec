# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

import PySide6
import shiboken6


project_root = Path.cwd()
src_dir = project_root / "src"
assets_dir = project_root / "assets"
pyside_dir = Path(PySide6.__file__).resolve().parent
shiboken_dir = Path(shiboken6.__file__).resolve().parent
env_root = Path(sys.executable).resolve().parent
conda_roots = [env_root]
if env_root.parent.name.lower() == "envs":
    conda_roots.append(env_root.parent.parent)

datas = [
    (str(assets_dir), "assets"),
    (str(src_dir / "gui" / "qml"), "gui/qml"),
]

hiddenimports = [
    "shiboken6",
    "inspect",
    "PySide6.support.deprecated",
    "PySide6.QtCore",
    "PySide6.QtGui",
    "PySide6.QtQml",
    "PySide6.QtQuick",
    "PySide6.QtQuickControls2",
]

for personality_file in (src_dir / "prompts" / "personalities").glob("*.py"):
    if personality_file.stem.startswith("_"):
        continue
    hiddenimports.append(f"prompts.personalities.{personality_file.stem}")

binaries = []

for dll_path in pyside_dir.glob("*.dll"):
    binaries.append((str(dll_path), "PySide6"))

for dll_path in shiboken_dir.glob("*.dll"):
    binaries.append((str(dll_path), "."))

extra_binary_patterns = (
    "libssl*.dll",
    "libcrypto*.dll",
    "libEGL.dll",
    "libGLESv2.dll",
    "opengl32sw.dll",
    "d3dcompiler_47.dll",
    "D3DCompiler_47.dll",
)

seen_binary_targets = {item[0] for item in binaries}

for conda_root in conda_roots:
    conda_bin_dir = conda_root / "Library" / "bin"
    if not conda_bin_dir.exists():
        continue
    for pattern in extra_binary_patterns:
        for dll_path in conda_bin_dir.glob(pattern):
            source = str(dll_path)
            if source in seen_binary_targets:
                continue
            binaries.append((source, "."))
            seen_binary_targets.add(source)


a = Analysis(
    ["src/main_gui.py"],
    pathex=[str(src_dir)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[str(src_dir / "runtime_hooks" / "pyi_dll_path.py")],
    excludes=[],
    noarchive=False,
)

a.binaries = [
    entry for entry in a.binaries
    if Path(entry[0]).name.lower() not in {"icuuc.dll", "icudt73.dll", "icuuc73.dll", "icuin.dll", "icuin73.dll"}
]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    exclude_binaries=False,
    name="GirlAgent",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=str(assets_dir / "heart.ico"),
    onefile=True,
)
