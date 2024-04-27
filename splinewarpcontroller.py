import nuke
import nuke.splinewarp as sp

def get_root_layers(root):
    """Will return layers present inside root layer in a roto ro splinewarp node.

    :param root: node['curves'].rootLayer
    :type root: rootLayer
    :return: list of layers
    :rtype: list
    """
    root_layers = []
    for element in root:
        if isinstance(element, sp.Layer):
            root_layers.append(element)

    return root_layers


def find_shape(layer, shape_name):
    """Will search for shape name's inside a given layer.

    :param layer: layer
    :type layer: nuke.splinewarp.Layer
    :param shape_name: name of shape
    :type shape_name: str
    :return: return True if shape name's has been found
    :rtype: Bool
    """
    for element in layer:
        if isinstance(element, sp.Shape) or isinstance(element, sp.Stroke):
            if element.name == shape_name:
                return True


def search_in_layers(layer, shape_name):
    """Will return layer's name + shape name in a str.

    :param layer: layer
    :type layer: nuke.splinewarp.Layer
    :param shape_name: shape name's we are searching
    :type shape_name: str
    :return: layer's name + shape's name.
    :rtype: str
    """
    for l in layer:
        if find_shape(l, shape_name):
            return l.name + "/" +shape_name


def full_shape_name(root, shape_name):
    """Will search if shape is inside a layer or not. If it is it will returns layer'sn ame + shape's name oterwise
    only shape's name.

    :param root: node root layer
    :type root: node['curves'].rootLayer
    :param shape_name: name of a selected shape
    :type shape_name: str
    :return:layer's name + shape's name or shape's name
    :rtype: str
    """
    searchs = {}
    i = 0
    if find_shape(root, shape_name):
        return shape_name
    full_qualified_name = search_in_layers(root, shape_name)
    return full_qualified_name


def exp_rotate(baseShapeName, refFrame):

    exp_rot = "[python -execlocal try:\\n\\ \\ \\ \\ math\\nexcept:\\n\\ \\ \\ \\ import\\ math\\n\\n\\nn\\ =\\" \
              " nuke.thisNode()\\ncurves\\ =\\ n\\[\'curves\'\\]\\n\\ns\\ =\\ curves.toElement(\\'{0}\\')" \
              "\\n\\n\\nrefy\\ =\\ \\[\\]\\nys\\ =\\ \\[\\]\\n\\nrefx\\ =\\ \\[\\]\\nxs\\ =\\ \\[\\]\\n\\nrots\\" \
              " =\\ \\[\\]\\n\\nfor\\ pt\\ in\\ s:\\n\\n\\ \\ \\ \\ animx\\ =\\ pt.getPositionAnimCurve(0)\\n\\ \\" \
              " \\ \\ animy\\ =\\ pt.getPositionAnimCurve(1)\\n\\ \\ \\ \\ \\n\\ \\ \\ \\ y1\\ =\\" \
              " animy.evaluate(nuke.frame())\\n\\ \\ \\ \\ y2\\ =\\ animy.evaluate({1})\\n\\ \\ \\ \\ \\n\\" \
              " \\ \\ \\ ys.append(y1)\\n\\ \\ \\ \\ refy.append(y2)\\n\\ \\ \\ \\ \\n\\ \\ \\ \\ \\n\\ \\ \\" \
              " \\ x1\\ =\\ animx.evaluate(nuke.frame())\\n\\ \\ \\ \\ x2\\ =\\ animx.evaluate({1})\\n\\ \\ \\ \\ " \
              "\\n\\ \\ \\ \\ xs.append(x1)\\n\\ \\ \\ \\ refx.append(x2)\\n\\ncenter\\ =\\ (sum(xs)/float(len(xs)),\\" \
              " sum(ys)/float(len(ys)))\\ncenterRef\\ =\\ (sum(refx)/float(len(refx)),\\" \
              " sum(refy)/float(len(refy)))\\n\\nx\\ =\\ xs\\[0\\]\\ -\\ center\\[0\\]\\ny\\ =\\ ys\\[0\\]\\" \
              " -\\ center\\[1\\]\\n\\n\\nrot\\ =\\ (math.atan2(y,x)*180/3.1415)\\n\\nxr\\ =\\ refx\\[0\\]\\" \
              " -\\ centerRef\\[0\\]\\nyr\\ =\\ refy\\[0\\]\\ -\\ centerRef\\[1\\]\\n\\n\\nrotRef\\ =\\" \
              " (math.atan2(yr,xr)*180/3.1415)\\n\\ \\ \\ \\ \\n\\ \\ \\ \\ \\nif\\ rot\\ >\\ 0\\ and\\" \
              " rotRef\\ >\\ 0\\ :\\n\\ \\ \\ \\ ret\\ =\\ rot\\ -\\ rotRef\\nelif\\ rot\\ <\\ 0\\ and\\" \
              " rotRef\\ >\\ 0:\\n\\ \\ \\ \\ ret\\ =\\ 360+rot\\ -\\ rotRef\\nelif\\ rot\\ <\\ 0\\ and\\ rotRef\\" \
              " <\\ 0:\\n\\ \\ \\ \\ ret\\ =\\ -1*rotRef\\ -\\ -1*rot\\nelif\\ rot\\ >\\ 0\\ and\\ rotRef\\ <\\" \
              " 0:\\n\\ \\ \\ \\ ret\\ =\\ (360\\ +\\ rotRef\\ -\\ rot)\\ *\\ -1\\n]".format(baseShapeName, refFrame)
    return exp_rot


