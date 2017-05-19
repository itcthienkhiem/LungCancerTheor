import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure, feature

import plotly.plotly as py
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.tools import FigureFactory as FF
from plotly.graph_objs import *
init_notebook_mode(connected=True)

import plotly
plotly.tools.set_credentials_file(username='itc.thienkhiem', api_key='3Gi4Cq30WDhUlPDG1aCh')

class PlotViewer:
    def plot_3d(image, threshold=-300):

        # Position the scan upright,
        # so the head of the patient would be at the top facing the camera
        p = image.transpose(2,1,0)

        verts, faces, normals, values = measure.marching_cubes(p, threshold)

        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Fancy indexing: `verts[faces]` to generate a collection of triangles
        mesh = Poly3DCollection(verts[faces], alpha=0.70)
        face_color = [0.45, 0.45, 0.75]
        mesh.set_facecolor(face_color)
        ax.add_collection3d(mesh)

        ax.set_xlim(0, p.shape[0])
        ax.set_ylim(0, p.shape[1])
        ax.set_zlim(0, p.shape[2])
        plt.show()


    #SHOW PILOT 2D WITH HOUNSFIELD UNITS HU
    def showsubplot(self,first_patient_pixels):
        # start: cach hien thi 2 do thi chung
        plt.subplot(1, 2, 1)
        plt.hist(self.first_patient_pixels.flatten(), bins=80, color='c')
        plt.xlabel("Hounsfield Units (HU)")
        plt.ylabel("Frequency")
        plt.subplot(1, 2, 2)
        # Show some slice in the middle
        plt.imshow(self.first_patient_pixels[80], cmap=plt.cm.gray, interpolation="none")
        plt.show()
        # end

    #SHOW PILOT 3D IN PLOTLY
    def plotly_3d(verts, faces,fn):
        x, y, z = zip(*verts)

        print "Drawing"

        # Make the colormap single color since the axes are positional not intensity.
        #    colormap=['rgb(255,105,180)','rgb(255,255,51)','rgb(0,191,255)']
        colormap = ['rgb(236, 236, 212)', 'rgb(236, 236, 212)']

        fig = FF.create_trisurf(x=x,
                                y=y,
                                z=z,
                                plot_edges=False,
                                colormap=colormap,
                                simplices=faces,
                                backgroundcolor='rgb(64, 64, 64)',
                                title="Interactive Visualization")
        py.iplot(fig, filename =fn)

