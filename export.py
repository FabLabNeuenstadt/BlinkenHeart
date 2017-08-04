import os
from pcbnew import * 
from subprocess import call
from time import sleep

dirPath = os.path.dirname(os.path.realpath(__file__))
#Make everything more reliable
call("cd " + dirPath, shell=True)

#Clean the enviroment(Just in case)
call("rm -rf export/*", shell=True)
call(["rm", "export.zip"])

#Source for this part of the code: https://gist.github.com/spuder/4a76e42f058ef7b467d9#file-plot_board-py-L69
board = LoadBoard("BlinkenHeart.kicad_pcb")

pctl = PLOT_CONTROLLER(board)

popt = pctl.GetPlotOptions()

popt.SetOutputDirectory("export/")

# Set some important plot options:
popt.SetPlotFrameRef(False)
popt.SetLineWidth(FromMM(0.1))

popt.SetAutoScale(False)
popt.SetScale(1)
popt.SetMirror(False)
popt.SetUseGerberAttributes(True)
popt.SetExcludeEdgeLayer(False)
popt.SetScale(1)
popt.SetUseAuxOrigin(True)
popt.SetSubtractMaskFromSilk(False)
popt.SetUseGerberProtelExtensions(True)

plot_plan = [
    ( "F.Cu", F_Cu, "Top layer" ),
    ( "B.Cu", B_Cu, "Bottom layer" ),
    ( "F.Silk", F_SilkS, "Silk top" ),
    ( "B.Silk", B_SilkS, "Silk bottom" ),
    ( "F.Mask", F_Mask, "Mask top" ),
    ( "B.Mask", B_Mask, "Mask bottom" ),
    ( "EdgeCuts", Edge_Cuts, "Edges" ),
]

for layer_info in plot_plan:
    pctl.SetLayer(layer_info[1])
    #Make the Edge Cuts dirty pcb comaptible
    if layer_info[0] == "EdgeCuts":
        popt.SetUseGerberProtelExtensions(False)
        pctl.OpenPlotfile(layer_info[0], PLOT_FORMAT_GERBER, layer_info[2])
        popt.SetUseGerberProtelExtensions(True)
    else:
        pctl.OpenPlotfile(layer_info[0], PLOT_FORMAT_GERBER, layer_info[2])
    pctl.PlotLayer()

pctl.ClosePlot()

#Zip everything
call("zip -j export.zip export/*", shell=True) 
