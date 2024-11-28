import logging

# Create General Logger-- includes error and http (which includes access)
general_logger = logging.getLogger("GeneralLogger")
general_logger.setLevel(logging.INFO)
general_handler = logging.FileHandler("general.log")
general_handler.setFormatter(logging.Formatter('%(asctime)s - GENERAL - %(levelname)s - %(message)s'))
general_logger.addHandler(general_handler)

# Create HTTP Logger-- includes access
http_logger = logging.getLogger("HTTPLogger")
http_logger.setLevel(logging.INFO)
http_handler = logging.FileHandler("http.log")
http_handler.setFormatter(logging.Formatter('%(asctime)s - HTTP - %(levelname)s - %(message)s'))
http_logger.addHandler(http_handler)
http_logger.addHandler(general_handler)

# Create Access Logger
access_logger = logging.getLogger("AccessLogger")
access_logger.setLevel(logging.INFO)
access_handler = logging.FileHandler("access.log")
access_handler.setFormatter(logging.Formatter('%(asctime)s - ACCESS - %(levelname)s - %(message)s'))
access_logger.addHandler(access_handler)
access_logger.addHandler(http_handler)
access_logger.addHandler(general_handler)


# Create Error Logger
error_logger = logging.getLogger("ErrorLogger")
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler("error.log")
error_handler.setFormatter(logging.Formatter('%(asctime)s - ERROR - %(levelname)s - %(message)s'))
error_logger.addHandler(error_handler)
error_logger.addHandler(general_handler)