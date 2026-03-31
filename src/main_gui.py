import os
import sys
from pathlib import Path
from datetime import datetime

from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine


ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))

from gui.app_bridge import AppBridge


def _startup_log_path() -> Path:
    candidates = []
    if getattr(sys, "frozen", False):
        candidates.append(Path(sys.executable).resolve().parent / "startup.log")
    candidates.append(ROOT_DIR / "startup.log")
    candidates.append(Path.cwd() / "startup.log")

    for path in candidates:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)
            return path
        except OSError:
            continue

    return Path("startup.log")


STARTUP_LOG = _startup_log_path()


def log_startup(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with STARTUP_LOG.open("a", encoding="utf-8") as fh:
        fh.write(f"[{timestamp}] {message}\n")


def create_app() -> tuple[QGuiApplication, QQmlApplicationEngine]:
    os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")
    log_startup(f"create_app start frozen={getattr(sys, 'frozen', False)}")
    log_startup(f"ROOT_DIR={ROOT_DIR}")
    app = QGuiApplication(sys.argv)
    app.setApplicationName("GirlAgent")
    app.setOrganizationName("GirlAgent")

    icon_path = ROOT_DIR.parent / "assets" / "heart.png"
    log_startup(f"icon_path={icon_path} exists={icon_path.exists()}")
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    engine = QQmlApplicationEngine()
    engine.warnings.connect(
        lambda warnings: [log_startup(f"QML warning: {warning.toString()}") for warning in warnings]
    )
    bridge = AppBridge()
    engine.rootContext().setContextProperty("bridge", bridge)

    qml_path = ROOT_DIR / "gui" / "qml" / "Main.qml"
    log_startup(f"qml_path={qml_path} exists={qml_path.exists()}")
    engine.load(os.fspath(qml_path))
    log_startup(f"rootObjects={len(engine.rootObjects())}")
    return app, engine


def main() -> int:
    try:
        app, engine = create_app()
        if not engine.rootObjects():
            log_startup("startup failed: no root objects")
            return 1
        log_startup("startup success: entering event loop")
        return app.exec()
    except Exception as exc:
        log_startup(f"unhandled exception: {exc!r}")
        raise


if __name__ == "__main__":
    sys.exit(main())
