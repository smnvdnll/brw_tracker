from loguru import logger

logger.remove()
logger.add(
    sink=lambda msg: print(msg, end=""),
    level="TRACE",
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{file.name}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>"
)

logger.add(
    "logs/logs.log",
    level="TRACE"
    # rotation="5 MB",
    # compression="zip"
)