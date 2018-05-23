'''
Test interface to the gerber_daemon module
'''

import logging
import traceback
import argparse
from src.gerber_daemon import gerber_daemon

'''
    Sets up argparser
'''
parser = argparse.ArgumentParser(description="CLI for working with gerber files.")
parser.add_argument('directory', help="Directory containing the gerber files you'll work with.")
parser.add_argument("-f", "--format", help="Gerber folder structure format, specific to the software used to export the gerber files. Is either eagle, kicad, ...")
parser.add_argument('-v', '--verbose', help="Changes logging level to the most output possible", action="store_true")


'''
    Main entry point
'''
if __name__ == "__main__":
    # get args
    args = parser.parse_args()

    '''
        Sets up logging for the module
    '''
    # Create logger
    logger = logging.getLogger("gerber_parsing") 
    # create file handle
    fh = logging.FileHandler("debug.log")  
    # console handler
    ch = logging.StreamHandler()
    # Set levels based on verbosity setting
    if args.verbose:
        logger.setLevel(logging.INFO)
        fh.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.CRITICAL)
        fh.setLevel(logging.CRITICAL)
        ch.setLevel(logging.CRITICAL)
    # Create formatter, add top handles
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add handles to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    '''
        Main entry point into submodules
    '''
    # Info log
    logger.info("Main entry in test file")
    try:
        logger.info("Creating an instance of gerber_daemon")
        daemon = gerber_daemon(args.directory, args.format)
        logger.info("Starting a render dump of the loaded files")
        daemon.output_dump()
    except ValueError, e:
        logger.error(e)
    except:
        logger.error( traceback.format_exc() )
