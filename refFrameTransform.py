n = nuke.selectedNode()
frame = nuke.frame()
try:
    n['refFrame'].setValue(frame)

except:
    refFrame = nuke.Int_Knob('refFrame', "Ref Frame")
    n.addKnob(refFrame)
    refFrame.setValue(frame)
    refFrame.setVisible(False)

    # TRANSLATE
    translate = n['translate']
    if translate.hasExpression():
        animX = translate.animation(0)
        expressionX = animX.expression()
        x1 = expressionX.find("?")
        x2 = expressionX.find(":")
        xsource = expressionX[x1+2:x2-1]

        if n['invert'].value() == 1:
            invert = "-"
        else:
            invert = "+"

        if animX.evaluate(nuke.frame()) < 0:
            negX = "-"
        else:
            negX = "+"

        frame = str(nuke.frame())

        animX.setExpression("(((((" + expressionX + ")))))" + invert + "-" + xsource + "(refFrame)")

        animY = translate.animation(1)
        expressionY = animY.expression()
        y1 = expressionY.find("?")
        y2 = expressionY.find(":")
        ysource = expressionY[y1+2:y2-1]

        if n['invert'].value() == 1:
            invert = "-"
        else:
            invert = "+"

        if animY.evaluate(nuke.frame())<0:
            negY = "-"
        else:
            negY = "+"

        animY.setExpression("(((((" + expressionY + ")))))" + invert + "-" + ysource + "(refFrame)")


    # ROTATE
    rotate = n['rotate']
    if rotate.hasExpression():
        ranim = rotate.animation(0)
        expressionR = ranim.expression()
        r1 = expressionR.find("?")
        r2 = expressionR.find(":")
        rsource = expressionR[r1+2:r2-1]

        if n['invert'].value() == 1:
            invert = "-"
        else:
            invert = "+"

        if ranim.evaluate(nuke.frame()) < 0:
            negR = "-"
        else:
            negR = "+"

        ranim.setExpression("(((((" + expressionR + ")))))" + invert + "-" + rsource + "(refFrame)")


    # SCALE
    scale = n['scale']
    if scale.hasExpression():
        sanimW = scale.animation(0)
        expressionSW = sanimW.expression()
        sW1 = expressionSW.find("?")
        sW2 = expressionSW.find(":")
        sWsource = expressionSW[sW1+2:sW2]


        if n['invert'].value() == 1:
            negSW = "abs(1/"
        else:
            negSW = "abs("

        # if sanimW.evaluate(nuke.frame())<0:
        #     negSW = "-" + negSW
        # else:
        #     negSW = "+" + negSW

        sanimW.setExpression("(((((" + expressionSW + ")))))" + "-" + negSW +sWsource + "(refFrame))+1")

        sanimH = scale.animation(1)
        expressionSH = sanimH.expression()
        sH1 = expressionSH.find("?")
        sH2 = expressionSH.find(":")
        sHsource = expressionSH[sH1+2:sH2]

        if n['invert'].value() == 1:
            negSH = "abs(1/"
        else:
            negSH = "abs("

        # if sanimW.evaluate(nuke.frame()) < 0:
        #     negSH = "-" + negSH
        # else:
        #     negSH = "+" + negSH

        sanimH.setExpression("(((((" + expressionSH + ")))))" + "-" + negSH + sHsource + "(refFrame))+1")
    # LABEL
    label = n['label']
    labelV = n['label'].value()
    label.setValue(labelV + "Ref Frame: [value refFrame]")