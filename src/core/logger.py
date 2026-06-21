"""
Application Logger
------------------
This module configures logging for the entire application.
"""

import logging
import os

from src.config import settings

# =====================================================
# Create Log Directory
# =====================================================

os.makedirs(settings.LOG_FOLDER, exist_ok=True)

# =====================================================
# Configure Logging
# =====================================================

logging.basicConfig(
    filename=os.path.join(settings.LOG_FOLDER, "application.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# =====================================================
# Logger Object
# =====================================================

logger = logging.getLogger(__name__)