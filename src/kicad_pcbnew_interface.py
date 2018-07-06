"""
    It turns out that kicad has python bindings for their codebase, that are abstracted
    to the point where they're immediately useful for gathering the data we need to parse
    from the kicad design files.

    This file will be a unit test of those features.


    Resources:

    Kicad Installation guide, Must compile from sources to get python bindings:
    https://kicad.mmccoo.com/2017/02/01/compiling-kicad-on-ubuntu/

    Various tutorials for using the python bindings:
    https://forum.kicad.info/t/tutorials-on-python-scripting-in-pcbnew/5333

    Notes:
    - Building required you to go off and manually build a few outside packages, as well as
    manually install the python libraries into the system ( we need to containerize this )
    - The use-case of these bindings is to create plugins within kicad, and they provide their
    own python console that they expect the code to run in. We'll need to emulate that environment:
        - Modules loaded into environment:
            ['heapq', 'code', 'wx.py.pprint', 'functools', 'wx.py', 'sysconfig', 'wx._gdi', 'pcbnew', 'wx.py.__builtin__', 'wx.types', 'wx.py.document', 'imp', 'collections', 'wx.codecs', 'wxversion', 'wx.py.imp', 'zipimport', 'wx.py.sys', 'string', 'sdip_wizard', 'wx._misc_', 'wx.py.dispatcher', 'encodings.utf_8', 'wx.py.commands', 'bga_wizard', 'wx.py.inspect', 'wx.py.__main__', 'wx.py.weakref', 'wx.stc', 'wx.wx', 'signal', 'FPC_(SMD_type)_footprintwizard', 'pprint', 'qfp_wizard', 'token', 'touch_slider_wizard', 'wx.py.tokenize', 'wx.py.types', 'dis', 'cStringIO', 'uss39_barcode', 'locale', 'wx._stc', 'atexit', 'encodings.encodings', 'wx.__version__', 'encodings', 'wx.py.crust', 'wx.py.glob', 'abc', 'wx.py.magic', 'wx.py.code', 're', 'new', 'FootprintWizardDrawingAids', 'math', 'UserDict', 'swig_runtime_data2', 'inspect', 'swig_runtime_data4', 'exceptions', 'codecs', 'wx._windows', 'wx.py.time', '_sysconfigdata_nd', 'wx', '_functools', '_locale', 'wx.sys', 'wx.py.version', 'traceback', 'wx.py.wx', 'weakref', 'itertools', 'opcode', 'wx.py.cStringIO', 'wx.py.frame', 'os', '__future__', '_collections', '_sre', 'wx.py.parse', '__builtin__', 'wx.py.exceptions', 'wx.locale', 'operator', 'PadArray', '_heapq', 'wx._core', 'posixpath', 'errno', 'wx._controls', 'sre_constants', 'wx.py.images', 'wx.py.crustslices', 'os.path', 'tokenize', '_warnings', 'wx.py.filling', 'encodings.__builtin__', '_codecs', 'wx.atexit', 'commands', 'wx.py.interpreter', 'wx.py.shell', 'zip_wizard', '_sysconfigdata', 'thread', 'keyword', 'wx._windows_', 'wx.py.sliceshell', 'wx.py.re', 'posix', 'encodings.aliases', 'fnmatch', 'sre_parse', 'wx.py.editor', 'copy_reg', 'sre_compile', 'site', 'wx.py.path', 'wx._gdi_', '__main__', 'strop', 'linecache', 'encodings.codecs', 'circular_pad_array_wizard', '_abcoll', 'wx._controls_', 'wx.os', 'wx._misc', 'genericpath', 'stat', '_pcbnew', 'warnings', 'glob', 'wx.py.pseudo', 'wx.new', 'sys', 'codeop', 'types', 'wx.py.keyword', 'sitecustomize', 'HelpfulFootprintWizardPlugin', 'wx.py.os', '_weakref', 'wx.py.introspect', 'wx._core_', '_weakrefset', 'wx.warnings', 'wx.py.editwindow', 'time', 'wx.py.buffer']
        - environment loader located at:
        
"""



