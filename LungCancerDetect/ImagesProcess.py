import SimpleITK as sitk
import numpy as np
import csv
import os
from PIL import Image
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
class ImageProcess:
    PIXEL_MEAN = 0.25

    # Normalization
    MIN_BOUND = -1000.0
    MAX_BOUND = 400.0

    #convert world To voxel data
    def worldToVoxelCoord(worldCoord, origin, spacing):
        stretchedVoxelCoord = np.absolute(worldCoord - origin)
        voxelCoord = stretchedVoxelCoord / spacing
        return voxelCoord

    #normalize pixel value
    def normalizePlanes(npzarray):
        maxHU = 400.
        minHU = -1000.

        npzarray = (npzarray - minHU) / (maxHU - minHU)
        npzarray[npzarray > 1] = 1.
        npzarray[npzarray < 0] = 0.
        return npzarray

    #input : slices of an images of a patient .
    #output: only a array of a image
    def get_pixels_hu(slices):
        image = np.stack([s.pixel_array for s in slices])
        # Convert to int16 (from sometimes int16),
        # should be possible as values should always be low enough (<32k)
        image = image.astype(np.int16)

        # Set outside-of-scan pixels to 0
        # The intercept is usually -1024, so air is approximately 0
        image[image == -2000] = 0

        # Convert to Hounsfield units (HU)
        for slice_number in range(len(slices)):

            intercept = slices[slice_number].RescaleIntercept
            slope = slices[slice_number].RescaleSlope

            if slope != 1:
                image[slice_number] = slope * image[slice_number].astype(np.float64)
                image[slice_number] = image[slice_number].astype(np.int16)

            image[slice_number] += np.int16(intercept)

        return np.array(image, dtype=np.int16)

    #resample dicom images
    def resample(image, scan, new_spacing=[1,1,1]):
        # Determine current pixel spacing
        spacing = np.array([scan[0].SliceThickness] + scan[0].PixelSpacing, dtype=np.float32)

        resize_factor = spacing / new_spacing
        new_real_shape = image.shape * resize_factor
        new_shape = np.round(new_real_shape)
        real_resize_factor = new_shape / image.shape
        new_spacing = spacing / real_resize_factor

        image = scipy.ndimage.interpolation.zoom(image, real_resize_factor, mode='nearest')

        return image, new_spacing

    def zero_center(image):
        image = image - PIXEL_MEAN
        return image

