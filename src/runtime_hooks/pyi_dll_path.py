import os
import sys


def _prepend_path(path: str) -> None:
    if not path or not os.path.isdir(path):
        return
    current = os.environ.get("PATH", "")
    parts = current.split(os.pathsep) if current else []
    if path not in parts:
        os.environ["PATH"] = path + (os.pathsep + current if current else "")
    if hasattr(os, "add_dll_directory"):
        try:
            os.add_dll_directory(path)
        except OSError:
            pass


if sys.platform.startswith("win"):
    base_dir = getattr(sys, "_MEIPASS", "")
    candidate_dirs = [
        base_dir,
        os.path.join(base_dir, "PySide6"),
        os.path.join(base_dir, "shiboken6"),
    ]

    for dll_dir in candidate_dirs:
        _prepend_path(dll_dir)
