__author__ = 'khiem'
import os
import dicom
import numpy as np
import csv
import  SimpleITK as sitk

class FileProcess:

    #load dicom image
    def load_dicom_image(path):
        slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
        slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))
        try:
            slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
        except:
            slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

        for s in slices:
            s.SliceThickness = slice_thickness

        return slices

    #read itk file
    def load_itk_image(filename):
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

