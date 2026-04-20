import argparse
import os
import sys


# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


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
