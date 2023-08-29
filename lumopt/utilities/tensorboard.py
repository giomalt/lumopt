import logging
import os
import subprocess

import matplotlib.pyplot as plt
import numpy as np
from lumopt.utilities.gradients import GradientFields
from scipy.constants import nano
from torch.utils.tensorboard import SummaryWriter


def plot_geometry(points: np.array):
    """
    Plot the device geometry.

    Args:
        points (np.array): Array of points defining the geometry.

    Returns:
        fig: Figure object.
    """
    points=np.reshape(points,(-1,2))
    x_p=points[:,0]/nano
    y_p=points[:,1]/nano
    fig, ax = plt.subplots()
    ax.plot(x_p,y_p)
    ax.set_title('Geometry')
    ax.set_ylim(min(y_p),max(y_p))
    ax.set_xlim(min(x_p),max(x_p))
    ax.set_xlabel('x (um)')
    ax.set_ylabel('y (um)')
    return fig


def plot_gradients(gradients: GradientFields, original_grid: bool = True):
    """
    Plot the gradients.

    Args:
        gradients (Gradients): Gradients object.
        original_grid (bool): Indicates if we should plot the gradients on the original grid or on a
                                regular grid.

    Returns:
        fig: Figure object.
    """

    fig, ax_gradients = plt.subplots()
    if original_grid:
        x = gradients.forward_fields.x
        y = gradients.forward_fields.y
    else:
        x = np.linspace(min(gradients.forward_fields.x), max(gradients.forward_fields.x), 50)
        y = np.linspace(min(gradients.forward_fields.x), max(gradients.forward_fields.y), 50)
    xx, yy = np.meshgrid(x[1:-1], y[1:-1])

    z = (min(gradients.forward_fields.z) + max(gradients.forward_fields.z))/2
    wl = gradients.forward_fields.wl[0]
    Sparse_pert = [gradients.sparse_perturbation_field(x, y, z, wl) for x, y in zip(xx, yy)]

    im = ax_gradients.pcolormesh(xx/nano, yy/nano, Sparse_pert, cmap = plt.get_cmap('bwr'))
    ax_gradients.set_title('Sparse perturbation gradient fields')
    ax_gradients.set_xlabel('x (nm)')
    ax_gradients.set_ylabel('y (nm)')
    return fig


def plot_eps(gradients: GradientFields):
    """
    Plot the permittivity.

    Args:
        gradients (Gradients): Gradients object.

    Returns:
        fig: Figure object.    
    """
    fig, ax_eps = plt.subplots()
    x = gradients.forward_fields.x
    y = gradients.forward_fields.y
    eps = gradients.forward_fields.eps[:,:,0,0,0]
    xx, yy = np.meshgrid(x, y)

    im = ax_eps.pcolormesh(xx/nano, yy/nano, np.real(np.transpose(eps)))#, cmap=plt.get_cmap('bwr'))
    ax_eps.set_xlim((np.amin(x)/nano,np.amax(x)/nano))
    ax_eps.set_ylim((np.amin(y)/nano,np.amax(y)/nano))

    #fig.colorbar(im,ax = ax_gradients)
    ax_eps.set_title('Eps')
    ax_eps.set_xlabel('x (nm)')
    ax_eps.set_ylabel('y (nm)')
    return fig


class Board:
    '''
        Send the figure of merit, parameters and gradients to TensorBoard to plot. 

        Parameters
        ----------
        :param plot_history      Indicates if we should plot the history of the parameters and gradients. Should
                                 be set to False for large (e.g. >100) numbers of parameters 
    '''
    def __init__(self, folder: str):
        self.writer = SummaryWriter(folder)
        self.process = subprocess.Popen(["tensorboard", "--logdir", folder])

    def log_data(self,
                 iteration: int,
                 fom: float,
                 parameters: list,
                 gradients: list):
        """
        Log data to TensorBoard.
        The board can be accessed at http://localhost:6006/.
        We take the absolute value of data to plot it in log scale along y.

        Args:
            iteration (int): Iteration number.
            fom (float): Figure of merit.
            parameters (list): List of parameters.
            gradients (list): List of gradients.
        """
        fom = np.abs(np.array(fom[-1]))
        parameters = np.abs(np.array(parameters[-1]))
        gradients = np.abs(np.array(gradients[-1]))
        logging.debug(f"Logging data to TensorBoard:")
        logging.debug(f"iteration {iteration}")
        logging.debug(f"fom {fom}")
        logging.debug(f"parameters {parameters}")
        logging.debug(f"gradients {gradients}")
        self.writer.add_scalar("fom", fom, iteration)
        params_dict = dict(zip([f"{i}" for i in range(len(parameters))], parameters))
        self.writer.add_scalars("parameters", params_dict, iteration)
        gradients_dict = dict(zip([f"{i}" for i in range(len(gradients))], gradients))
        self.writer.add_scalars("gradients", gradients_dict, iteration)           
        self.writer.flush()
        
    def log_data2d(self, points: np.array, gradients: GradientFields):
        """
        Log 2D data to TensorBoard. It logs:
        - The 2D geometry of the device.
        - The 2D gradients field.
        """
        fig_geometry = plot_geometry(points)
        fig_gradients = plot_gradients(gradients)
        fig_permittivity = plot_eps(gradients)
        logging.debug(f"Logging to TensorBoard: geometry, gradients and permittivity.")
        self.writer.add_figure('Geometry', fig_geometry)
        self.writer.add_figure('Gradients', fig_gradients)
        self.writer.add_figure('Permittivity', fig_permittivity)
        self.writer.flush()
    
    def close(self):
        self.writer.close()
        self.process.terminate()


if __name__ == "__main__":
    folder = rf'C:\Users\t-gmaltese\code\OSD\workflows\photonics\head\lumopt'
    board = Board(os.path.join(folder, 'tensorboard'))
    board.log_data(0, 90, [1,2,3], [4,5,6,7])
    board.log_data(1, 10, [2,1,3], [8,5,4,1])