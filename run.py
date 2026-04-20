import argparse
import os
import sys
from pathlib import Path


# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def configure_runtime_environment() -> None:
    path_entries = os.environ.get("PATH", "").split(os.pathsep) if os.environ.get("PATH") else []
    python_bin_dir = str(Path(sys.executable).parent)
    if python_bin_dir not in path_entries:
        path_entries.insert(0, python_bin_dir)
    for candidate in ("/opt/homebrew/bin", "/usr/local/bin"):
        if candidate not in path_entries and Path(candidate).exists():
            path_entries.insert(0, candidate)
    os.environ["PATH"] = os.pathsep.join(path_entries)

    developer_dir = Path("/Applications/Xcode.app/Contents/Developer")
    if "DEVELOPER_DIR" not in os.environ and developer_dir.exists():
        os.environ["DEVELOPER_DIR"] = str(developer_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the hardened iOS Bridge server")
    parser.add_argument("--host", default=os.getenv("IOS_BRIDGE_HOST"))
    parser.add_argument("--port", type=int, default=None)
    parser.add_argument("--access-token", default=os.getenv("IOS_BRIDGE_ACCESS_TOKEN"))
    parser.add_argument(
        "--enable-debug-routes",
        action="store_true",
        help="Enable the debug routes that are disabled by default in this hardened fork.",
    )
    parser.add_argument(
        "--enable-file-bridge",
        action="store_true",
        help="Enable file push/pull endpoints that are disabled by default in this hardened fork.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    configure_runtime_environment()

    if args.host:
        os.environ["IOS_BRIDGE_HOST"] = args.host
    if args.port is not None:
        os.environ["IOS_BRIDGE_PORT"] = str(args.port)
    if args.access_token:
        os.environ["IOS_BRIDGE_ACCESS_TOKEN"] = args.access_token
    if args.enable_debug_routes:
        os.environ["IOS_BRIDGE_ENABLE_DEBUG_ROUTES"] = "1"
    if args.enable_file_bridge:
        os.environ["IOS_BRIDGE_ENABLE_FILE_BRIDGE"] = "1"

    from app.main import app
    from app.config.settings import settings
    import uvicorn

    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower(),
    )
else:
    from app.main import app
