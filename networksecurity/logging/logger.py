# # import logging
# # import os
# # from datetime import datetime

# # LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# # log_path=os.path.join(os.getcwd(),"logs")
# # os.makedirs(log_path,exist_ok=True)

# # LOG_FILE_PATH=os.path.join(log_path,LOG_FILE)

# # logging.basicConfig(
# #     filename=LOG_FILE_PATH,
# #     format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
# #     level=logging.INFO,
# #     handlers=[
# #         logging.FileHandler(log_path),
# #         logging.StreamHandler()
# #     ]
# # )

# # logger=logging.getLogger(__name__)


# import logging
# import os
# from datetime import datetime
# from pathlib import Path  # Use absolute paths

# # FIXED: Use project root for logs (go up 2 levels from logger.py)
# BASE_DIR = Path(__file__).parent.parent  # networksecurity/
# logs_dir = BASE_DIR / "logs"
# logs_dir.mkdir(exist_ok=True)  # Create once [web:11][web:51]

# log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
# log_path = logs_dir / log_file

# # Simple single handler (no PermissionError)
# logging.basicConfig(
#     level=logging.INFO,
#     format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
#     handlers=[logging.FileHandler(log_path), logging.StreamHandler()]
# )

# logger = logging.getLogger(__name__)
