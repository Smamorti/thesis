import numpy as np

def readStack(stackfile):

    sourceDict = {}
    texDict = {}
    colorDict = {}
    typeList = []


    with open(stackfile) as f:

        line = f.readline()
        line = line.rstrip('\n')

        while line:

            if line[0] != '+':

                # check if the variable already exists or if we are just beginning to read the file

                if 'sourcelist' in locals():

                    sourceDict[source] = sourcelist
                    texDict[source] = tex 
                    colorDict[source] = int(color)
                    typeList.append(source)

                # new bkg/signal type
                source, tex, style, color = line.split('\t')
                sourcelist = []
                
            else:
                
                sourcelist.append(line.lstrip('+'))

            line = f.readline()
            line = line.rstrip('\n')

    # add last type of bkg/signal

    sourceDict[source] = sourcelist
    texDict[source] = tex
    colorDict[source] = int(color)
    typeList.append(source)

    f.close

    return typeList, sourceDict, texDict, colorDict

def readConf(conffile):

    locationDict = {}
    xSecDict = {}

    channels_conf, files, xSecs = np.loadtxt(conffile, comments = "%", unpack = True, dtype = str)

    for i in range(len(channels_conf)):

        locationDict[channels_conf[i]] = files[i]
        xsec = float(xSecs[i])
        xSecDict[channels_conf[i]] = xsec

    return locationDict, xSecDict

# testing

if __name__ == '__main__':

    typeList, sourceDict, texDict,colorDict = readStack('../samples/2018_total.stack')

    print(typeList)
    print(sourceDict)
    print(texDict)
    print(colorDict)

    locationDict, xSecDict = readConf('../samples/2018_total.conf')

    print(locationDict)
    print(xSecDict)
