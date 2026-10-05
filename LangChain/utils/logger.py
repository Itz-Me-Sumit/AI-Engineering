import logging

def get_logger(name:str = __name__):
    """ Creates and Returns logger object """
    logging.basicConfig(
        level = logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"        
    )

    return logging.getLogger(name)