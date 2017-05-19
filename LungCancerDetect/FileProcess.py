import dicom,os
import numpy as np
import SimpleITK as sitk
import numpy as np
import csv
import os
from PIL import Image
import matplotlib.pyplot as plt
#this is class read dicom file
class FileProcess:
    def load_scan(path):
        slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
        slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))
        try:
            slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
        except:
            slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

        for s in slices:
            s.SliceThickness = slice_thickness

        return slices

    def load_itk_image(filename):
        itkimage = sitk.ReadImage(filename)
        numpyImage = sitk.GetArrayFromImage(itkimage)

        numpyOrigin = np.array(list(reversed(itkimage.GetOrigin())))
        numpySpacing = np.array(list(reversed(itkimage.GetSpacing())))

        return numpyImage, numpyOrigin, numpySpacing