def expX(baseShapeName, refFrame):
    """Generate expression for controller's x translate knob.

    :param baseShapeName: name of the source shape
    :type baseShapeName: str
    :param refFrame: Reference frame
    :type refFrame: int
    :return: generated expression
    :rtype: str
    """

    expx = "[python -execlocal n\\ =\\ nuke.thisNode()\\ncurves\\ =\\" \
           " n\\['curves'\\]\\nroot\\ =\\ curves.rootLayer\\nshape\\ =\\" \
           " curves.toElement('{0}')\\n\\nxAverage\\ =\\ 0.0\\ni\\ =\\" \
           " len(shape)\\n\\nfor\\ point\\ in\\ shape:\\n\\ \\ \\ \\ Animcurve\\" \
           " =\\ point.getPositionAnimCurve(0)\\n\\ \\ \\ \\ xAverage\\" \
           " +=\\ Animcurve.evaluate(nuke.frame())\\n\\nxAverage\\ =\\ xAverage/i\\n" \
           "\\nxrefFrameAverage\\ =\\ 0.0\\nfor\\ point\\ in\\ shape:\\n\\ \\ \\ \\" \
           " Animcurve\\ =\\ point.getPositionAnimCurve(0)\\n\\ \\ \\ \\ xrefFrameAverage\\" \
           " +=\\ Animcurve.evaluate({1})\\n\\nxrefFrameAverage\\ =\\ xrefFrameAverage/i\\n\\nret\\" \
           " =\\ xAverage\\ -\\ xrefFrameAverage]".format(baseShapeName, refFrame)

    return expx


def expY(baseShapeName, refFrame):
    """Generate expression for controller's y translate knob.

    :param baseShapeName: name of the source shape
    :type baseShapeName: str
    :param refFrame: Reference frame
    :type refFrame: int
    :return: generated expression
    :rtype: str
    """
    expy = "[python -execlocal n\\ =\\ nuke.thisNode()\\ncurves\\ =\\ n\\['curves'\\]\\nroot\\" \
           " =\\ curves.rootLayer\\nshape\\ =\\ curves.toElement('{0}')\\n\\nxAverage\\ =\\" \
           " 0.0\\ni\\ =\\ len(shape)\\n\\nfor\\ point\\ in\\ shape:\\n\\ \\ \\ \\ Animcurve\\" \
           " =\\ point.getPositionAnimCurve(1)\\n\\ \\ \\ \\ xAverage\\ +=\\" \
           " Animcurve.evaluate(nuke.frame())\\n\\nxAverage\\ =\\ xAverage/i\\n\\nxrefFrameAverage\\" \
           " =\\ 0.0\\nfor\\ point\\ in\\ shape:\\n\\ \\ \\ \\ Animcurve\\ =\\" \
           " point.getPositionAnimCurve(1)\\n\\ \\ \\ \\ xrefFrameAverage\\ +=\\" \
           " Animcurve.evaluate({1})\\n\\nxrefFrameAverage\\ =\\ xrefFrameAverage/i\\n\\nret\\" \
           " =\\ xAverage\\ -\\ xrefFrameAverage]".format(baseShapeName, refFrame)

    return expy


def remove_key_frame_add_one_key_frame(animCurve, ref_frame):
    """Remove all keys frame and set one key frame at ref frame for a given Anim curve.

    :param animCurve: Knob AnimCurve
    :type animCurve: AnimCurve
    :param ref_frame: reference frame
    :type ref_frame: int
    """

    xvalue = animCurve.evaluate(ref_frame)
    animCurve.removeAllKeys()
    animCurve.addKey(ref_frame, xvalue)


def add_key_frame_from_base_shape(base_shape, controller, ref_frame):

    for i, pt in enumerate(controller, -1):
        pt.addPositionKey(ref_frame, base_shape[i].getPosition(ref_frame))


