from FileProcess import FileProcess  as fp
from ImagesProcess import ImageProcess as ip
import Candidates as cand
from  PlotViewer import PlotViewer as pv
import Segmentation as seg
import Config as cf





first_patient = fp.load_dicom_image(cf.INPUT_FOLDER)
first_patient_pixels =ip.get_pixels_hu(first_patient)


pv.showsubplot(first_patient_pixels)


