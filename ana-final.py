import h5py
import numpy as np

f = h5py.File('job_6380.h5','r')
#dataSetNum equals to total process number
dataSetNum = 15 
intervalsNum = [72, 2100, 576, 480, 660, 636, 756, 756, 948, 1932, 1980, 1932, 972, 1284, 1296, 1332, 1548, 3240, 3120, 2232, 2532, 4476, 4524, 4416]
intervalsNum = [(n+6) for n in intervalsNum]
machineNodes=['gpu01']
processNumPerNode = 15



nodesNum = len(machineNodes)
dataset=[]
startIndex =[0]
for i in range(0, len(intervalsNum)):
    e = intervalsNum[i]
    s = startIndex[i] + e 
    startIndex.append(s);

endIndex = startIndex[1:]
#endIndex = [(n+12) for n in endIndex]
startIndex.pop()

print("intervalsNum = " + str(intervalsNum))
print("startIndex = " + str(startIndex))
print("endIndex = " + str(endIndex))

#exit() 

for i in range(0,nodesNum):
    for j in range(0, processNumPerNode):
        node = machineNodes[i]
        processID = str(i * processNumPerNode + j)
        #print((node, processID))
        dataset.append(f['Steps']['0']['Nodes'][node]['Tasks'][processID])


rowsPerDataset = len(dataset[0])
readMB = [0 for i in range(0, rowsPerDataset)]
writeMB = [0 for i in range(0, rowsPerDataset)]


fileNameFinalRead = "final_read.txt"
fileNameFinalWrite = "final_write.txt"
fileNameFinalReadWrite = "final_read_write.txt"

ffr = open(fileNameFinalRead, "w")
ffw = open(fileNameFinalWrite, "w")
ffrw = open(fileNameFinalReadWrite, "w")


for k in range(0, len(startIndex)):
    (start, end) = (startIndex[k], endIndex[k])
    fileNameRead = "read_iter%02d%s" %(k, ".txt")
    fileNameWrite = "write_iter%02d%s" %(k, ".txt")
    fileNameReadSum = "sum_read_iter%02d%s" %(k, ".txt")
    fileNameWriteSum = "sum_write_iter%02d%s" %(k, ".txt")
    fr = open(fileNameRead, "w")
    fw = open(fileNameWrite, "w")
    sfr = open(fileNameReadSum, "w")
    sfw = open(fileNameWriteSum, "w")
    for j in range(start, end):
        for i in range(0, dataSetNum):
            readMB[j] = readMB[j] + dataset[i][j][8]
            writeMB[j] = writeMB[j] + dataset[i][j][9]

    sumRead = 0.0
    sumWrite = 0.0
    for j in range(start, end):
        sumRead = sumRead + readMB[j]
        sumWrite = sumWrite + writeMB[j]
        fr.write(str(readMB[j]) + "\n")
        fw.write(str(writeMB[j]) + "\n")


    sfr.write(str(sumRead) + "\n");
    sfw.write(str(sumWrite) + "\n")
    ffr.write(str(k + 1) + "    " + str(sumRead) + "\n")
    ffw.write(str(k + 1) + "    " + str(sumWrite) +"\n")
    ffrw.write(str(k + 1) + "    " + str(sumRead) + "    " + str(sumWrite) + "\n")

    ffr.flush()
    ffw.flush()
    ffrw.flush()

    fr.close()
    fw.close()
    sfr.close()
    sfw.close()

ffr.close()
ffw.close()
ffrw.close()


