import h5py
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import copy
import numpy as np
from colorspacious import cspace_convert # pyth

f = h5py.File("input.h5")

for key in f.keys():

	data = f[key][()]

color_circle = np.ones((256,3))*60
color_circle[:,1] = np.ones((256))*45
color_circle[:,2] = np.arange(0,360,360/256)
color_circle_rgb = cspace_convert(color_circle, "JCh","sRGB1")

cm = colors.ListedColormap(color_circle_rgb)

fig, ax = plt.subplots()

skip = np.array(f['x']).shape[0]//50

if skip == 0:
    skip =1



x = np.array(f['x'])[::skip]
y = np.array(f['y'])[::skip]
nx = np.array(f['N1R'])[::-skip,::skip]
ny = np.array(f['N2R'])[::-skip,::skip]
c = np.array(f['CR'])[::skip,::skip]

dx = x[1]-x[0]
dy = y[1]-y[0]

im = ax.quiver(x, y, nx, ny, np.arctan2(ny, nx), scale=0.2, scale_units='xy',cmap=cm)
im2 = ax.imshow(c, cmap="gist_yarg",extent=[x.min()-dx/2, x.max()+dx/2, y.min()-dy/2, y.max()+dy/2])

cbar = fig.colorbar(im2, ax=ax)

plt.show()


# Write your plotting commands here.
# You may want to import pylab (from pylab import *) or matplotlib (from matplotlib import *)





