import subprocess
import base64
from PIL import Image
import io
from typing import Optional, Dict
from app.config.settings import settings
from app.core.logging import logger

class ScreenshotService:
    """Service for screenshot capture with dynamic UDID support"""
    
    def __init__(self, udid: Optional[str] = None):
        self.udid = udid
    
    def set_udid(self, udid: str):
        """Set the UDID for this service instance"""
        self.udid = udid
    
    def capture_screenshot(self, quality: int = None) -> Optional[Dict[str, any]]:
        """Capture device screenshot"""
        if not self.udid:
            logger.error("No UDID set for screenshot capture")
            return None
            
        if quality is None:
            quality = settings.DEFAULT_JPEG_QUALITY
            
        try:
            cmd = ["xcrun", "simctl", "io", self.udid, "screenshot", "--type=jpeg", "-"]
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=settings.SCREENSHOT_TIMEOUT
            )

            if result.returncode == 0 and result.stdout:
                image_data = result.stdout
                with Image.open(io.BytesIO(image_data)) as img:
                    pixel_width, pixel_height = img.size

                return {
                    "data": base64.b64encode(image_data).decode('utf-8'),
                    "pixel_width": pixel_width,
                    "pixel_height": pixel_height
                }

        except subprocess.TimeoutExpired:
            logger.debug(f"Screenshot timeout for UDID: {self.udid}")
        except Exception as e:
            logger.error(f"Screenshot error for UDID {self.udid}: {e}")
        
        return None
    
    def capture_ultra_fast_screenshot(self) -> Optional[Dict[str, any]]:
        """Ultra-fast screenshot for real-time streaming"""
        return self.capture_screenshot(quality=settings.DEFAULT_JPEG_QUALITY)
    
    def capture_high_quality_screenshot(self) -> Optional[Dict[str, any]]:
        """High-quality screenshot"""
        return self.capture_screenshot(quality=settings.WEBRTC_HIGH_QUALITY)
