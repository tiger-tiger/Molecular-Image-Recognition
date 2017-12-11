import os
import numpy as np
from lines_to_graph import *
from adjacency import *
from line import *
import matplotlib.pyplot as plt
from copy import deepcopy
from skimage.feature import canny
from skimage.io import imread
from rmgpy.molecule.molecule import Molecule
from skimage.filters import threshold_otsu

#image = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'hough_test', 'hexagon.JPG')
#image = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'hough_test', 'PDD.png')
#image = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'hough_test', 'Test_Set_1', 'PNGs',
#                     'C(C)C(CCCC)(C)C.png')

#image = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'hough_test', 'Test_Set_1', 'PNGs',
 #                    'C(C)(CC)(CC)CCCCC.png')
#image = os.path.join(os.path.dirname(os.path.dirname(__file__)),'data','hough_test','short test set','C(C)(CC)(CC)CCCCC.png')
#image = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'hough_test','square.jpg' )
#image = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'hough_test', 'Test_Set_1','double_bonds', 'C((CCC)CC)C.png')
image = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'hand_drawn', 'C1C(C1)CC=CC.png')

bname = os.path.basename(os.path.normpath(image))

smiles = bname.split('.')[0]
print smiles
m = Molecule().fromSMILES(str(smiles))

image = imread(image, as_grey=True)
thresh = threshold_otsu(image)
image = image > thresh
image = np.invert(image)
lines = get_hough_lines(image)

#    min_dist_merge = params[0]
#    min_angle_merge = params[1] 
#    min_width_merge = params[2]
#    split_tol = params[3]
#    min_dist_bond = params[4]
#    max_dist_bond = params[5]
#    max_angle_bond = params[6]
#    node_radius = params[7]
lines = lines_to_graph(lines, [0.05,0.4,.2,0.2,0.1,0.3,0.3,0.2])
#lines = lines_to_graph(lines_final, [0.05,.4,.1,0.2,0.06,0.8,0.1,.2])
print [line.order for line in lines]

for line in lines:
    plt.plot((line.pts[0].x, line.pts[1].x), (line.pts[0].y, line.pts[1].y))
#plt.xlim((0, get_image_size(image)[1]/imdim))
#plt.ylim(( get_image_size(image)[0]/imdim,0))
plt.figure()

for line in lines:
    plt.plot((line.pts[0].x, line.pts[1].x), (line.pts[0].y, line.pts[1].y))
#plt.xlim((0, get_image_size(image)[1]/imdim))
#plt.ylim(( get_image_size(image)[0]/imdim,0))

plt.title('Probabilistic Hough')


adj = getAdjMatrix(lines)

atomnames = ['C']*adj.shape[0]
molecule = Adjacency(adj, atomnames)
molecule.addHydrogens()
rmgmol = molecule.toRMGmol()

    
print m.isIsomorphic(rmgmol)