"""
Code to generate SVG's from the boardfile:
https://raw.githubusercontent.com/mmccoo/kicad_mmccoo/master/gensvg/gensvg.py
"""
# Copyright [2017] [Miles McCoo]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# this script is a basic svg generator for pcbnew.
# the point of the script is more as a teaching tool
# there are a number of ways in which is is deficient.

"""
    I've made the following modifications to his demo code:
    1) We're loading outside of a running pcbnew instance, so we manually load in the board file
    2) Instead of saving the SVG, we're returning it so we can use it elsewhere.
    3) Wrapped everything in a function so we can import into further test code. The function
    returns a tuple of whatever data is needed from the board or w/e
    4) Added a function to convert from svg -> png for opencv compatability
"""


import pcbnew
import sys, os
import svgwrite
import subprocess

# if you get the error: importError: No module named svgwrite
#    you need to do "pip install svgwrite" in an xterm

def convert_with_inkscape(args):
    try:
        inkscape_path = subprocess.check_output(["which", "inkscape"]).strip()
    except subprocess.CalledProcessError:
        print("ERROR: You need inkscape installed to use this script.")
        exit(1)

    export_width, export_height = args['size'].split('x')

    args = [
        inkscape_path,
        "--without-gui",
        "-f", args['file'],
        #"--export-area-page",
        "--export-area-drawing",
        #"-w", export_width,
        #"-h", export_height,
        "--export-background-opacity=0",
        "--export-png=" + args['out']
    ]
    print(args)
    subprocess.check_call(args)


