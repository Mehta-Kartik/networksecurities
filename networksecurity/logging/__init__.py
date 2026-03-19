# networksecurity/logging/__init__.py (NO logger.py file!)
import logging
import os
from datetime import datetime
from pathlib import Path

# Project root logs
BASE_DIR = Path(__file__).parent.parent
logs_dir = BASE_DIR / "logs"
logs_dir.mkdir(exist_ok=True)

log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_path = logs_dir / log_file

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_path), logging.StreamHandler()]
)

logger = logging.getLogger(__name__)  # Exports logger object [web:3]
