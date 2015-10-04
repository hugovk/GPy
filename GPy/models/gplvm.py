# Copyright (c) 2012-2014, GPy authors (see AUTHORS.txt).
# Licensed under the BSD 3-clause license (see LICENSE.txt)


import numpy as np
from .. import kern
from ..core import GP, Param
from ..likelihoods import Gaussian
from .. import util


class GPLVM(GP):
    """
    Gaussian Process Latent Variable Model


    """
    def __init__(self, Y, input_dim, init='PCA', X=None, kernel=None, name="gplvm"):

        """
        :param Y: observed data
        :type Y: np.ndarray
        :param input_dim: latent dimensionality
        :type input_dim: int
        :param init: initialisation method for the latent space
        :type init: 'PCA'|'random'
        """
        if X is None:
            from ..util.initialization import initialize_latent
            X, fracs = initialize_latent(init, input_dim, Y)
        else:
            fracs = np.ones(input_dim)
        if kernel is None:
            kernel = kern.RBF(input_dim, lengthscale=fracs, ARD=input_dim > 1) + kern.Bias(input_dim, np.exp(-2))

        likelihood = Gaussian()

        super(GPLVM, self).__init__(X, Y, kernel, likelihood, name='GPLVM')

        self.X = Param('latent_mean', X)
        self.link_parameter(self.X, index=0)

    def parameters_changed(self):
        super(GPLVM, self).parameters_changed()
        self.X.gradient = self.kern.gradients_X(self.grad_dict['dL_dK'], self.X, None)

    def plot_latent(self, labels=None, which_indices=None,
                resolution=50, ax=None, marker='o', s=40,
                fignum=None, legend=True,
                plot_limits=None,
                aspect='auto', updates=False, **kwargs):
        import sys
        assert "matplotlib" in sys.modules, "matplotlib package has not been imported."
        from ..plotting.matplot_dep import dim_reduction_plots

        return dim_reduction_plots.plot_latent(self, labels, which_indices,
                resolution, ax, marker, s,
                fignum, False, legend,
                plot_limits, aspect, updates, **kwargs)