def clear_controller(controller, ref_frame, node_name, base_shape, fullControllerShapeName):
    """Remove key frame for controller shape points.

    :param controller: controller shape
    :type controller: _curveknob.Stroke instance
    :param ref_frame: reference frame
    :type ref_frame: int
    """
    for point in controller:

        point.removeAllKeys()

        fullControllerShapeNamer = fullControllerShapeName.replace("/", ".")
        nuke.tcl('animation {0}.curves.{1} erase_all 0'.format(node_name, fullControllerShapeNamer))

        #add_key_frame_from_base_shape(base_shape, controller, ref_frame)

def animate_controller_shape(controller, expX, expY):
    """Animate controller shape's translate knob based on an average of every point from source shape.

    :param controller: controller shape
    :type controller: _curveknob.Stroke instance
    :param expX: expression of all source shape's point animation average. (x)
    :type expX: str
    :param expY: expression of all source shape's point animation average. (y)
    :type expY:str
    """
    transform = controller.getTransform()
    AnimCurveX = transform.getTranslationAnimCurve(0)
    AnimCurveX.expressionString = expX
    AnimCurveX.useExpression = True

    AnimCurveY = transform.getTranslationAnimCurve(1)
    AnimCurveY.expressionString = expY
    AnimCurveY.useExpression = True


def rotate_controller_shape(controller, expRotate):
    transform = controller.getTransform()
    ranim = transform.getRotationAnimCurve(2)
    ranim.expressionString = expRotate
    ranim.useExpression = True


def createControllerShape(base_shape, baseShapeName):
    """Create controller shape based on source shape.

    :param base_shape: source shape
    :type base_shape: _curveknob.Stroke
    :param controllerNum: index of the controller
    :type controllerNum: int
    :param baseShapeName: name of controller shape is based on
    :type baseShapeName: str
    :return: controller shape
    :rtype: _curveknob.Stroke instance
    """
    controller = base_shape.clone()
    controller.name = 'controller({0})'.format(baseShapeName)
    return controller


def create_destination_shape(base_shape, baseShapeName):
    """Create Destination shape

    :param base_shape: source shape
    :type base_shape: _curveknob.Stroke instance
    :param baseShapeName: name of destination shape is based on
    :type baseShapeName: str
    :return: destination shape
    :rtype: _curveknob.Stroke instance
    """

    output_shape = base_shape.clone()
    output_shape.name = 'destination({0})'.format(baseShapeName)
    return output_shape


def animate_destination_shape(destination, refFrame, controller, controllerName, baseShapeName):
    """Set expression for all destination shape's point. The result is the addition of the source shape with the
        controller shape minus the controller shape at reference frame.

    :param destination: destination shape
    :type destination: _curveknob.Stroke instance
    :param refFrame: reference frame
    :type refFrame: int
    :param controller: controller shape
    :type controller: _curveknob.Stroke instance
    :param controllerName: controller shape's name
    :type controllerName: str
    :param baseShapeName: source shape's name
    :type baseShapeName:str
    """
    for i, point in enumerate(destination):

        controllerXValue = controller[i].getPositionAnimCurve(0).evaluate(refFrame)
        controllerYValue = controller[i].getPositionAnimCurve(1).evaluate(refFrame)

        AnimcurveX = point.getPositionAnimCurve(0)
        AnimcurveX.expressionString = "[python -execlocal try:\\n math\\nexcept:\\n import math\\n\\nn" \
                                      " = nuke.thisNode()\\n\\ncurves = n\\['curves'\\]\\" \
                                      "nsource = curves.toElement('{0}')\\ncontroller" \
                                      " =  curves.toElement('{1}')\\nt = " \
                                      "controller.getTransform()\\nrot = t.getRotationAnimCurve(2).evaluate(nuke.frame())" \
                                      "\\n\\nsourceValx = source\\[{2}\\].getPositionAnimCurve(0).evaluate(nuke.frame())" \
                                      "\\ncontrollerValx= controller\\[{2}\\].getPositionAnimCurve(0).evaluate(nuke.frame())" \
                                      "\\n\\nx = controllerValx - {3}\\n\\n\\nsourceValy = " \
                                      "source\\[{2}\\].getPositionAnimCurve(1).evaluate(nuke.frame())\\ncontrollerValy =" \
                                      " controller\\[{2}\\].getPositionAnimCurve(1).evaluate(nuke.frame())\\ny = " \
                                      "controllerValy - {4}\\n\\ntheta = math.atan2(y,x) \\n\\n\\n\\nret" \
                                      " = sourceValx + math.sqrt(x*x + y*y)*math.cos(theta + rot * 3.1415/180)" \
                                      "\\n\\n\\n\\n\\n\\n\\n]".format(baseShapeName, controllerName, i, controllerXValue, controllerYValue)
        AnimcurveX.useExpression = True
        AnimcurveY = point.getPositionAnimCurve(1)
        AnimcurveY.expressionString = "[python -execlocal try:\\n math\\nexcept:\\n import math\\n\\nn" \
                                      " = nuke.thisNode()\\n\\ncurves = n\\['curves'\\]\\" \
                                      "nsource = curves.toElement('{0}')\\ncontroller" \
                                      " =  curves.toElement('{1}')\\nt = " \
                                      "controller.getTransform()\\nrot = t.getRotationAnimCurve(2).evaluate(nuke.frame())" \
                                      "\\n\\nsourceValx = source\\[{2}\\].getPositionAnimCurve(0).evaluate(nuke.frame())" \
                                      "\\ncontrollerValx= controller\\[{2}\\].getPositionAnimCurve(0).evaluate(nuke.frame())" \
                                      "\\n\\nx = controllerValx - {3}\\n\\n\\nsourceValy = " \
                                      "source\\[{2}\\].getPositionAnimCurve(1).evaluate(nuke.frame())\\ncontrollerValy =" \
                                      " controller\\[{2}\\].getPositionAnimCurve(1).evaluate(nuke.frame())\\ny = " \
                                      "controllerValy - {4}\\n\\ntheta = math.atan2(y,x) \\n\\n\\n\\nret" \
                                      " = sourceValy + math.sqrt(x*x + y*y)*math.sin(theta + rot * 3.1415/180)" \
                                      "\\n\\n\\n\\n\\n\\n\\n]".format(baseShapeName, controllerName, i, controllerXValue, controllerYValue)
        AnimcurveY.useExpression = True


