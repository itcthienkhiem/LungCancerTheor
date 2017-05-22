__author__ = 'khiem'
import os
import dicom
import numpy as np
import csv
import  SimpleITK as sitk

class FileProcess:
    def __init__(self):
        print 'FileProcess'

    #load dicom image
    @classmethod
    def load_dicom_image(self,path):
        if not os.path.exists(path):
            raise  path
        slices=[]
        for s in os.listdir(path):

            ext = os.path.splitext(s)[-1].lower()
            if(ext=='.dcm'):
                slices.append(dicom.read_file(path + '/' + s) )

#        slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]

        slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))
        try:
            slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
        except:
            slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

        for s in slices:
            s.SliceThickness = slice_thickness

        return slices

    #read itk file
    def load_itk_image(self,filename):
        itkimage = sitk.ReadImage(filename)
        numpyImage = sitk.GetArrayFromImage(itkimage)

        numpyOrigin = np.array(list(reversed(itkimage.GetOrigin())))
        numpySpacing = np.array(list(reversed(itkimage.GetSpacing())))
        return numpyImage, numpyOrigin, numpySpacing

    #read CSV file
    def readCSV(filename):
        lines = []
        with open(filename, "rb") as f:
            csvreader = csv.reader(f)
            for line in csvreader:
                lines.append(line)
        return lines

    #save file matrix
    def saveMatrix(self, id,first_patient,first_patient_pixels):
        np.save("fullimages_%d.npy" % (0), self.first_patient)
        np.save("fullimages_%d.npy" % (1), self.first_patient_pixels)

    def loadMatrix(self,path):
        first_patient = self. load_dicom_image(path)
        first_patient_pixels = self.get_pixels_hu(first_patient)
        return first_patient,first_patient_pixels

