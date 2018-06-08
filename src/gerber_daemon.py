'''
This file implements classes to handle loading in a set of gerber files

Initial control flow brainstorm:

 - User creates an instance of the gerber daemon class
 - Give a directory containing gerber files
 - Parse filenames to determine which files are useful to us
 - Each useful file gets passed to a gerber wrapper class which triggers a set of operations:
    - Detect useful features from the file and wrap them
    - Generate and store the bit-image described by the file
 - The daemon holds references to each gerber object and provides an API to the gerber class with abstractions
 made for selecting the various files
 

The daemon class
    - Constructor accepts a directory pointer
    - On initialization, will parse filenames (and file headers?) to determine which files are useful
    - For each useful file, create a gerber object and store the reference in an attribute dict
    - Implement API to access operations from the gerber class

The gerber_wrapper class:
    - Will implement any operations required on a gerber file
        - output the bit-image in various formats
        - Removing/adding features
        - Highlighting/modifying existing features
'''
import os
import logging
from src.gerber_wrapper import gerber_wrapper

class gerber_daemon:

    def __init__(self, file_directory, gerber_format):
        '''
            @param file_directory(string) - a valid filepath containing gerber files
            @param gerber_format(string) - One of the supported gerber output formats, likely
                one of either (eagle|orcad|protel|kicad)
        '''

        # Create logger
        self.logger = logging.getLogger("gerber_parsing.gerber_daemon")

        # Validate directory and store reference
        if os.path.exists( os.path.dirname(file_directory) ):
            self.file_directory = os.path.dirname(file_directory)
        else:
            raise ValueError("gerber_daemon: Given directory {} is invalid".format(file_directory))

        # Validate gerber_format and store reference
        if gerber_format in file_extensions:
            self.gerber_format = gerber_format
        else:
            raise ValueError("gerber_daemon: Given gerber format {} is not supported.".format(gerber_format))

        # Define required attributes
        # file pointers to the original ( filtered ) list of gerbers, mapped to the expected files
        self.gerber_files = {
            "top_copper"        : None,
            "bottom_copper"     : None, 
            "top_soldermask"    : None, 
            "bottom_soldermask" : None,
            "top_silkscreen"    : None,
            "bottom_silkscreen" : None,
            "nc_drill"          : None
        }  
        # Files that were filtered out
        self.rejected_files = [] 
        # map of gerber objects, {key=(Index schema) : value=Object(Gerber Class)}
        self.gerber_map = {}    

        # Filter files
        self.filter_files()
        # Create map w/ wrapper instances
        self.create_gerber_map()
    
    def filter_files(self):
        '''
            Gets a file blob from self.file_directory, iterates the files and stores useful
            ones into self.gerber_files
        '''
        # Log start of function
        self.logger.info("Filtering files")
        # Store extension map locally for easier access
        extensions = file_extensions[self.gerber_format]
        # Iterate over files
        for filename in os.listdir(self.file_directory):
            # Flags
            rejected = True
            # Iterate over extensions
            for extension in extensions:
                # if the current file has the current extension..
                if filename.endswith(extension):
                    # Store the filename under the resolved file type
                    self.gerber_files[extensions[extension]] = os.path.join(self.file_directory, filename)
                    rejected = False
            # If file was not found in lookup tables, store it into the rejected list
            if rejected:
                self.rejected_files.append(filename)
        # Report
        num_found = 0
        for key in self.gerber_files:
            if self.gerber_files[key] != None:
                num_found += 1
        self.logger.info("Found {} of the {} expected gerber files".format(num_found, len(self.gerber_files)))
        self.logger.info("Rejected {} files, which were {}".format(len(self.rejected_files), self.rejected_files))
    
    def create_gerber_map(self):
        '''
            Creates a gerber instance from each of the filtered files and adds them to self.gerber_map
        '''
        # Iterate over gerber file list
        for filetype, filepath in self.gerber_files.iteritems():
            
            # If the filepath was resolved...
            if filepath != None:
                try:
                    # Info log
                    self.logger.info("Creating wrapper for {}".format(filetype))
                    # Currently just use string filetype for map
                    # Create a wrapper instance for the gerber file and add to map
                    self.gerber_map[filetype] = gerber_wrapper(filepath)
                except Exception as e:
                    self.logger.error("Wrapper creation failed for {} with error: \n    {}".format(filetype, e))
                    pass

    def output_dump(self):
        '''
            Triggers an svg output from each of the held gerber_wrapper references
        '''     
        for filetype, wrapper in self.gerber_map.iteritems():
            self.logger.info("Rendering frame for {}".format(filetype))
            wrapper.render_frame()

'''
    Various maps // tables required for parsing
'''
# File extensions we're looking for based on the input format
file_extensions = {
    'eagle' : {
        ".cmp"  : "top_copper"        ,
        ".sol"  : "bottom_copper"     , 
        ".stc"  : "top_soldermask"    , 
        ".sts"  : "bottom_soldermask" ,
        ".plc"  : "top_silkscreen"    ,
        ".pls"  : "bottom_silkscreen" ,
        ".drd"  : "nc_drill"
    },
    'orcad' : {
        ".top"      : "top_copper"        , 
        ".bot"      : "bottom_copper"     ,
        ".smt"      : "top_soldermask"    ,
        ".smb"      : "bottom_soldermask" ,
        ".sst"      : "top_silkscreen"    ,
        ".ssb"      : "bottom_silkscreen" ,
        "nc_drill"  : "thruhole.tap"
    },
    'protel' : {
        ".gtl" : "top_copper"        ,
        ".gbl" : "bottom_copper"     ,
        ".gts" : "top_soldermask"    ,
        ".gbs" : "bottom_soldermask" ,
        ".gto" : "top_silkscreen"    ,
        ".gbo" : "bottom_silkscreen" ,
        ".drl" : "nc_drill"
    },
    'kicad' : {
        "-F_Cu.gbr"     : "top_copper"        ,
        "-B_Cu.gbr"     : "bottom_copper"     ,
        "-F_Mask.gbr"   : "top_soldermask"    ,
        "-B_Mask.gbr"   : "bottom_soldermask" ,
        "-F_SilkS.gbr"  : "top_silkscreen"    ,
        "-B_SilkS.gbr"  : "bottom_silkscreen" ,
        ".drl"          : "nc_drill"
    },
    'IPCD365' : {
        ".d365" :   "IPCD365"
    }
}
        