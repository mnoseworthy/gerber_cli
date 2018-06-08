'''
This class implements classes to create svg graphic elements from an ipcd365 file

-Initial brainstorm of how to do this:
    - Parse an ipcd365 and create objects representing the various graphics.
    - IPC files are 80 coloumns wide, the first 3 coloumns identify the feature, identify a feature then create an object
    with that feature
    - IPC graphics will identify features based on the 
'''

class ipc_graphics:

    def __init__(self, directory, filename):
        '''
        Load files using Matt's code?? Need to meet up and understand what has been done.
        Assume the ipc.d365 has been placed into a
        :param directory:
        :param filename:
        '''

class via(self, line)

coloumn_data = {
    'C1-3'  :   {
        "317"   : "Thru Hole"       ,
        "327"   : "SMD Feature"     ,
        "367"   : "Non Plated Hole" ,
        "370"   : "In Board Passive",
        "380"   : "On Board Passive",
    }
}