def controller_in_layer(num, layer):
    """Get the number of shape with 'source' in it's name. return that number + 1.

    :param layer: layer in wich to search
    :type layer: nuke.splinewarp.Layer
    :return: new source index
    :rtype: int
    """
    for curve in layer:
        if 'controller' in curve.name:
            num += 1

    for l in layer:
        if isinstance(l, sp.Layer):
            num = controller_in_layer(num, l)

    return num


def getPanel():
    """Generate a panel in wich user enter the reference frame.

    :return: the panel
    :rtype: nuke.Panel instance
    """

    panel = nuke.Panel('Splinewarp Controller Shape')
    panel.addBooleanCheckBox(" Rename selected curves to 'source#'", True)
    panel.addBooleanCheckBox(" Moving Controller (Heavier)", False)
    panel.addBooleanCheckBox(" Rotate Controller (Heavier)", False)
    panel.setWidth(300)

    return panel


def splinewarp_controller():
    """Main function of splinewarp controller. Based on the first shape of a splinewarp rootlayer, it will duplacate
        that shape twice; one will become the controller shape. the shape from wich the user will add keyframe; the
        other will be the destination shape. The latter will be the result of the source shape plus the
        controller shape minus the controller shape at reference frame.
    """
    # Panel
    panel = getPanel()
    if panel.show() == 0:
        return

    if nuke.thisNode().Class() != "SplineWarp3":
        sw = nuke.selectedNode()
    else:
        sw = nuke.thisNode()
    ref_frame = nuke.frame()
    node_name = sw.name()

    curves = sw['curves']
    root = curves.rootLayer
    shapes = curves.getSelected()
    if shapes == []:
        return
    num = 1
    for base_shape in shapes:
        controllerNum = controller_in_layer(num, root)
        # Rename shapes if user want to
        if panel.value(" Rename selected curves to 'source#'") == True:
            base_shape.name = 'source{0}'.format(controllerNum)
        baseShapeName = base_shape.name

        fullBaseShapeName = full_shape_name(root, baseShapeName)

        # Controller
        expx = expX(fullBaseShapeName, ref_frame)
        expy = expY(fullBaseShapeName, ref_frame)

        controller = createControllerShape(base_shape, baseShapeName)
        controllerName = controller.name
        fullControllerShapeName = full_shape_name(root, controllerName)
        clear_controller(controller, ref_frame, node_name, base_shape, fullControllerShapeName)
        if panel.value(" Moving Controller (Heavier)") == True:
            animate_controller_shape(controller, expx, expy)
        if panel.value(" Rotate Controller (Heavier)") == True:
            expR = exp_rotate(baseShapeName, ref_frame)
            rotate_controller_shape(controller, expR)

        # Destination
        destination = create_destination_shape(base_shape, baseShapeName)
        animate_destination_shape(destination, ref_frame, controller, fullControllerShapeName, fullBaseShapeName)

        # join Shapes
        curves.defaultJoin(base_shape, destination)
