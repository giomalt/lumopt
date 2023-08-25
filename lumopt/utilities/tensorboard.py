import logging
import os
import subprocess

import numpy as np
from torch.utils.tensorboard import SummaryWriter


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

    def log_data(self, iteration: int, fom: float, parameters: list, gradients: list):
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
        # Extract values of last iteration 
        fom = np.abs(np.array(fom[-1]))
        parameters = np.abs(np.array(parameters[-1]))
        gradients = np.abs(np.array(gradients[-1]))
        # Log data to TensorBoard
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

    def close(self):
        self.process.terminate()


if __name__ == "__main__":
    folder = rf'C:\Users\t-gmaltese\code\OSD\workflows\photonics\head\lumopt'
    board = Board(os.path.join(folder, 'tensorboard'))
    board.log_data(0, 90, [1,2,3], [4,5,6,7])
    board.log_data(1, 10, [2,1,3], [8,5,4,1])