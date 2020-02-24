def makeYlabels(xtypeList, binList):

    yLabels = []

    for i in range(len(xtypeList)):

        if xtypeList[i] == "Other":

            yLabels.append("Events")

        elif xtypeList[i] == "GeV":

            binWidth = (binList[i][2] - binList[i][1]) / binList[i][0]

            if binWidth == 1.0:

                yLabels.append("Events / GeV")

            elif binWidth == (binList[i][2] - binList[i][1]) // binList[i][0]:

                yLabels.append("Events / {} GeV".format(int(binWidth)))

            else:

                yLabels.append("Events / {} GeV".format(binWidth))

    return yLabels

def str2tuple(string):

    # to convert binList strings achieved from reading in *.plot files
                                                                                                                                                                                                         
    string = string.lstrip('(').rstrip(')')
    spl = string.split(',')

    return (int(spl[0]), float(spl[1]), float(spl[2]))
