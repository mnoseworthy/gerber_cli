

import os
import ntpath
import logging
import gerber
from gerber.render import GerberCairoContext, RenderSettings, theme

'''
    Class to wrap a gerber file and implement all the operations that we'll require with
    respect to the gerber files themselves
'''
class gerber_wrapper():

    def __init__(self, filepath):
        '''
            @param filepath(string) - path to the file this instance should wrap
        '''
        # Create logger
        self.logger = logging.getLogger("gerber_parsing.gerber_wrapper.{}".format(filepath))
        
        # Validate filepath
        if os.path.isfile(filepath):
            self.filepath = filepath
            self.filename = ntpath.basename(filepath)
        else:
            raise ValueError("gerber_wrapper: filepath doesn't point to a valid file")

        # create a render settings object
        self.settings = RenderSettings(color=theme.COLORS['white'], alpha=1)
        
    
    def render_frame(self):
        '''
            Renders the current gerber file, returns a pointer to an svg or something?
        '''
        # output filename
        output = "./{}.svg".format(self.filename)
        # Create gerber context
        ctx = GerberCairoContext()
        # Read file // load layer
        layer = gerber.load_layer(self.filepath)
        # Render
        ctx.render_layer(layer, settings=self.settings)
        # Output
        ctx.dump(output)
        return output