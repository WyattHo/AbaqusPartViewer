import tkinter as tk
from tkinter import filedialog
from tkinter import font
import answerKernel


def ReadInp():
    fileName = filedialog.askopenfilename(title='open')
    entryText.set(fileName)

    return



def CollectData():
    fileName = entryText.get()
    
    with open(fileName, 'r') as f:
        content = f.readlines()

    nodeDict, elementDict, partName = answerKernel.CollectNodesAndElements(content)
    edgeDict = answerKernel.CollectEdges(nodeDict, elementDict)

    for key in elementDict.keys():
        elementDict[key].ComputeProperties(nodeDict)

    partNameVar.set(partName)

    return nodeDict, elementDict, edgeDict



def PlotGlobal(edgeDict):
    canvas.delete('all')

    minX = min([min([edgeDict[key].strX, edgeDict[key].endX]) for key in edgeDict.keys()])
    maxX = max([max([edgeDict[key].strX, edgeDict[key].endX]) for key in edgeDict.keys()])
    minY = min([min([edgeDict[key].strY, edgeDict[key].endY]) for key in edgeDict.keys()])
    maxY = max([max([edgeDict[key].strY, edgeDict[key].endY]) for key in edgeDict.keys()])

    deltaX = maxX - minX
    deltaY = maxY - minY

    for key in edgeDict.keys():
        strX = (edgeDict[key].strX - minX) * width / deltaX
        endX = (edgeDict[key].endX - minX) * width / deltaX
        strY = (edgeDict[key].strY - minY) * height / deltaY * -1 + height
        endY = (edgeDict[key].endY - minY) * height / deltaY * -1 + height

        canvas.create_line(strX, strY, endX, endY, fill='grey')

    return minX, maxX, minY, maxY, deltaX, deltaY



def PlotTarget(elementTgtList, minX, maxX, minY, maxY, deltaX, deltaY):
    for ele in elementTgtList:
        node1X = (ele.node1X - minX) * width / deltaX
        node2X = (ele.node2X - minX) * width / deltaX
        node3X = (ele.node3X - minX) * width / deltaX
        node1Y = (ele.node1Y - minY) * height / deltaY * -1 + height
        node2Y = (ele.node2Y - minY) * height / deltaY * -1 + height
        node3Y = (ele.node3Y - minY) * height / deltaY * -1 + height
        canvas.create_polygon(node1X, node1Y, node2X, node2Y, node3X, node3Y, fill='red', outline='blue', width=2)



def PushBtn1():
    nodeDict, elementDict, edgeDict = CollectData()
    elementTgtList = answerKernel.CheckAspectRatio(elementDict, ratioLim=5)
    minX, maxX, minY, maxY, deltaX, deltaY = PlotGlobal(edgeDict)
    PlotTarget(elementTgtList, minX, maxX, minY, maxY, deltaX, deltaY)
    


def PushBtn2():
    nodeDict, elementDict, edgeDict = CollectData()
    elementMin, elementMax = answerKernel.CheckArea(elementDict)
    minX, maxX, minY, maxY, deltaX, deltaY = PlotGlobal(edgeDict)
    PlotTarget([elementMin], minX, maxX, minY, maxY, deltaX, deltaY)
    PlotTarget([elementMax], minX, maxX, minY, maxY, deltaX, deltaY)



def PushBtn3():
    nodeDict, elementDict, edgeDict = CollectData()
    elementTgtList = answerKernel.CheckAdjacent(elementDict, idx=5)
    minX, maxX, minY, maxY, deltaX, deltaY = PlotGlobal(edgeDict)
    PlotTarget(elementTgtList, minX, maxX, minY, maxY, deltaX, deltaY)



if __name__ == '__main__':
    root = tk.Tk()
    root.title('Tri Graph Painter')
    root.geometry('500x450')
    root.configure()

    labelFrame = tk.LabelFrame(root, text='Read input file')
    labelFrame.pack()
    
    frame1 = tk.Frame(labelFrame)
    frame1.pack()
    
    entryText = tk.StringVar()
    inpFileEntry = tk.Entry(frame1, width=55, textvariable=entryText)
    inpFileEntry.pack(side=tk.LEFT)

    btn1 = tk.Button(frame1, text='Read input', command=ReadInp)
    btn1.pack(side=tk.LEFT, padx=2, ipadx=2)

    frame2 = tk.Frame(labelFrame)
    frame2.pack()
    
    partNameVar = tk.StringVar()
    label = tk.Label(frame2, textvariable=partNameVar)
    label.pack(side=tk.LEFT, padx=2, ipadx=2)

    btn2 = tk.Button(frame2, text='Show aspect ratio > 5', command=PushBtn1)
    btn2.pack(side=tk.LEFT, padx=2, ipadx=2)
    
    btn3 = tk.Button(frame2, text='Show max/min area', command=PushBtn2)
    btn3.pack(side=tk.LEFT, padx=2, ipadx=2)
    
    btn4 = tk.Button(frame2, text='Find element 5 adj', command=PushBtn3)
    btn4.pack(side=tk.LEFT, padx=2, ipadx=2)

    btnFont = font.Font(family='Helvetica', size=8)
    btn1['font'] = btnFont
    btn2['font'] = btnFont
    btn3['font'] = btnFont
    btn4['font'] = btnFont

    height, width = 300, 400
    canvas = tk.Canvas(root, height=height, width=width, bg='white')
    canvas.pack(pady=30)

    root.mainloop()
    