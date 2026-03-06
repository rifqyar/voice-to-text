import os
from dotenv import load_dotenv

load_dotenv()

MAX_GPU_PROCESSES = int(os.getenv("MAX_GPU_PROCESSES", 12))
MODEL_SIZE = os.getenv("MODEL_SIZE", "small")
DEVICE = os.getenv("DEVICE", "cuda")
COMPUTE_TYPE = os.getenv("COMPUTE_TYPE", "float16")