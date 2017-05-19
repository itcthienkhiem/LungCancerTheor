import numpy as np
from requests.api import patch

import  ImagesProcess as ip

class Candidates:

    #this is function get Candidates
    #input: cands: list of cands in excel file
    #numpyImage: image from local
    #numpyOrigin: Origin of images
    #numpySpacing: Spacing of images
    def getCandidates(self,cands,numpyImage,numpyOrigin,numpySpacing):
        #list of cands
        worldCoords  = []
        voxelCoords = []
        patchs = []
        #foreach to cands in excel
        for cand in cands[1:]:
            worldCoord = np.asarray([float(cand[3]), float(cand[2]), float(cand[1])])
            voxelCoord =ip. worldToVoxelCoord(worldCoord, numpyOrigin, numpySpacing)
            voxelWidth = 65
            patch = numpyImage[int(voxelCoord[0]),
                    int(voxelCoord[1] - voxelWidth / 2):int(voxelCoord[1] + voxelWidth / 2),
                    int(voxelCoord[2] - voxelWidth / 2):int(voxelCoord[2] + voxelWidth / 2)]
            patch =ip. normalizePlanes(patch)
            print 'data'
            print worldCoord
            print voxelCoord
            print patch
            worldCoords.append(worldCoord)
            voxelCoords.append(voxelCoord)
            patchs.append(patch)

            #save to file cands
            #outputDir = 'patches/'
            #plt.imshow(patch, cmap='gray')
            #plt.show()
            #Image.fromarray(patch * 255).convert('L').save(os.path.join(outputDir,
            #                                                           'patch_' + str(worldCoord[0]) + '_' + str(
            #                                                                worldCoord[1]) + '_' + str(
            #                                                               worldCoord[2]) + '.tiff'))
