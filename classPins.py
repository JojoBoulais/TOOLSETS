import nuke
import nuke.splinewarp as sw


def main():

    getSplineWarpNode()
    node, curve, root = getSplineWarpNode()

    validateLayers(curve)
    validateSource, validateDest = validateLayers(curve)

    if validateSource == None and validateDest == None:
        sourceL, destL = createLayers(curve, root)
        classSource(curve, sourceL)
        classDest(curve, destL)


    else:
        getSplineWarpNode()
        node, curve, root = getSplineWarpNode()
        sourceL, destL = getLayers(curve)
        s = getNewSourceindex(curve)
        classNewSource(curve, s, sourceL)
        d = getNewDestindex(curve)
        classNewDest(curve, d, destL)



def getSplineWarpNode():
    node = nuke.thisNode()
    curve = node['curves']
    root = curve.rootLayer
    return node, curve, root


def validateLayers(curve):
    validateSource = curve.toElement('Source')
    validateDest = curve.toElement('Dest')
    return validateSource, validateDest


def createLayers(curve, root):
    sourceL = sw.Layer(curve)
    root.append(sourceL)
    sourceL.name = 'Source'
    sourceL.locked = True
    destL = sw.Layer(curve)
    root.append(destL)
    destL.name = 'Dest'
    return sourceL, destL


def getLayers(curve):
    sourceL = curve.toElement('Source')
    destL = curve.toElement('Dest')
    return sourceL, destL


def classSource(curve, sourceL):


    for n in range(1, 999, 1):
        for i in range(2,100,2):
            pin = curve.toElement('Pin' + str(i))
            if pin == None:
                break
            else:
                pin.name = 'Source' + str(n)
                sourceL.append(pin)
                del pin


def getNewSourceindex(curve):


    for s in range(1, 999, 1):
        pinCheck = curve.toElement('Source.Source{0}'.format(s+1))
        if pinCheck == None:
            break
    return s


def classNewSource(curve, s, sourceL):


     for SS in (s, 999, 1):
         for S in range(2, 998, 2):
            pin = curve.toElement('Pin' + str(S))
            if pin == None:
                break
            else:
                pin.name = 'Source' + str(SS + 1)
                sourceL.append(pin)
                del pin


def classDest(curve, destL):


    for n in range(1, 999, 1):
        for i in range(1, 101, 2):
            pin = curve.toElement('Pin' + str(i))
            if pin == None:
                break
            else:
                pin.name = 'Dest' + str(n)
                destL.append(pin)
                del pin


def getNewDestindex(curve):


    for d in range(1, 999, 1):
        pinCheck = curve.toElement('Dest.Dest{0}'.format(d+1))
        if pinCheck == None:
            break
    return d


def classNewDest(curve, d, destL):


     for DD in range(d, 100, 1):
        for D in range(1, 999, 2):
            pin = curve.toElement('Pin' + str(D))
            if pin == None:
                break
            else:
                pin.name = 'Dest' + str(DD + 1)
                destL.append(pin)
                del pin

