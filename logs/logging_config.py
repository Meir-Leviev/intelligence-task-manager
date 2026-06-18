import logging

def config_logging():
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logging.basicConfig(level=logging.INFO,
                         handlers=[file_handler, stream_handler])