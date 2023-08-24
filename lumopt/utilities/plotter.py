""" Copyright chriskeraly
    Copyright (c) 2019 Lumerical Inc. """

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation
from matplotlib.animation import FileMovieWriter

class SnapShots(FileMovieWriter):
    ''' Grabs the image information from the figure and saves it as a movie frame. '''

    supported_formats = ['png', 'jpeg', 'pdf']

    def __init__(self, *args, extra_args = None, **kwargs):
        super().__init__(*args, extra_args = (), **kwargs) # stop None from being passed

    def setup(self, fig, dpi, frame_prefix):
        super().setup(fig, dpi, frame_prefix, clear_temp = False)
        self.fname_format_str = '%s%%d.%s'
        self.temp_prefix, self.frame_format = self.outfile.split('.')

    # def grab_frame(self, **fig_kwargs):
    #     ''' All keyword arguments in fig_kwargs are passed on to the 'savefig' command that saves the figure. '''
    #     with self._frame_sink() as myframesink:
    #         self.fig.savefig(myframesink, format = self.frame_format, dpi = self.dpi, **fig_kwargs)

    def finish(self):
        pass
        # self._frame_sink().close()

class Plotter(object):
    '''
        Orchestrates the generation of plots during the optimization.

        Parameters
        ----------
        :param movie:            Indicates if the evolution of parameters should be recorded as a movie
        :param plot_history      Indicates if we should plot the history of the parameters and gradients. Should
                                 be set to False for large (e.g. >100) numbers of parameters 
    '''

    def __init__(self, movie = True, plot_history = True):
        self.plot_history = plot_history

        if plot_history:
            self.fig, self.ax = plt.subplots(nrows=2, ncols=3, figsize=(12, 7))
        else:
            self.fig, self.ax = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))

        self.fig.show()
        self.movie = movie
        if movie:
            metadata = dict(title = 'Optimization', artist='lumopt', comment = 'Continuous adjoint optimization')
            self.writer = SnapShots(fps = 2, metadata = metadata)

    def update(self, optimization):
        if self.plot_history:
            optimization.optimizer.plot(fomax=self.ax[0,0], paramsax=self.ax[0,2], gradients_ax=self.ax[1,2])
        else:
            optimization.optimizer.plot(fomax=self.ax[0,0], paramsax=None, gradients_ax=None)

        if hasattr(optimization, 'optimizations'):
            for i,opt in enumerate(optimization.optimizations):
                if hasattr(opt, 'gradient_fields'):
                    if not opt.geometry.plot(self.ax[1,0]):
                        opt.gradient_fields.plot_eps(self.ax[1,0])
                    opt.gradient_fields.plot(self.fig, self.ax[1,1], self.ax[0,1])
                print('Plots updated with optimization {0} iteration {1} results'.format(i, optimization.optimizer.iteration - 1))
        else:
            if hasattr(optimization, 'gradient_fields'):
                if not optimization.geometry.plot(self.ax[1,0]):
                    optimization.gradient_fields.plot_eps(self.ax[1,0])
                optimization.gradient_fields.plot(self.fig, self.ax[1,1], self.ax[0,1])
            print('Plots updated with iteration {} results'.format(optimization.optimizer.iteration - 1))
        plt.tight_layout()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        if self.movie:
            self.writer.grab_frame()
            print('Saved frame')


