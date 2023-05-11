#!/usr/bin/env python3
from xpdeint.XSILFile import XSILFile
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import copy
import numpy as np
from colorspacious import cspace_convert # https://stackoverflow.com/a/50860105
import matplotlib.ticker as mticker


class Figure():
  def __init__(self, video=False, snapshots=False):
    
    self.import_data()
    
    self.video = video
    self.snapshots = snapshots

    self.set_params()
    self.gen_colormap()
    self.prepare_xy()

    self.fig, self.ax = self.set_up_fig()

    self.plot_first_last()

    if self.video or self.snapshots:
      self.gen_video()
    
  def __delete__(self):
    plt.close()

  def import_data(self):
    xsilFile = XSILFile("actin.xsil")

    def firstElementOrNone(enumerable):
      for element in enumerable:
        return element
      return None

    self.t = firstElementOrNone(_["array"] for _ in xsilFile.xsilObjects[0].independentVariables if _["name"] == "t")
    self.x = firstElementOrNone(_["array"] for _ in xsilFile.xsilObjects[0].independentVariables if _["name"] == "x")
    self.y = firstElementOrNone(_["array"] for _ in xsilFile.xsilObjects[0].independentVariables if _["name"] == "y")
    self.c = firstElementOrNone(_["array"] for _ in xsilFile.xsilObjects[0].dependentVariables if _["name"] == "CR")
    self.nx = firstElementOrNone(_["array"] for _ in xsilFile.xsilObjects[0].dependentVariables if _["name"] == "N1R")
    self.ny = firstElementOrNone(_["array"] for _ in xsilFile.xsilObjects[0].dependentVariables if _["name"] == "N2R")

  def set_params(self):
    self.fig_size_w = 16
    self.fig_size_h = 7

    self.quiver_scale = 0.25

    self.skip=self.x.shape[0]//50

    if self.skip == 0 : self.skip = 1

  def gen_colormap(self):
    color_circle = np.ones((256,3))*60
    color_circle[:,1] = np.ones((256))*45
    color_circle[:,2] = np.arange(0,360,360/256)
    color_circle_rgb = cspace_convert(color_circle, "JCh","sRGB1")

    self.cm = colors.ListedColormap(color_circle_rgb)

  def get_cmap_bounds(self, idx):
    self.cmap_min = self.c[idx,:,:].min()
    self.cmap_max = self.c[idx,:,:].max()

  def prepare_xy(self):
    x_pix_len = (self.x[-1] - 2*self.x[0] + self.x[1])/(self.x.shape[0])
    self.half_x_pix_len = x_pix_len/2

    y_pix_len = (self.y[-1] - 2*self.y[0] + self.y[1])/(self.y.shape[0])
    self.half_y_pix_len = y_pix_len/2

    self.xs=self.x[::self.skip]
    self.ys=self.y[::self.skip]

    self.L = self.x[-1] - self.x[0] + (self.x[1] - self.x[0])
    self.dL = self.x[1] - self.x[0]

  def set_up_fig(self):
    matplotlib.rcParams["image.origin"] = 'upper'

    fig, ax = plt.subplots(2, 3,
                          layout="constrained",
                          figsize=(self.fig_size_w, self.fig_size_h),
                          gridspec_kw={ 'height_ratios': [1, 0.025],
                                        'width_ratios': [1,1,1],
                                        'hspace': 0.0001}) 

    ax[0,0].set_aspect('equal')
    ax[0,1].set_aspect('equal')
    ax[0,2].set_aspect('equal')

    ax[0,0].set_xticks([])
    ax[0,0].set_yticks([])

    ax[0,1].set_xticks([])
    ax[0,1].set_yticks([])

    ax[0,2].set_xticks([])
    ax[0,2].set_yticks([])


    ax[0,0].set( xlim=( self.x[0]  -  self.half_x_pix_len, 
                        self.x[-1] + self.half_x_pix_len), 
                 ylim=( self.y[0]  -  self.half_y_pix_len, 
                        self.y[-1] + self.half_y_pix_len) )

    ax[0,1].set( xlim=( self.x[0]  -  self.half_x_pix_len, 
                        self.x[-1] + self.half_x_pix_len), 
                 ylim=( self.y[0]  -  self.half_y_pix_len, 
                        self.y[-1] + self.half_y_pix_len) )

    ax[0,2].set( xlim=( self.x[0] -  self.half_x_pix_len, 
                        self.x[-1] + self.half_x_pix_len), 
                 ylim=( self.y[0] -  self.half_y_pix_len, 
                        self.y[-1] + self.half_y_pix_len) )                    

    ax[1,0].axis('off')
    ax[1,2].axis('off')

    return (fig, ax)

  def plot_data(self, idx, fname_str):
    self.nxs=self.nx[idx, ::-self.skip, ::self.skip]
    self.nys=self.ny[idx, ::-self.skip, ::self.skip]

    self.get_cmap_bounds(idx)

    self.im = self.ax[0,0].quiver(self.xs, self.ys, 
                                  self.nxs, self.nys, 
                                  np.arctan2(self.nys, self.nxs), 
                                  scale=self.quiver_scale, scale_units='xy',
                                  cmap=self.cm)

    self.im2 = self.ax[0,1].imshow(self.c[idx,:,:], cmap="gist_yarg",
                                   extent=[ self.x.min() - self.half_x_pix_len, 
                                           self.x.max() + self.half_x_pix_len, 
                                           self.y.min() - self.half_y_pix_len, 
                                           self.y.max() + self.half_y_pix_len],
                                   vmin=self.cmap_min, vmax=self.cmap_max)

    self.im3_q = self.ax[0,2].quiver(self.xs, self.ys, 
                                     self.nxs, self.nys, 
                                     np.arctan2(self.nys, self.nxs), 
                                     scale=self.quiver_scale, scale_units='xy', 
                                     cmap=self.cm)

    self.im3_i = self.ax[0,2].imshow(self.c[idx,:,:], cmap="gist_yarg",
                                    extent=[ self.x.min() - self.half_x_pix_len, 
                                            self.x.max() + self.half_x_pix_len, 
                                            self.y.min() - self.half_y_pix_len, 
                                            self.y.max() + self.half_y_pix_len],
                                    vmin=self.cmap_min, vmax=self.cmap_max)

    self.ax[0,0].set_title("director field", y=0, pad=-20)
    self.ax[0,1].set_title("concentration", y=0, pad=-20)
    self.ax[0,2].set_title("composite", y=0, pad=-20)

    self.fig.suptitle(f't = {self.t[idx]:.2f}\nL = {self.L:.1f}, dL = {self.dL:.1f}')

    cbar = plt.colorbar(self.im2, cax=self.ax[1,1], 
                        orientation='horizontal', 
                        ticks=mticker.LinearLocator(numticks=5),
                        extend="both", extendfrac=0.1, extendrect=True)

    cbar.formatter.set_powerlimits((0, 0))

    # to get 10^3 instead of 1e3
    cbar.formatter.set_useMathText(True)

    fname = fname_str + ".png"

    plt.savefig(fname, dpi="figure", format="png")

    print(f'frame {idx} snapshot saved')

  def plot_first_last(self):
    self.fig, self.ax = self.set_up_fig()
    self.plot_data(0, "first")

    plt.close()

    self.fig, self.ax = self.set_up_fig()
    self.plot_data(-1, "last")

  def gen_video(self):
    def updatefig(j):
      self.fig.suptitle(f't = {self.t[j]:.2f}\nL = {self.L:.1f}, dL = {self.dL:.1f}')

      U=self.nx[j,::-self.skip,::self.skip]
      V=self.ny[j,::-self.skip,::self.skip]

      self.im.set_UVC(U, V, C=np.arctan2(V,U))
      self.im3_q.set_UVC(U, V, C=np.arctan2(V,U))

      C = self.c[j,:,:]

      # loc = mticker.LinearLocator(numticks=5)
      # print(type(loc))

      # breakpoint()

      # cmin = loc()[0]
      # cmax = loc()[1]
      # ntix = loc()[2]

      tick_pad = 0 #(cmax - cmin)/(ntix*2)

      self.im2.set_data(C)
      self.im2.autoscale()
      # self.im2.set_clim([cmin - tick_pad, cmax + tick_pad])


      self.im3_i.set_data(C)
      self.im3_i.autoscale()
      # self.im3_i.set_clim([cmin - tick_pad, cmax + tick_pad])

      if self.snapshots:
        fname = str(j)+".png"
        plt.savefig(fname, dpi="figure", format="png")

      return [self.im]

    ani = animation.FuncAnimation(self.fig, updatefig, frames=range(self.nx.shape[0]), interval=10, repeat=False)

    if self.snapshots:
      print("snapshots saved")

    if self.video:
      writer_video = animation.FFMpegWriter(fps=5)
      ani.save("movie.mp4", writer=writer_video,dpi=300)

      print("movie saved")
    
myFig = Figure(video=True)
del(myFig)