def test_output(filepath):

    padshapes = {
        pcbnew.PAD_SHAPE_CIRCLE:  "PAD_SHAPE_CIRCLE",
        pcbnew.PAD_SHAPE_OVAL:    "PAD_SHAPE_OVAL",
        pcbnew.PAD_SHAPE_RECT:    "PAD_SHAPE_RECT",
        pcbnew.PAD_SHAPE_TRAPEZOID: "PAD_SHAPE_TRAPEZOID"    
    }
    # new in the most recent kicad code
    if hasattr(pcbnew, 'PAD_SHAPE_ROUNDRECT'):
        padshapes[pcbnew.PAD_SHAPE_ROUNDRECT] = "PAD_SHAPE_ROUNDRECT",


    board = pcbnew.BOARD()
    board = pcbnew.LoadBoard(filepath)


    boardbbox = board.ComputeBoundingBox()
    boardxl = boardbbox.GetX()
    boardyl = boardbbox.GetY()
    boardwidth = boardbbox.GetWidth()
    boardheight = boardbbox.GetHeight()

    # coordinate space of kicad_pcb is in mm. At the beginning of
    # https://en.wikibooks.org/wiki/Kicad/file_formats#Board_File_Format
    # "All physical units are in mils (1/1000th inch) unless otherwise noted."
    # then later in historical notes, it says,
    # As of 2013, the PCBnew application creates ".kicad_pcb" files that begin with
    # "(kicad_pcb (version 3)". All distances are in millimeters. 

    # the internal coorinate space of pcbnew is 10E-6 mm. (a millionth of a mm)
    # the coordinate 121550000 corresponds to 121.550000 

    SCALE = 1000000.0




    print("working in the dir " + os.getcwd())
    name = "output.svg"
    # A4 is approximately 21x29
    dwg = svgwrite.Drawing(name, size=('21cm', '29cm'), profile='full', debug=True)

    dwg.viewbox(width=boardwidth, height=boardheight, minx=boardxl, miny=boardyl)
    #background = dwg.add(dwg.g(id='bg', stroke='white'))
    #background.add(dwg.rect(insert=(boardxl, boardyl), size=(boardwidth, boardheight), fill='white'))



    svglayers = {}
    colors = board.Colors()
    for layerid in range(pcbnew.PCB_LAYER_ID_COUNT):
        c4 = colors.GetLayerColor(layerid);
        colorrgb = "rgb({:d}, {:d}, {:d})".format(int(round(c4.r*255)),
                                                int(round(c4.g*255)),
                                                int(round(c4.b*255)));
        layer = dwg.add(dwg.g(id='layer_'+str(layerid), stroke=colorrgb, stroke_linecap="round"))
        svglayers[layerid] = layer

    alltracks = board.GetTracks() 
    for track in alltracks:
        # print("{}->{}".format(track.GetStart(), track.GetEnd()))
        # print("{},{}->{},{} width {} layer {}".format(track.GetStart().x/SCALE, track.GetStart().y/SCALE,
        #                                               track.GetEnd().x/SCALE,   track.GetEnd().y/SCALE,
        #                                               track.GetWidth()/SCALE,
        #                                               track.GetLayer())          
        # )
        svglayers[track.GetLayer()].add(dwg.line(start=(track.GetStart().x,
                                                        track.GetStart().y),
                                                end=(track.GetEnd().x,
                                                    track.GetEnd().y),
                                                stroke_width=track.GetWidth()
        ))


    svgpads = dwg.add(dwg.g(id='pads', stroke='red',fill='orange'))
    allpads = board.GetPads()

    for pad in allpads:
        mod = pad.GetParent()
        name = pad.GetPadName()
        if (0):
            print("pad {}({}) on {}({}) at {},{} shape {} size {},{}"
                .format(name,
                        pad.GetNet().GetNetname(),
                        mod.GetReference(),
                        mod.GetValue(),
                        pad.GetPosition().x, pad.GetPosition().y,
                        padshapes[pad.GetShape()],
                        pad.GetSize().x, pad.GetSize().y
                ))
        if (pad.GetShape() == pcbnew.PAD_SHAPE_RECT):
            if ((pad.GetOrientationDegrees()==270) | (pad.GetOrientationDegrees()==90)):
                svgpads.add(dwg.rect(insert=(pad.GetPosition().x-pad.GetSize().x/2,
                                            pad.GetPosition().y-pad.GetSize().y/2),
                                    size=(pad.GetSize().y, pad.GetSize().x)))
            else:
                svgpads.add(dwg.rect(insert=(pad.GetPosition().x-pad.GetSize().x/2,
                                            pad.GetPosition().y-pad.GetSize().y/2),
                                    size=(pad.GetSize().x, pad.GetSize().y)))
        elif (pad.GetShape() == pcbnew.PAD_SHAPE_CIRCLE):
            svgpads.add(dwg.circle(center=(pad.GetPosition().x, pad.GetPosition().y),
                                r=pad.GetSize().x))
        elif (pad.GetShape() == pcbnew.PAD_SHAPE_OVAL):
            svgpads.add(dwg.ellipse(center=(pad.GetPosition().x, pad.GetPosition().y),
                                    r=(pad.GetSize().x/2, pad.GetSize().y/2)))
        else:
            print("unknown pad shape {}({})".format(pad.GetShape(), padshapes[pad.GetShape()]))

    # save and convert the SVG
    dwg.save()
    args = {
        'file' : "./output.svg",
        'out' : "./output.png",
        'size' : "800x800"
    }
    convert_with_inkscape(args)
    # Aggregate required  data and return
    dwg.save()
    return {
        'boardbox' : boardbbox,
        'boardxl' : boardxl,
        'boardyl' : boardyl,
        'boardwidth' : boardwidth,
        'boardheight' : boardheight,
        'svg' : 'output.png'
    }


if __name__ == "__main__":
    test_output("/home/matt/Desktop/projects/Ganglion_Hardware_Design_Files/Ganglion_KiCad_Files/Ganglion_01.kicad_pcb")


   

