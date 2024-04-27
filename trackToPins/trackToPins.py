import nuke
import nuke.rotopaint as rp, _curvelib as cl
import copy

def getNodes():
    nodes = {}
    sNodes = nuke.selectedNodes()

    for node in sNodes:
        if node.Class() == 'SplineWarp3':
            nodes["splinewarp"] = node
        elif node.Class() == 'Tracker4':
            nodes["tracker"] = node
        else:
            pass

    return nodes


def getTrackNum(nodes):


    for i in range(1, 1000):
        check = nuke.tcl("value {0}.tracks.{1}.track_x".format(nodes["tracker"].name(), i))
        if check == '1':
            break



    trackerstr = nodes['tracker']["tracks"].toScript()
    trackers = int(trackerstr.count("track"))

    return i -1


def createPins(curve, PinPairs, stabilize):

    shape1 = rp.Shape(curve)
    vec1 = rp.CVec4()
    shape1.append(vec1)

    shape2 = rp.Shape(curve)
    vec2 = rp.CVec4()
    shape2.append(vec2)

    PinPair = []
    PinPair.append(shape1)
    PinPair.append(shape2)

    if stabilize == "stabilize":
        PinPair.reverse()


    curve.defaultJoin(shape1, shape2)

    PinPairs.append(PinPair)

def animatePins(track, nodes, pinPairs,fRange, refFrame, parameters):
    transX = cl.AnimCurve()
    transY = cl.AnimCurve()
    transXSource = cl.AnimCurve()
    transYsource = cl.AnimCurve()


    transX.expressionString = '{0}.tracks.{1}.track_x'.format(nodes["tracker"].name(), track)
    transY.expressionString = '{0}.tracks.{1}.track_y'.format(nodes["tracker"].name(), track)
    transX.useExpression = True
    transY.useExpression = True


    transXSource.expressionString = '{0}.tracks.{1}.track_x({2})'.format(nodes["tracker"].name(), track, refFrame)
    transYsource.expressionString = '{0}.tracks.{1}.track_y({2})'.format(nodes["tracker"].name(), track,refFrame)
    transXSource.useExpression = True
    transYsource.useExpression = True


    for f in range(int(fRange[0]), int(fRange[1])):
        transX.addKey(f, transX.evaluate(f))
        transY.addKey(f, transY.evaluate(f))

    for f in range(int(fRange[0]), int(fRange[1])):
        transXSource.addKey(f, transXSource.evaluate(f))
        transYsource.addKey(f, transYsource.evaluate(f))


    ### DEST PIN
    transformDest = pinPairs[track-1][1].getTransform()
    transformDest.setTranslationAnimCurve(0, transX)
    transformDest.setTranslationAnimCurve(1, transY)


    ### SOURCE PIN

    transformSource = pinPairs[track-1][0].getTransform()
    transformSource.setTranslationAnimCurve(0, transXSource)
    transformSource.setTranslationAnimCurve(1, transYsource)


    if parameters == "Bake":
        #BAKE
        transformDest.getTranslationAnimCurve(0).expressionString = 'curve'
        transformDest.getTranslationAnimCurve(1).expressionString = 'curve'

        transformSource.getTranslationAnimCurve(0).expressionString = 'curve'
        transformSource.getTranslationAnimCurve(1).expressionString = 'curve'

def panel(nodes, fFrame, lFrame):


    panel = nuke.Panel('Track to Pin')

    panel.addEnumerationPulldown('track/stabilize', 'track stabilize')
    panel.addEnumerationPulldown('Parameters', '"Bake" "Link(to trackers)"')
    panel.addSingleLineInput('Reference Frame', int(nodes["tracker"]['reference_frame'].value()))
    panel.addSingleLineInput('Range', str(fFrame) + "-" + str(lFrame))

    return panel

def main():

    nodes = getNodes()


    #### VERIFY WICH NODES EXIST ####

    try:
        nodes["tracker"]
    except:
        return
    else:
        pass

        ##### SET VARIABLES ###

    root = nuke.root()


    fFrame = int(root["first_frame"].value())
    lFrame = int(root["last_frame"].value())

    p = panel(nodes, fFrame, lFrame)

    if p.show() == 0:
        return

    fRange = p.value("Range")
    fRange = fRange.split("-")


    xpos = nodes['tracker']["xpos"].value()
    ypos = nodes['tracker']["ypos"].value()

    ### CHECK IF THERE IS AN ACTUAL FRAMERANGE
    try:
        fRange[1]
    except:
        return
    else:
        pass

    ### GET VALUE FROM PANEL

    refFrame = p.value("Reference Frame")
    stabilize = p.value("track/stabilize")
    parameters = p.value("Parameters")

    # GET NUMBERS OF TRACKS

    trackers = getTrackNum(nodes)

    if trackers == 0:
        return

    #create splinewarp if doesn't exist

    try:
        nodes["splinewarp"]
    except:
        nodes["splinewarp"] = nuke.createNode("SplineWarp3")
        nodes["splinewarp"].setInput(0, None)
        nodes["splinewarp"]["xpos"].setValue(xpos)
        nodes["splinewarp"]["ypos"].setValue(ypos + 100)
    else:
        pass

    curve = nodes["splinewarp"]["curves"]
    ###### CREATE PINS ####

    pinPairs = []


    for track in range(1, trackers+1):
        createPins(curve, pinPairs, stabilize)
        animatePins(track, nodes, pinPairs,fRange, refFrame, parameters)



### LUNCH ###

main()
