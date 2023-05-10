#!/usr/bin/env python3
from xpdeint.XSILFile import XSILFile

xsilFile = XSILFile("actin.xsil")

def firstElementOrNone(enumerable):
  for element in enumerable:
    return element
  return None

t_1 = firstElementOrNone(_["array"] for _ in xsilFile.xsilObjects[0].independentVariables if _["name"] == "t")
x_1 = firstElementOrNone(_["array"] for _ in xsilFile.xsilObjects[0].independentVariables if _["name"] == "x")
y_1 = firstElementOrNone(_["array"] for _ in xsilFile.xsilObjects[0].independentVariables if _["name"] == "y")
CR_1 = firstElementOrNone(_["array"] for _ in xsilFile.xsilObjects[0].dependentVariables if _["name"] == "CR")
N1R_1 = firstElementOrNone(_["array"] for _ in xsilFile.xsilObjects[0].dependentVariables if _["name"] == "N1R")
N2R_1 = firstElementOrNone(_["array"] for _ in xsilFile.xsilObjects[0].dependentVariables if _["name"] == "N2R")
# t_2 = firstElementOrNone(_["array"] for _ in xsilFile.xsilObjects[1].independentVariables if _["name"] == "t")
# CtotR_2 = firstElementOrNone(_["array"] for _ in xsilFile.xsilObjects[1].dependentVariables if _["name"] == "CtotR")

# Write your plotting commands here.
# You may want to import pylab (from pylab import *) or matplotlib (from matplotlib import *)
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import copy
import numpy as np
from colorspacious import cspace_convert # https://stackoverflow.com/a/50860105

color_circle = np.ones((256,3))*60
color_circle[:,1] = np.ones((256))*45
color_circle[:,2] = np.arange(0,360,360/256)
color_circle_rgb = cspace_convert(color_circle, "JCh","sRGB1")

cm = colors.ListedColormap(color_circle_rgb)

fig, ax = plt.subplots()

skip=x_1.shape[0]//100

# box_bounds = 15

x_last=x_1[::skip]
y_last=y_1[::skip]

nx_last=np.fliplr(N1R_1[0,::-skip,::-skip])
ny_last=np.fliplr(N2R_1[0,::-skip,::-skip])

n_mag = 1#np.sqrt(nx_last**2 + ny_last**2)
c_r = CR_1[-1,:,:]

print(CR_1[0,:,:].sum())

norm = 1 # c_r.sum()

cmap_min = c_r.min()/norm
cmap_max = c_r.max()/norm

# print(cmap_min, cmap_max)

im = ax.quiver(y_last, x_last, nx_last/n_mag, ny_last/n_mag, np.arctan2(ny_last, nx_last), scale=0.2, scale_units='xy',cmap=cm)
im2 = ax.imshow(c_r/norm, cmap="gist_yarg",extent=[x_1.min(),x_1.max(),y_1.min(),y_1.max()], vmin=cmap_min, vmax=cmap_max)
fig.colorbar(im2, ax=ax)

plt.xticks([])
plt.yticks([])

t_steps = N1R_1.shape[0] -1

def updatefig(j):
  U=np.fliplr(N1R_1[j,::-skip,::-skip])
  V=np.fliplr(N2R_1[j,::-skip,::-skip])

  mag = 1#np.sqrt(U**2 + V**2)
  im.set_UVC(U, V, C=np.arctan2(V,U))

  plt.title(f't = {t_1[j]:.2f}')

  C = CR_1[j,:,:]

  norm =  1 # C.sum()

  im2.set_data(C/norm)
  im2.autoscale()

  return [im]

ani = animation.FuncAnimation(fig, updatefig, frames=range(N1R_1.shape[0]), interval=10, repeat=False)

writer_video = animation.FFMpegWriter(fps=5)
ani.save("movie.mp4", writer=writer_video,dpi=300)

# plt.show()
# plt.draw()
# ani.save(filename="movie.gif", writer="imagemagick")
# ani2.save(filename='movie.gif', writer='imagemagick')
# plt.show()
# 

plt.close()


fig2, ax2 = plt.subplots() 

plt.xlabel("time")
plt.ylabel("total concentration")

ax2.scatter(t_1, CR_1.sum(axis=(1,2)))


plt.savefig("conc.png", dpi="figure", format="png")

print(CR_1.min())

