import h5py
import numpy as np
from matplotlib import pyplot as plt
from scipy import math
import cv2
import json

 
#import TomopyReconstructionForVortexAbsorptionPt2506
from TomopyReconstructionForVortexAbsorptionPt2506 import tomography


  
class material(object):
    def __init__(self, name,density):
        self.name=name
        self.density=density
        print 'class defining material'
    #name =''
    keys=['material', 'massAbsCoef']
    myDictionary=dict(dict.fromkeys(keys, None))
    
    #def setName(self,materialName):
    #    self.name=materialName
    def readName(self):
        print 'material name:',self.name  
    def setPathToProjections(self,path):
        self.pathToProjections=path
        
class processingTools():
    def __init__(self):
        print 'defining tool'
        
class materialProjectionsTomo(object):
    def __init__(self, name,pathToProjection):
        self.name=name
        print 'class defining material'
        #self.projections=pathToProjection
        self.path=pathToProjection
    def set_projection(self,projection):
        self.projection=projection
    def set_materialTomo(self,tomo):    #self.tomo=np.zeros([angles,width,width])
        self.tomo=tomo
    
 
            
def AttenuationCorrection(listOfMaterials,pathToMerlinTomo,dataFolder,tomoCentre,minFluoSignal,projShift):
    #print pathToNexusPt
    
    #mypathPt=h5py.File(pathToNexusPt,'r') 
    #mypathCu=h5py.File(pathToNexusCu,'r') 
    pixelSize=0.25e-4
    mypathMerlin=h5py.File(pathToMerlinTomo,'r') 
    '''
    trasmission through a pixel calculated from the transmission measured with the  Merlin: the effective density of Pt is found
     to be 1g/cm^3, for Cu 0.8g/cm^3
    '''
    #CuTransmThroughCu=0.999
    #CuTransmThroughPt=0.9951
    #PtTransmThroughCu=0.995
    #PtTransmThroughPt=0.996
    '''   
    print 'looking for "',dataFolder, '" in the tree...'
    contLoop=True
    pathTot=''
    contLoop, pathToData, pathTot=myRec(mypathPt,contLoop,pathTot,dataFolder)

    print 'looking for "',dataFolder, '" in the tree...'
    contLoop2=True
    pathTot2=''
    contLoop2, pathToData2, pathTot2=myRec(mypathCu,contLoop2,pathTot2,dataFolder)
    '''
    print 'looking for "',dataFolder, '" in the tree...'
    contLoop3=True
    pathTot3=''
    contLoop3, pathToData3, pathTot3=myRec(mypathMerlin,contLoop3,pathTot3,dataFolder)
    
    if not (contLoop3):
        print 'database "',dataFolder,'" found in  ', pathTot3
        #npdataPt=np.array(mypathPt[str(pathTot)])
        #npdataCu=np.array(mypathCu[str(pathTot2)])
        tomoMerlin=mypathMerlin[str(pathTot3)]
        
        
        
        print 'loading materials'
        print len(listOfMaterials)
        materialsAnalysis=[]
        print 'loading data...'
        
        for i in range(len(listOfMaterials)):
            print 'Im happy here'
            name=listOfMaterials[i]
            temp=materialProjectionsTomo(listOfMaterials[i].name,listOfMaterials[i].pathToProjections)
            contLoop=True
            pathTot=''
            print 'path to projections', listOfMaterials[i].pathToProjections
            mypathTemp=h5py.File(temp.path,'r') 
            contLoop, pathToData, pathTot=myRec(mypathTemp,contLoop,pathTot,dataFolder)
            try:
               
                temp.set_projection(np.array(mypathTemp[str(pathTot)]))
                #print 'just before ', temp.path,dataFolder,tomoCentre
                
                #temp.set_materialTomo(tomography(temp.path,dataFolder, tomoCentre))
                #print 'tomography added'
                materialsAnalysis.append(temp)
                materialsAnalysis[i].set_materialTomo(tomography(materialsAnalysis[i].path,dataFolder, tomoCentre))
                print materialsAnalysis[i].name, 'loaded'
                #plt.imshow(materialsAnalysis[i].tomo[1,:,:])
                #plt.show()
                #raw_input("Press Enter to continue...")   
            except:
                print 'data', listOfMaterials[i].pathToProjections, 'not found! closing'
            
        #raw_input("Press Enter to continue...")       
            #materialsAnalysis.append(materialProjectionsTomo())
            #materialsAnalysis=[]
        #npdataPt=np.array(mypathPt[str(pathTot)])
            
            
        #raw_input("Press Enter to continue...")    
        '''
        STEP 1:
        do the tomography with the acquired sinograms
        '''
        testIteration=0
        NewMaterials = [None] * len(listOfMaterials)
        MaterialsCorrection = [None] * len(listOfMaterials)
        MaterialDensity = [None] * len(listOfMaterials)
        oscillation=np.zeros(10)
        
        vortexImPtCorr=[None] * len(listOfMaterials)
        dsetImagePtCorr=[None] * len(listOfMaterials)
        dsetOscillation=[None] * len(listOfMaterials)
        
        for nMat in range(len(listOfMaterials)):
                nameTomoMaterial="/dls/i13-1/data/2017/cm16785-1/processing/VortexTomo/vortexTomo"+listOfMaterials[nMat].name+"101117.hdf"
                #nameTomoPt="/dls/i13-1/data/2017/cm16785-1/processing/VortexTomo/vortexTomoPt2506.hdf"
                #nameTomoCu="/dls/i13-1/data/2017/cm16785-1/processing/VortexTomo/vortexTomoCu2506.hdf"
            
            
                nAngles,height,width=np.shape(materialsAnalysis[nMat].projection)
                vortexImPtCorr[nMat]=h5py.File(nameTomoMaterial,"w")
                dsetImagePtCorr[nMat]=vortexImPtCorr[nMat].create_dataset('data', (11,height,width,width), 'f')
                dsetOscillation[nMat]=vortexImPtCorr[nMat].create_dataset('oscillation', (11,), 'f')
        
        
        
        
        
        while testIteration<10:
            if testIteration==0:
                for nMat in range(len(listOfMaterials)):
                    dsetImagePtCorr[nMat][testIteration,:,:,:]=materialsAnalysis[nMat].tomo[:,:,:]
                    dsetOscillation[nMat][testIteration]=materialsAnalysis[nMat].tomo[1,25,68]
            testIteration+=1
            print 'iteration', testIteration
            npdataMerlin=np.array(tomoMerlin)
            #a,b,c=np.shape(npdataMerlin)
            nAngles=0
            height=0
            width=0
            #print a,b,c, 'shape'
            #SumTotTomo=np.zeros(np.shape(tomoMerlin))
            for nMat in range (len(listOfMaterials)):
                #print nMat
                
                #print 'reconstruction done for ', materialsAnalysis[nMat].name
                print np.shape(materialsAnalysis[nMat].tomo)
                #SumTotTomo+=materialsAnalysis[nMat].tomo
                print 'VALUE',materialsAnalysis[nMat].tomo[1,25,68]
                plt.figure(1)
                plt.imshow(materialsAnalysis[nMat].tomo[1,:,:],'Greys')
                #plt.show()
                nAngles,height,width=np.shape(materialsAnalysis[nMat].projection)
                NewMaterials[nMat]=np.zeros([nAngles,height,width])
                NewMaterials[nMat][:,:,0]=materialsAnalysis[nMat].projection[:,:,0]
                #print nAngles,height,width, 'shape'
                MaterialsCorrection[nMat]=np.ones((nAngles,height,width,width))
            print 'tomography done, now Calculated Densities'    
            print 'VALUE',materialsAnalysis[1].tomo[1,25,68]
            #oscillation[testIteration-1]=materialsAnalysis[1].tomo[1,25,68]
            #raw_input("Press Enter to continue...") 
            materialRatio=[None]*len(listOfMaterials)
            materialEffectiveDensity=[None]*height
            
            for heightIndex in range(height):
                effDens=np.zeros([width,width,len(listOfMaterials)])
                for firstIndex in range(width):
                    for secondIndex in range(width):
                        nonZerMat=0
                        sum=0
                        nMat=0
                        densitynonZeroMat=1
                        pippo=0
                        countMat=0
                        
                        
                        '''
                        find a material if there is any at this scanning position
                        '''
                        for nonZerMat in range (len(listOfMaterials)):
                            if materialsAnalysis[nonZerMat].tomo[heightIndex,firstIndex,secondIndex]>minFluoSignal:
                                break
                        
                        
                        for nMat in range (len(listOfMaterials)):
                            #effDensTemp=np.zeros([height,width,width])
                            
                                #materialRatio[nMat]=materialsAnalysis[nMat].tomo[heightIndex,firstIndex,secondIndex]/SumTotTomo[heightIndex,firstIndex,secondIndex]
                            '''
                            calculate the material ration
                            '''
                            if materialsAnalysis[nonZerMat].tomo[heightIndex,firstIndex,secondIndex]>minFluoSignal:
                                materialRatio[nMat]=materialsAnalysis[nMat].tomo[heightIndex,firstIndex,secondIndex]/materialsAnalysis[nonZerMat].tomo[heightIndex,firstIndex,secondIndex]
                            else:
                                materialRatio[nMat]=0
                                
                            '''
                            ******** I'm here
                            '''
                            if materialRatio[nMat]>0:      
                                pippo+=materialRatio[nMat]*listOfMaterials[nMat].myDictionary['Beam']*pixelSize 
                                countMat+=1  
                        '''
                        calculate density of the non zero material
                        ''' 
                        if pippo>0:
                            densitynonZeroMat=npdataMerlin[heightIndex,firstIndex,secondIndex]/ pippo  
                        else:
                            densitynonZeroMat=0
                        '''
                        calculate the density for all the other materials
                        '''
                        
                        
                        for nMat in range (len(listOfMaterials)):
                            effDens[firstIndex,secondIndex,nMat]=densitynonZeroMat*materialRatio[nMat]
                            
                materialEffectiveDensity[heightIndex]=effDens
                
            MaterialCorrection=np.ones((len(listOfMaterials),nAngles,height,width,width))
             
            print 'doing correction'
            shift=projShift
            minimum=0.001
            maximum=0.05
            
            
            generalDensity=0
            '''
            this shift is due to the centre of rotation, the centre of rotation is 23, the centre of the reconstruction is 43,
             so I need to shift 20 pixels to have the profile coincide '''
            xplot=np.linspace(0, width-1,width)
            for i in range(0,nAngles):
                print 'angle', i
                for k in range(height):
                    #print 'slice',k
                    '''
                    rotating absorption
                    '''
                    M = cv2.getRotationMatrix2D((width/2,width/2),-i,1)
                    merlinSlice=npdataMerlin[k,:,:]
                    dst = cv2.warpAffine(merlinSlice,M,(width,width))
                    dstShifted=np.zeros((width,width))
                    dstShifted[0:width-1-shift,:]=dst[shift:width-1,:]
                    binaryMask=np.zeros((width,width))
                    
                    MaterialSlice=[None]*len(listOfMaterials)
                    dstShiftedMaterial=[None]*len(listOfMaterials)
                    shiftedMaterialDensity=[None]*len(listOfMaterials)
                    binaryMaskMaterial=[None]*len(listOfMaterials)
                    '''
                    rotating fluorescence and density
                    '''
                    
                    for nMat in range(len(listOfMaterials)):

                        '''
                        rotate tomography of each material
                        '''
                        dstMaterial=cv2.warpAffine(materialsAnalysis[nMat].tomo[k,:,:],M,(width,width))
                        dstShiftedMaterial[nMat]=np.zeros((width,width))
                        binaryMaskMaterial[nMat]=np.zeros((width,width))
                        '''
                        shift the rotated material
                        '''
                        dstShiftedMaterial[nMat][0:width-1-shift,:]=dstMaterial[shift:width-1,:]
                        shiftedMaterialDensity[nMat]=np.zeros([width,width])
                        '''
                        shift material density
                        '''
                        shiftedMaterialDensity[nMat][0:width-1-shift,:]=cv2.warpAffine(materialEffectiveDensity[k][:,:,nMat],M,(width,width))[shift:width-1,:]
                        #shiftedMaterialDensity[nMat]=cv2.warpAffine(materialEffectiveDensity[k][:,:,nMat],M,(width,width))

                    #print 'creating masks...'
                    for kk in range(width):
                        for ll in range(width):
                            if (dstShifted[kk,ll]>minimum) and (dstShifted[kk,ll]<maximum):
                                binaryMask[kk,ll]=1
                            for nMat in range(len(listOfMaterials)):
                                if (dstShiftedMaterial[nMat][kk,ll]>minFluoSignal):
                                    binaryMaskMaterial[nMat][kk,ll]=1
                                
                    for j in range(0,width):
                        
                        for ll in range(0,j-1):
                            '''
                            correct the new mask for my mask
                            For Cu first and Pt then
                            '''
                            
                            averageDensityMaterial=np.zeros(len(listOfMaterials))
                           
                            for nMat in range(len(listOfMaterials)):
                                
                                '''
                                profllMaterial thickness in pixel of the material at ll
                                '''
                                profllMaterial=binaryMask[ll,:]*binaryMaskMaterial[nMat][j,:]
                                correction=1
                                nMat2=0
                                for nMat2 in range(len(listOfMaterials)):
                                    
                                    profllDensMaterial=shiftedMaterialDensity[nMat2][ll,:]*binaryMaskMaterial[nMat][j,:]
                                    profThickMaterial= np.sum(profllMaterial)
                                    profDensMaterial=np.sum(profllDensMaterial)
                                    if profThickMaterial>0:
                                        averageDensityMaterial[nMat2]=profDensMaterial/profThickMaterial
                                    else:
                                        averageDensityMaterial[nMat2]=0
                                    correction=correction*math.exp(-averageDensityMaterial[nMat2]*listOfMaterials[nMat2].myDictionary[listOfMaterials[nMat].name]*pixelSize)
                                    
                                MaterialCorrection[nMat,i,k,j,ll]=correction

                        NewCorrectionMaterial=np.ones(len(listOfMaterials))

                        for lll in range(j):  
                            for nMat in range (len(listOfMaterials)):
                                NewCorrectionMaterial[nMat]*=MaterialCorrection[nMat,i,k,j,lll] 
                        '''
                        here forrect the projection for the attenuationt
                        '''
                        for nMat in range(len(listOfMaterials)):

                            NewMaterials[nMat][i,k,j]=materialsAnalysis[nMat].projection[i,k,j]/NewCorrectionMaterial[nMat]

            print 'all done, writing file for each material....'
            
            tomoNew=[None]*len(listOfMaterials)
            for nMat in range(len(listOfMaterials)):
                nameMat="/dls/i13-1/data/2017/cm16785-1/processing/VortexTomo/vortexProjections"+listOfMaterials[nMat].name+"101117.hdf"
                vortexImPt=h5py.File(nameMat,"w")
                dsetImagePt=vortexImPt.create_dataset('data', (nAngles,height,width), 'f')
                dsetImagePt[...]=NewMaterials[nMat]#/myMax
                vortexImPt.close()
                listOfMaterials[nMat].path=nameMat
                print 'processing the new tomography'
                tomoNew[nMat]=tomography(nameMat, 'data',tomoCentre )
                plt.figure(1)
                plt.imshow(materialsAnalysis[nMat].tomo[1,:,:])
        
                plt.figure(2)
                plt.imshow(tomoNew[nMat][1,:,:])
                materialsAnalysis[nMat].set_materialTomo(tomoNew[nMat])
                dsetImagePtCorr[nMat][testIteration,:,:,:]=tomoNew[nMat]
                dsetOscillation[nMat][testIteration]=materialsAnalysis[nMat].tomo[1,25,68]
        for nMat in range(len(listOfMaterials)):
            vortexImPtCorr[nMat].close()
        
    else:
        print 'database "', dataFolder,'" not found!'

    print 'all done, all closed'


      
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
    
    materialName="/home/xfz42935/Documents/Vortex/DensitiesForPaper.json"
    with open(materialName) as json_data_file:
        data = json.load(json_data_file)
        print data
        print data["materials"]["name"][0],len(data["materials"]["name"])
    raw_input('Press enter to continue...')
    '''
    numbOfMaterials=2
    
    
    namePt="/dls/i13-1/data/2017/cm16785-1/processing/VortexTomo/vortexProjectionsPtDriftCorrection2702.hdf"
    nameCu="/dls/i13-1/data/2017/cm16785-1/processing/VortexTomo/vortexProjectionsCuDriftCorrection2702.hdf"
    
    massAttcoeffCu118=164.83
    massAttcoeffPt118=185.2#184.0857#134.3#
    
    massAttcoeffCu944=250.18#127.08#252.5462#241.8#
    massAttcoeffPt944=137.14#130.3238#288.16#
    
    massAttcoeffCu804=50.028
    massAttcoeffPt804=190.3#197.5128#321.4#
    '''
    
    
    listOfMaterials = []
    for i in range(len(data["materials"]["name"])):
        listOfMaterials.append(material(data["materials"]["name"][i],data["materials"]["density"][i]))
        listOfMaterials[i].setPathToProjections(data["materials"]["path"][i])
        print listOfMaterials[i].name,listOfMaterials[i].density, listOfMaterials[i].pathToProjections
    raw_input('Press enter to continue...')
    print 'loading mass attenuation coefficients...'
    
    massAttenuationCoefficients="/home/xfz42935/Documents/Vortex/RajaParameterFile.json"
    with open(massAttenuationCoefficients) as json_data_file:
        data2 = json.load(json_data_file)
        #print data2
        for i in range(len(data["materials"]["name"])):
            print 'setting up mass absorption coefficient for ', listOfMaterials[i].name
            
            for j in range(len(data["materials"]["name"])):
                print 'mass absorption For ', listOfMaterials[j].name, 'is', data2[listOfMaterials[i].name][listOfMaterials[j].name]
                listOfMaterials[i].myDictionary[listOfMaterials[j].name]=data2[listOfMaterials[i].name][listOfMaterials[j].name]
            listOfMaterials[i].myDictionary["Beam"]=data2[listOfMaterials[i].name]["Beam"]
        print  'here'
        print listOfMaterials[i].myDictionary
    raw_input('finished loading material properties: Press enter to continue...')
    '''
    
    #listOfMaterials
    #a=listOfMaterials[0]()
    #mat1=material()
    #mat1.setName('Cu')
    #mat1.myDictionary={'Cu':massAttcoeffCu804, 'Pt':massAttcoeffCu944, 'Beam':massAttcoeffCu118}
    #a=listOfMaterials[0]()
    #mat2=material()
    #mat2.setName('Pt')
    #mat2.myDictionary={'Cu':massAttcoeffPt804, 'Pt':massAttcoeffPt944, 'Beam':massAttcoeffPt118}
    listOfMaterials.append(material('Cu',8.96))
    
    #listOfMaterials.append(mat2)
    listOfMaterials[0].readName()
    listOfMaterials[0].myDictionary={'Cu':massAttcoeffCu804, 'Pt':massAttcoeffCu944, 'Beam':massAttcoeffCu118}
    listOfMaterials[0].setPathToProjections(nameCu)
    listOfMaterials.append(material('Pt',21.45))
    listOfMaterials[1].readName()
    listOfMaterials[1].myDictionary={'Cu':massAttcoeffPt804, 'Pt':massAttcoeffPt944, 'Beam':massAttcoeffPt118}
    listOfMaterials[1].setPathToProjections(namePt)
    print 'number of materials',len(listOfMaterials), listOfMaterials[i].pathToProjections
    print  listOfMaterials[1].myDictionary['Cu']
    #raw_input("Press Enter to continue...")
    '''
    width=86
    height=10
    depthProjections=181
    tomoCentre=23
    #name="/home/xfz42935/Documents/Vortex/Merlin/merlinProjections.hdf"
    
    #name="/dls/i13-1/data/2017/cm16785-1/processing/VortexTomo/vortexProjectionsPtAttenuation.hdf"
    nameMerlinTomo="/dls/i13-1/data/2017/cm16785-1/processing/merlinTomo/merlinTomo2702.hdf"

    #name="/dls/i13-1/data/2017/cm16785-1/processing/VortexTomo/vortexProjectionsPtAttenuation.hdf"
    #vortexIm=h5py.File(name,"w")
    #dsetImage=vortexIm.create_dataset('data', (depthProjections,height,width), 'f')
    #print dsetImage.shape
    #print dsetImage.dtype
    #count=0
    #imageVortex=np.zeros(((depthProjections,height,width)))
    #myMax=0
    minFluoSignal=1
    projShift=20
    AttenuationCorrection(listOfMaterials,nameMerlinTomo,'data',tomoCentre, minFluoSignal, projShift)