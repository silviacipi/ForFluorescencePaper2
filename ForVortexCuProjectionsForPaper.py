import h5py
import numpy as np
from matplotlib import pyplot as plt
from scipy import math

            
def findContour(nxsfileName,dataFolder, channelmin,channelmax,aa,bb):
    print nxsfileName
    
    mypath=h5py.File(nxsfileName,'r') 
    print 'looking for "',dataFolder, '" in the tree...'
    contLoop=True
    pathTot=''
    contLoop, pathToData, pathTot=myRec(mypath,contLoop,pathTot,dataFolder)
    print pathTot
    dataionization='ionc_i'
    print 'looking for "',dataionization, '" in the tree...'
    contLoop2=True
    pathTot2=''
   # mypath2=h5py.File(nxsfileName,'r') 
    image=np.zeros((bb,aa))
    print np.shape(image)
    contLoop2, pathToData2, pathTot2=myRec(mypath,contLoop2,pathTot2,dataionization)
    if not (contLoop or contLoop2):
        print 'database "',dataFolder,'" found in  ', pathTot
        data=mypath[str(pathTot)]
        ion=mypath[str(pathTot2)]
        npdata=np.array(data)
        npion=np.array(ion)
        a,b,c=npdata.shape
        print a,b,c, ' file images to analyse' 
        sizeA=int(math.sqrt(a))
        print 'size', sizeA
        s=(aa,bb)
        
        counter=0
        calibration=0.0012221238
        minchan=int(channelmin/calibration)
        maxchan=int(channelmax/calibration)
        for i in range (aa):
#            print 'i', i
            for j in range (bb):
#               print j
                sum=0
                for col in range(minchan,maxchan):
                    sum=sum+npdata[counter][0][col]/npion[counter]
                if i % 2 == 0:
#                print 'it is even 
                   # print i,j
                    image[j][i]=sum
#                print j,i
                else:
                 image[bb-1-j][i]=sum
#                print sizeA-1-j,i
                counter=counter+1
        #fig1 = plt.figure(1)
        #plt.imshow(image)
        #plt.show()
        xlength=np.linspace(0, aa, aa)
        #plt.plot(xlength,image[0][:])
        #plt.show()
    else:
        print 'database "', dataFolder,'" not found!'
    mypath.close()
    return image

      
def myRec(obj,continueLoop,pathTot,dataFolder):  
    ### recursive function to look for the data database
    temp=None
    i=1
    tempPath=''
    for name, value in obj.items():
        if continueLoop:
            #check if the object is a group
            if isinstance(obj[name], h5py.Group):
                tempPath='/'+name
                if len(obj[name])>0:
                    continueLoop,temp,tempPath= myRec(obj[name],continueLoop,tempPath,dataFolder)
                else:
                    continue
            else:
                test=obj[name]
                temp1='/'+dataFolder
                if temp1 in test.name:
                    continueLoop=False
                    tempPath=pathTot+'/'+name
                    return continueLoop,test.name,tempPath
            i=i+1
        if (i-1)>len(obj.items()):
            tempPath=''
    pathTot=pathTot+tempPath
    return continueLoop,temp, pathTot

    
   
#########For testing function
if __name__ == "__main__":
    
    width=86
    height=10
    depthProjections=181
    #name="/home/xfz42935/Documents/Vortex/Merlin/merlinProjections.hdf"
    name="/dls/i13-1/data/2017/cm16785-1/processing/VortexTomo/vortexProjectionsCuForPaper.hdf"
    vortexIm=h5py.File(name,"w")
    dsetImage=vortexIm.create_dataset('data', (depthProjections,height,width), 'f')
    print dsetImage.shape
    print dsetImage.dtype
    count=0
    imageVortex=np.zeros(((depthProjections,height,width)))
    myMax=0
    for i in range(92780,92820)+ range(92826,92967):
        #print 'Im here'
        path=str(i)      
        #pathToNexus='/dls/i13-1/data/2017/cm16785-1/raw/'
        #pathToNexus=' C:\\Users\\xfz42935\\Documents\\Experiments\\vortexPtycho\\data\\pippo.txt'
        #pathToNexus=' C:\\Users\\xfz42935\\Documents\\pippo.txt'
        
        pathToNexus='/dls/i13-1/data/2017/cm16785-1/raw/'
        pathToNexus += "%s.nxs" %(path)
        print pathToNexus
        imageVortex[count][:][:]=findContour(pathToNexus,'fullSpectrum',7.9,8.1,width,height)#Cu
        #imageVortex[count][:][:]=findContour(pathToNexus,'fullSpectrum',9.3,9.6,width,height)#Pt
        if count <40:
            print 'correct misalignment'
            pluto=np.zeros([height,width])
            print 'pluto shape',np.shape(pluto)
            for j in range(width-6):
                #print 'j',j
                #print np.shape(imageVortex[count][:][:])
                #print 'pluto',pluto[:,j],imageVortex[count][:,j+6]
                pluto[:,j]=imageVortex[count][:,j+3]
                
            imageVortex[count][:][:]=pluto
            print 'corrected'
        locMax=np.max(np.max(imageVortex[count][:][:]))
        if myMax<locMax:
            myMax=locMax
        #plt.imshow(imageMerlin[count][:][:])
        #plt.show()
        #imagePt=findContour(pathToNexus,'fullSpectrum',9.3,9.6,width,height)

        count+=1
        print 'count ', count
    print 'max Value found', myMax
    dsetImage[...]=imageVortex#/myMax
    #print dsetImage.value
    vortexIm.close()
    print 'done, file closed'
    #pathToNexus='/dls/i13-1/data/2017/cm16785-1/raw/92876.nxs'
    #name='C:\\Users\\xfz42935\\Documents\\Alignement\\pco1-63429.hdf'
    '''
    findContour(<pathToNexusFile>,<nameOfTheEntry>,minimumEnergy,MaximumEnergy,xLenghtOfPtychoScan,yLenghtofPtychoScan)
    nameofTheEntry is 'fullSpectrum' for vortex, PCO or Merlin is 'data'
    '''
    #findContour(pathToNexus,'fullSpectrum',7.9,8.1,86,10)
    #findContour(pathToNexus,'fullSpectrum',9.3,9.6,86,10)
