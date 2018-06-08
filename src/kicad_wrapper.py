
'''
This file will contain all the object definitions required to process a kicad file
for the information we're going to need to generate an AR overlay in combination
with the gerber files.

Structure:
*This will almost 100% change as we learn more*

gerber_wrapper - class to handle interations with the actual file, and high level operations
    on the full set, or subsets of component objects.
component_objects
    -> Super class, defines any standard attributes/methods required for all different component types
    -> subclass, each component type ( net resistor whatever) will get its own data type as a subclass of the
     component object class

'''
import os
import re

class kicad_wrapper(object):

    def __init__(self, filepath):

        # Validate and store file
        if os.path.isfile(filepath):
            self.filepath = filepath
            self.filename = ntpath.basename(filepath)
        else:
            raise ValueError("gerber_wrapper: filepath doesn't point to a valid file")

        # Define any required attributes
        self.lines = [] # Array of lines from the file
        self.line_index = 0 # Place in iteration in file, if required, could also be a window index
        self.object_map = {
            "Object tag of some sort" : Object # Reference to the object
        }

        # Kick off control flow
        self.lines = self.readFile()

    def readFile(self):
        '''
            For now, as this is a human readable file we will simply read the file into
            an array of lines and iterate over them to ge the information we need
        '''
        with open(self.filepath) as kidcad_file:
            return kicad_file.read().split(',')


    # Define other high level methods required for processing, for example, the function
    # to iterate over the lines and build the required objects for each section
    def parse_components(self):
        # Define mapping between regex and object type, if this is how we're going to deteremine
        # The type of object to build ( regex is fairly robust )
        regex_map = {
            'Regular expression' : "object type that should be build from this line or set of lines"
            '(module'            : "create a new component"
            '(descr'             : "Descriptiuon of the module, "
            '(fp_text reference' : "Conponent annotation"
            '(fp_text value'     : "Component Value"    #This cpould have many meaning: eg 10pF or Conn02x24
            '(fp_line'           : "Lines which could be a useful fiducial"
            '(pad'               : "A pad is being defined"
            '(at'                : "Location of feature"
            '(segment'           : "Trace"
            '(via'               : "Via"
            '(gr_line'           : "Graphics line that has been explicitly drawn"
            '(gr_circle'         : "Graphics circle"
            '(gr_text'           : "Graphics text"
            '(layers'            : "Lists layers relevant to a feature"
            '(start'             : "Start of a feature"
            '(end'               : "End of a feature"
        }
        # Iterate over lines in file
        for line in lines:
            # Iterate over all the regular expressions in our map
            for regex, object_type in regex_map.iteritems():
                # Check for regex match
                if re.match(regex, line):
                    # Build the new object and store into the object map
                    self.object_map["tag for this instance"] = new object_type



class component_object(object, KiCADObj, Ref):
    # super constructor
    def __init__(self):
        # Define whatever attributes every object will require
        self.location = [0,0]
        self.units = 'mm'

     def find_Annotate(self, Ref):
         line = KiCADObj.lines(Ref)
         annotatipon = []
         for i in len(line):
            if line[i+22] == ' '
                break
            annotation.append(line[i+22])
         return str(annotation)

    # Define whatever methods everything will need
    def aMethod(self):
        x = "dostuff"
        return x

class resistor(component_object):
    def __init__(self):
        # Pass refernece to this object to the super class constructor
        component_object.__init__(self)
        # Define whatever attributes this class will need
        self.resistance = 6000
    
    # Define your methods
    def aCoolerMethod(self):
        y = "do cooler stuff"
        return y


# To test the code, execute this file and the block below will run
# there you can create an object of the wrapper class and start the
# program control flow
if __name__ == "__main__":
    wrapper = new gerber_wrapper()
    wrapper.serial_parse() # Or whatever method you need to 