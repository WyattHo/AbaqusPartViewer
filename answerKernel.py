import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

###################################################################
# Function area - main
###################################################################
def CollectNodesAndElements(content):
    nodeDict = {}
    elementDict = {}

    scanNode = False
    scanElement = False

    for text in content:
        if not text.startswith('**'):
            if text.startswith('*Part'):
                partName = text.split('=')[-1].strip('\n')

            if text.startswith('*Node'):
                scanNode = True
                scanElement = False
                continue

            if text.startswith('*Element'):
                scanElement = True
                scanNode = False
                continue

            if text.startswith('*End Part'):
                scanElement = False
                scanNode = False
                continue

            if scanNode:
                idx, coorX, coorY, coorZ = text.rstrip('\n').split(',')
                idx, coorX, coorY, coorZ = eval(idx), eval(coorX), eval(coorY), eval(coorZ)
                nodeDict[idx] = nodeObj(coorX, coorY)

            if scanElement:
                idx, nodeIdx1, nodeIdx2, nodeIdx3 = text.rstrip('\n').split(',')
                idx, nodeIdx1, nodeIdx2, nodeIdx3 = eval(idx), eval(nodeIdx1), eval(nodeIdx2), eval(nodeIdx3)
                elementDict[idx] = elementObj(nodeIdx1, nodeIdx2, nodeIdx3)


    return nodeDict, elementDict, partName



def CollectEdges(nodeDict, elementDict):
    edgeDict = {}
    nodeSetList = []

    for key in elementDict.keys():
        nodeSet1 = set([elementDict[key].nodeIdx1, elementDict[key].nodeIdx2])
        nodeSet2 = set([elementDict[key].nodeIdx2, elementDict[key].nodeIdx3])
        nodeSet3 = set([elementDict[key].nodeIdx1, elementDict[key].nodeIdx3])
        
        for nodeSet in [nodeSet1, nodeSet2, nodeSet3]:
            if nodeSet not in nodeSetList:
                copySet = nodeSet.copy()
                nodeIdx1 = copySet.pop()
                nodeIdx2 = copySet.pop()
                
                idx = len(nodeSetList)
                edgeDict[idx] = edgeObj(nodeIdx1, nodeIdx2, nodeDict)

                nodeSetList.append(nodeSet)

            else:
                idx = nodeSetList.index(nodeSet)
                edgeDict[idx]
            
            elementDict[key].AppendEdgeIdx(idx)

    return edgeDict



def CheckAspectRatio(elementDict, ratioLim=5):
    elementTgtList = [elementDict[key] for key in elementDict.keys() if elementDict[key].aspectRatio > ratioLim]

    return elementTgtList



def CheckArea(elementDict):
    minArea = 1000
    maxArea = 0
    
    for key in elementDict.keys():
        area = elementDict[key].area
        
        if area < minArea:
            minArea = elementDict[key].area
            minKey = key

        if area > maxArea:
            maxArea = area
            maxKey = key

    minElement = elementDict[minKey]
    maxElement = elementDict[maxKey]

    return minElement, maxElement



def CheckAdjacent(elementDict, idx=5):
    tgtEdgeIdxList = elementDict[idx].edgeIdxList

    elementTgtList = []
    for key in elementDict.keys():
        for idx2 in elementDict[key].edgeIdxList:
            if idx2 in tgtEdgeIdxList:
                elementTgtList.append(elementDict[key])
                break

    return elementTgtList



def PlotGlobal(edgeDict):
    fig = plt.figure(figsize=(8,6), tight_layout=True)
    ax = plt.axes()

    for key in edgeDict.keys():
        dataX = [edgeDict[key].strX, edgeDict[key].endX]
        dataY = [edgeDict[key].strY, edgeDict[key].endY]

        ax.plot(dataX, dataY, 'silver', zorder=-10)

    return fig, ax



