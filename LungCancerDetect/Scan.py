import numpy as np
from FileProcess import FileProcess  as fp
from ImagesProcess import ImageProcess as ip
from Candidates import Candidates as cand
from  PlotViewer import PlotViewer as pv
from Segmentation import Segmentation as se
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons


import Config as cf
import matplotlib.pyplot as plt
class Scan:
    @classmethod
    def load_all_dicom_images(self,path="", verbose=True,annotation_groups=None):
        images = fp.load_dicom_image(path)

        fig = plt.figure(figsize=(16, 8))
        current_slice = int(len(images) / 2)

        ax_image = fig.add_axes([0.5, 0.0, 0.5, 1.0])
        img = ax_image.imshow(images[current_slice].pixel_array,
                              cmap=plt.cm.gray)

        ax_image.set_xlim(-0.5, 511.5);
        ax_image.set_ylim(511.5, -0.5)
        ax_image.axis('off')

        # Add annotation indicators if necessary.
        if annotation_groups is not None:
            nnods = len(annotation_groups)
            centroids = [np.array([a.centroid() for a in group]).mean(0)
                         for group in annotation_groups]
            radii = [np.mean([a.estimate_diameter() / 2 for a in group])
                     for group in annotation_groups]

            arrows = []
            for i in range(nnods):
                r = radii[i]
                c = centroids[i]
                s = '%d Annotations' % len(annotation_groups[i])
                a = ax_image.annotate(s,
                                      xy=(c[0] - r, c[1] - r),
                                      xytext=(c[0] - 50, c[1] - 50),
                                      bbox=dict(fc='w', ec='r'),
                                      arrowprops=dict(arrowstyle='->',
                                                      edgecolor='r'))
                a.set_visible(False)  # flipped on/off by `update` function.
                arrows.append(a)

        ax_scan_info = fig.add_axes([0.1, 0.8, 0.3, 0.1])  # l,b,w,h
        ax_scan_info.set_facecolor('w')
        SliceThickness = (images[0].SliceThickness )
        print  SliceThickness
        PixelSpacing=  (images[0].PixelSpacing)
        print PixelSpacing[0]
        scan_info_table = ax_scan_info.table(cellText=[
            ['Patient ID:',images[0].PatientID],
            ['Slice thickness:', '%.3f mm' %SliceThickness],
            ['Pixel spacing:', '%.3f mm' %PixelSpacing[0]]
        ],
            loc='center', cellLoc='left'
        )
        # Remove the table cell borders.
        for cell in scan_info_table.properties()['child_artists']:
            cell.set_color('w')
        # Add title, remove ticks from scan info.
        ax_scan_info.set_title('Scan Info')
        ax_scan_info.set_xticks([])
        ax_scan_info.set_yticks([])

        # If annotation_groups are provided, give a info table for them.
        if annotation_groups is not None and nnods != 0:
            # The values here were chosen heuristically.
            ax_ann_grps = fig.add_axes([0.1, 0.45 - nnods * 0.01,
                                        0.3, 0.2 + 0.01 * nnods])
            txt = [['Num Nodules:', str(nnods)]]
            for i in range(nnods):
                c = centroids[i]
                g = annotation_groups[i]
                txt.append(['Nodule %d:' % (i + 1),
                            '%d annotations, near z=%.2f' % (len(g), c[2])])
            ann_grps_table = ax_ann_grps.table(cellText=txt, loc='center',
                                               cellLoc='left')
            # Remove cell borders.
            for cell in ann_grps_table.properties()['child_artists']:
                cell.set_color('w')
            # Add title, remove ticks from scan info.
            ax_ann_grps.set_title('Nodule Info')
            ax_ann_grps.set_xticks([])
            ax_ann_grps.set_yticks([])

        # Add the widgets.
        ax_slice = fig.add_axes([0.1, 0.1, 0.3, 0.05])
        ax_slice.set_facecolor('w')
        z = float(images[current_slice].ImagePositionPatient[-1])
        sslice = Slider(ax_slice, 'Z: %.3f' % z, 0, len(images) - 1,
                        valinit=current_slice, valfmt=u'Slice: %d')

        def update(_):
            # Update image itself.
            current_slice = int(sslice.val)
            img.set_data(images[current_slice].pixel_array)

            # Update `z` label.
            z = float(images[current_slice].ImagePositionPatient[-1])
            sslice.label.set_text('Z: %.3f' % z)

            # Show annotation labels if possible.
            if annotation_groups is not None:
                for i in range(len(annotation_groups)):
                    dist = abs(z - centroids[i][2])
                    arrows[i].set_visible(dist <= 3 * self.slice_thickness)

            fig.canvas.draw_idle()

        sslice.on_changed(update)
        update(None)
        plt.show()
    @classmethod
    def dicom_images(self,images, verbose=True,annotation_groups=None):
      #  images = fp.load_dicom_image(path)

        fig = plt.figure(figsize=(16, 8))
        current_slice = int(len(images) / 2)

        ax_image = fig.add_axes([0.5, 0.0, 0.5, 1.0])
        img = ax_image.imshow(images[current_slice].pixel_array,
                              cmap=plt.cm.gray)

        ax_image.set_xlim(-0.5, 511.5);
        ax_image.set_ylim(511.5, -0.5)
        ax_image.axis('off')

        # Add annotation indicators if necessary.
        if annotation_groups is not None:
            nnods = len(annotation_groups)
            centroids = [np.array([a.centroid() for a in group]).mean(0)
                         for group in annotation_groups]
            radii = [np.mean([a.estimate_diameter() / 2 for a in group])
                     for group in annotation_groups]

            arrows = []
            for i in range(nnods):
                r = radii[i]
                c = centroids[i]
                s = '%d Annotations' % len(annotation_groups[i])
                a = ax_image.annotate(s,
                                      xy=(c[0] - r, c[1] - r),
                                      xytext=(c[0] - 50, c[1] - 50),
                                      bbox=dict(fc='w', ec='r'),
                                      arrowprops=dict(arrowstyle='->',
                                                      edgecolor='r'))
                a.set_visible(False)  # flipped on/off by `update` function.
                arrows.append(a)

        ax_scan_info = fig.add_axes([0.1, 0.8, 0.3, 0.1])  # l,b,w,h
        ax_scan_info.set_facecolor('w')
        SliceThickness = (images[0].SliceThickness )
        print  SliceThickness
        PixelSpacing=  (images[0].PixelSpacing)
        print PixelSpacing[0]
        scan_info_table = ax_scan_info.table(cellText=[
            ['Patient ID:',images[0].PatientID],
            ['Slice thickness:', '%.3f mm' %SliceThickness],
            ['Pixel spacing:', '%.3f mm' %PixelSpacing[0]]
        ],
            loc='center', cellLoc='left'
        )
        # Remove the table cell borders.
        for cell in scan_info_table.properties()['child_artists']:
            cell.set_color('w')
        # Add title, remove ticks from scan info.
        ax_scan_info.set_title('Scan Info')
        ax_scan_info.set_xticks([])
        ax_scan_info.set_yticks([])

        # If annotation_groups are provided, give a info table for them.
        if annotation_groups is not None and nnods != 0:
            # The values here were chosen heuristically.
            ax_ann_grps = fig.add_axes([0.1, 0.45 - nnods * 0.01,
                                        0.3, 0.2 + 0.01 * nnods])
            txt = [['Num Nodules:', str(nnods)]]
            for i in range(nnods):
                c = centroids[i]
                g = annotation_groups[i]
                txt.append(['Nodule %d:' % (i + 1),
                            '%d annotations, near z=%.2f' % (len(g), c[2])])
            ann_grps_table = ax_ann_grps.table(cellText=txt, loc='center',
                                               cellLoc='left')
            # Remove cell borders.
            for cell in ann_grps_table.properties()['child_artists']:
                cell.set_color('w')
            # Add title, remove ticks from scan info.
            ax_ann_grps.set_title('Nodule Info')
            ax_ann_grps.set_xticks([])
            ax_ann_grps.set_yticks([])

        # Add the widgets.
        ax_slice = fig.add_axes([0.1, 0.1, 0.3, 0.05])
        ax_slice.set_facecolor('w')
        z = float(images[current_slice].ImagePositionPatient[-1])
        sslice = Slider(ax_slice, 'Z: %.3f' % z, 0, len(images) - 1,
                        valinit=current_slice, valfmt=u'Slice: %d')

        def update(_):
            # Update image itself.
            current_slice = int(sslice.val)
            img.set_data(images[current_slice].pixel_array)

            # Update `z` label.
            z = float(images[current_slice].ImagePositionPatient[-1])
            sslice.label.set_text('Z: %.3f' % z)

            # Show annotation labels if possible.
            if annotation_groups is not None:
                for i in range(len(annotation_groups)):
                    dist = abs(z - centroids[i][2])
                    arrows[i].set_visible(dist <= 3 * self.slice_thickness)

            fig.canvas.draw_idle()

        sslice.on_changed(update)
        update(None)
        plt.show()

sc = Scan().load_all_dicom_images(cf.INPUT_FOLDER_ITK)