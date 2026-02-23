from dotenv import load_dotenv
import os

load_dotenv()

CONFIG = {
    "project_name": os.getenv("PROJECT_NAME", "OperatorOS"),
    "version": os.getenv("VERSION", "0.1"),
}
