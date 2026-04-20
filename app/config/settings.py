from typing import Optional
import os


def _env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_token(name: str) -> Optional[str]:
    value = os.getenv(name)
    if value is None:
        return None
    value = value.strip()
    return value or None

class Settings:
    """Application settings"""
    
    # Device Configuration - Remove hardcoded UDID
    # UDID will be provided by session management
    
    # Video Configuration
    DEFAULT_VIDEO_FPS: int = 60
    VIDEO_QUEUE_SIZE: int = 3
    WEBRTC_QUEUE_SIZE: int = 2
    
    # Connection Management
    MAX_CONNECTIONS_PER_SESSION: int = 10
    MAX_CONNECTIONS_PER_MINUTE: int = 20
    CONNECTION_CLEANUP_INTERVAL: int = 30
    
    # Resource Management
    MAX_MEMORY_MB: int = 2048
    SERVICE_IDLE_TIMEOUT: int = 300  # 5 minutes
    MEMORY_CHECK_INTERVAL: int = 30
    
    # Quality Settings
    DEFAULT_JPEG_QUALITY: int = 80
    WEBRTC_HIGH_QUALITY: int = 95
    
    # Timeouts
    SCREENSHOT_TIMEOUT: float = 0.5
    TAP_TIMEOUT: float = 2.0
    SWIPE_TIMEOUT: float = 3.0
    TEXT_TIMEOUT: float = 5.0
    
    # Server Configuration
    HOST: str = os.getenv("IOS_BRIDGE_HOST", "127.0.0.1")
    PORT: int = int(os.getenv("IOS_BRIDGE_PORT", "8000"))
    ACCESS_TOKEN: Optional[str] = _env_token("IOS_BRIDGE_ACCESS_TOKEN")
    AUTH_COOKIE_NAME: str = "ios_bridge_token"
    AUTH_HEADER_NAME: str = "x-ios-bridge-token"
    ENABLE_DEBUG_ROUTES: bool = _env_flag("IOS_BRIDGE_ENABLE_DEBUG_ROUTES", default=False)
    ENABLE_FILE_BRIDGE: bool = _env_flag("IOS_BRIDGE_ENABLE_FILE_BRIDGE", default=False)
    
    # Paths
    STATIC_DIR: str = "static"
    TEMP_DIR: Optional[str] = None
    
    # Logging
    LOG_LEVEL: str = os.getenv("IOS_BRIDGE_LOG_LEVEL", "INFO")

settings = Settings()