def PlotTarget(ax, elementTgtList, facecolor='r', edgecolor='r'):
    for ele in elementTgtList:
        pts = [[ele.node1X, ele.node1Y], [ele.node2X, ele.node2Y], [ele.node3X, ele.node3Y]]
        polygon = Polygon(pts, facecolor=facecolor, edgecolor=edgecolor)
        ax.add_patch(polygon)



###################################################################
# Function area - sub
###################################################################
def GetLength(vector):
    length = sum([comp**2 for comp in vector])**0.5
    return length



def ComputeTriArea(a, b, c):
    s = (a + b + c) / 2
    area = (s * (s - a) * (s - b) * (s - c))**0.5
    return area



###################################################################
# Class area
###################################################################
class nodeObj:
    def __init__(self, coorX, coorY):
        self.coorX = coorX
        self.coorY = coorY


class elementObj:
    def __init__(self, nodeIdx1, nodeIdx2, nodeIdx3):
        self.nodeIdx1 = nodeIdx1
        self.nodeIdx2 = nodeIdx2
        self.nodeIdx3 = nodeIdx3
        self.edgeIdxList = []


    def ComputeProperties(self, nodeDict):
        self.node1X = nodeDict[self.nodeIdx1].coorX
        self.node1Y = nodeDict[self.nodeIdx1].coorY
        
        self.node2X = nodeDict[self.nodeIdx2].coorX
        self.node2Y = nodeDict[self.nodeIdx2].coorY
        
        self.node3X = nodeDict[self.nodeIdx3].coorX
        self.node3Y = nodeDict[self.nodeIdx3].coorY

        deltaX1 = self.node2X - self.node1X
        deltaY1 = self.node2Y - self.node1Y

        deltaX2 = self.node3X - self.node2X
        deltaY2 = self.node3Y - self.node2Y

        deltaX3 = self.node3X - self.node1X
        deltaY3 = self.node3Y - self.node1Y


        self.length1 = GetLength([deltaX1, deltaY1])
        self.length2 = GetLength([deltaX2, deltaY2])
        self.length3 = GetLength([deltaX3, deltaY3])

        self.aspectRatio = max(self.length1, self.length2, self.length3) / min(self.length1, self.length2, self.length3)
        self.area = ComputeTriArea(self.length1, self.length2, self.length3)


    def AppendEdgeIdx(self, idx):
        self.edgeIdxList.append(idx)



class edgeObj:
    def __init__(self, nodeIdxStr, nodeIdxEnd, nodeDict):
        self.strX = nodeDict[nodeIdxStr].coorX
        self.strY = nodeDict[nodeIdxStr].coorY
        self.endX = nodeDict[nodeIdxEnd].coorX
        self.endY = nodeDict[nodeIdxEnd].coorY



###################################################################
# Main area
###################################################################
if __name__ == '__main__':

    # Open input file
    with open('./test.inp', 'r') as f:
        content = f.readlines()


    # Collect nodes / elements / edges
    nodeDict, elementDict, partName = CollectNodesAndElements(content)
    edgeDict = CollectEdges(nodeDict, elementDict)

    
    # Compute length / aspect ratio / area  for all elements
    for key in elementDict.keys():
        elementDict[key].ComputeProperties(nodeDict)
    

    # Check aspect ratio
    elementTgtList = CheckAspectRatio(elementDict, ratioLim=5)
    fig, ax = PlotGlobal(edgeDict)
    PlotTarget(ax, elementTgtList, facecolor='gold', edgecolor='r')


    # Check area
    elementMin, elementMax = CheckArea(elementDict)
    fig, ax = PlotGlobal(edgeDict)
    PlotTarget(ax, [elementMin], facecolor='lime', edgecolor='r')
    PlotTarget(ax, [elementMax], facecolor='violet', edgecolor='r')


    # Check adjacent elements
    elementTgtList = CheckAdjacent(elementDict, idx=5)
    fig, ax = PlotGlobal(edgeDict)
    PlotTarget(ax, elementTgtList, facecolor='royalblue', edgecolor='r')

    plt.show()