#===============================================================================
# Copyright (c) 2012-2015, GPy authors (see AUTHORS.txt).
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of GPy nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#===============================================================================

import numpy as np

from . import pl
from .plot_util import helper_for_plot_data, update_not_existing_kwargs, \
    helper_predict_with_model, get_which_data_ycols
from .data_plots import _plot_data, _plot_inducing

def plot_mean(self, plot_limits=None, fixed_inputs=None,
              resolution=None, plot_raw=False,
              apply_link=False, visible_dims=None,
              which_data_ycols='all',
              levels=20,
              predict_kw=None,
              **kwargs):
    """
    Plot the mean of the GP.

    Give the Y_metadata in the predict_kw if you need it.
   
    
    :param plot_limits: The limits of the plot. If 1D [xmin,xmax], if 2D [[xmin,ymin],[xmax,ymax]]. Defaluts to data limits
    :type plot_limits: np.array
    :param fixed_inputs: a list of tuple [(i,v), (i,v)...], specifying that input dimension i should be set to value v.
    :type fixed_inputs: a list of tuples
    :param int resolution: The resolution of the prediction [defaults are 1D:200, 2D:50]
    :param bool plot_raw: plot the latent function (usually denoted f) only?
    :param bool apply_link: whether to apply the link function of the GP to the raw prediction.
    :param array-like which_data_ycols: which columns of y to plot (array-like or list of ints)
    :param dict predict_kw: the keyword arguments for the prediction. If you want to plot a specific kernel give dict(kern=<specific kernel>) in here
    :param int levels: for 2D plotting, the number of contour levels to use is 
    """
    canvas, kwargs = pl.get_new_canvas(kwargs)
    plots = _plot_mean(self, canvas, plot_limits, fixed_inputs, 
                       resolution, plot_raw, 
                       apply_link, visible_dims, which_data_ycols, levels, 
                       predict_kw, **kwargs)
    return pl.show_canvas(canvas, plots)

def _plot_mean(self, canvas, plot_limits=None, fixed_inputs=None,
              resolution=None, plot_raw=False,
              apply_link=False, visible_dims=None,
              which_data_ycols=None,
              levels=20, 
              predict_kw=None, **kwargs):
    _, _, _, _, free_dims, Xgrid, x, y, _, _, resolution = helper_for_plot_data(self, plot_limits, visible_dims, fixed_inputs, resolution)

    if len(free_dims)<=2:
        mu, _, _ = helper_predict_with_model(self, Xgrid, plot_raw, 
                                          apply_link, None, 
                                          get_which_data_ycols(self, which_data_ycols), 
                                          predict_kw)
        if len(free_dims)==1:
            # 1D plotting:
            update_not_existing_kwargs(kwargs, pl.defaults.meanplot_1d)  # @UndefinedVariable
            return dict(gpmean=[pl.plot(canvas, Xgrid[:, free_dims], mu, **kwargs)])
        else:
            update_not_existing_kwargs(kwargs, pl.defaults.meanplot_2d)  # @UndefinedVariable
            return dict(gpmean=[pl.contour(canvas, x, y, 
                                           mu.reshape(resolution, resolution), 
                                           levels=levels, **kwargs)])
    elif len(free_dims)==0:
        pass # Nothing to plot!
    else:
        raise RuntimeError('Cannot plot mean in more then 2 input dimensions')

def plot_confidence(self, lower=2.5, upper=97.5, plot_limits=None, fixed_inputs=None,
              resolution=None, plot_raw=False,
              apply_link=False, visible_dims=None,
              which_data_ycols='all',
              predict_kw=None, 
              **kwargs):
    """
    Plot the confidence interval between the percentiles lower and upper.
    E.g. the 95% confidence interval is $2.5, 97.5$.
    Note: Only implemented for one dimension!

    Give the Y_metadata in the predict_kw if you need it.
   
    :param float lower: the lower percentile to plot
    :param float upper: the upper percentile to plot
    :param plot_limits: The limits of the plot. If 1D [xmin,xmax], if 2D [[xmin,ymin],[xmax,ymax]]. Defaluts to data limits
    :type plot_limits: np.array
    :param fixed_inputs: a list of tuple [(i,v), (i,v)...], specifying that input dimension i should be set to value v.
    :type fixed_inputs: a list of tuples
    :param int resolution: The resolution of the prediction [default:200]
    :param bool plot_raw: plot the latent function (usually denoted f) only?
    :param bool apply_link: whether to apply the link function of the GP to the raw prediction.
    :param array-like visible_dims: which columns of the input X (!) to plot (array-like or list of ints)
    :param array-like which_data_ycols: which columns of the output y (!) to plot (array-like or list of ints)
    :param dict predict_kw: the keyword arguments for the prediction. If you want to plot a specific kernel give dict(kern=<specific kernel>) in here
    """
    canvas, kwargs = pl.get_new_canvas(kwargs)
    plots = _plot_confidence(self, canvas, lower, upper, plot_limits, 
                             fixed_inputs, resolution, plot_raw, 
                             apply_link, visible_dims, which_data_ycols, 
                             predict_kw, **kwargs)
    return pl.show_canvas(canvas, plots)

def _plot_confidence(self, canvas, lower, upper, plot_limits=None, fixed_inputs=None,
              resolution=None, plot_raw=False,
              apply_link=False, visible_dims=None,
              which_data_ycols=None, 
              predict_kw=None, 
              **kwargs):
    _, _, _, _, free_dims, Xgrid, _, _, _, _, _ = helper_for_plot_data(self, plot_limits, visible_dims, fixed_inputs, resolution)

    ycols = get_which_data_ycols(self, which_data_ycols)
    
    update_not_existing_kwargs(kwargs, pl.defaults.confidence_interval)  # @UndefinedVariable
    
    if len(free_dims)<=1:
        if len(free_dims)==1:
            _, percs, _ = helper_predict_with_model(self, Xgrid, plot_raw, apply_link, 
                                                 (lower, upper), 
                                                 ycols, predict_kw)
    
            fills = []
            for d in ycols:
                fills.append(pl.fill_between(canvas, Xgrid[:,free_dims[0]], percs[0][:,d], percs[1][:,d], **kwargs))
            return dict(gpconfidence=fills)
        else:
            pass #Nothing to plot!
    else:
        raise RuntimeError('Can only plot confidence interval in one input dimension')


def plot_samples(self, plot_limits=None, fixed_inputs=None,
              resolution=None, plot_raw=True,
              apply_link=False, visible_dims=None,
              which_data_ycols='all',
              samples=3, predict_kw=None,
              **kwargs):
    """
    Plot the mean of the GP.

    Give the Y_metadata in the predict_kw if you need it.
   
    
    :param plot_limits: The limits of the plot. If 1D [xmin,xmax], if 2D [[xmin,ymin],[xmax,ymax]]. Defaluts to data limits
    :type plot_limits: np.array
    :param fixed_inputs: a list of tuple [(i,v), (i,v)...], specifying that input dimension i should be set to value v.
    :type fixed_inputs: a list of tuples
    :param int resolution: The resolution of the prediction [defaults are 1D:200, 2D:50]
    :param bool plot_raw: plot the latent function (usually denoted f) only? This is usually what you want!
    :param bool apply_link: whether to apply the link function of the GP to the raw prediction.
    :param array-like visible_dims: which columns of the input X (!) to plot (array-like or list of ints)
    :param array-like which_data_ycols: which columns of y to plot (array-like or list of ints)
    :param dict predict_kw: the keyword arguments for the prediction. If you want to plot a specific kernel give dict(kern=<specific kernel>) in here
    :param int levels: for 2D plotting, the number of contour levels to use is 
    """
    canvas, kwargs = pl.get_new_canvas(kwargs)
    plots = _plot_samples(self, canvas, plot_limits, fixed_inputs, 
                       resolution, plot_raw, 
                       apply_link, visible_dims, which_data_ycols, samples, 
                       predict_kw, **kwargs)
    return pl.show_canvas(canvas, plots)

def _plot_samples(self, canvas, plot_limits=None, fixed_inputs=None,
              resolution=None, plot_raw=False,
              apply_link=False, visible_dims=None,
              which_data_ycols=None,
              samples=3, 
              predict_kw=None, **kwargs):
    _, _, _, _, free_dims, Xgrid, _, _, _, _, resolution = helper_for_plot_data(self, plot_limits, visible_dims, fixed_inputs, resolution)

    if len(free_dims)<2:
        
        if len(free_dims)==1:
            # 1D plotting:
            _, _, samples = helper_predict_with_model(self, Xgrid, plot_raw, apply_link, 
                                     None, get_which_data_ycols(self, which_data_ycols), predict_kw, samples)
            update_not_existing_kwargs(kwargs, pl.defaults.samples_1d)  # @UndefinedVariable
            return dict(gpmean=[pl.plot(canvas, Xgrid[:, free_dims], samples, **kwargs)])
        else:
            pass # Nothing to plot!
    else:
        raise RuntimeError('Cannot plot mean in more then 1 input dimensions')


def plot_density(self, plot_limits=None, fixed_inputs=None,
              resolution=None, plot_raw=False,
              apply_link=False, visible_dims=None, 
              which_data_ycols='all',
              levels=35,
              predict_kw=None, 
              **kwargs):
    """
    Plot the confidence interval between the percentiles lower and upper.
    E.g. the 95% confidence interval is $2.5, 97.5$.
    Note: Only implemented for one dimension!

    Give the Y_metadata in the predict_kw if you need it.
   
    :param plot_limits: The limits of the plot. If 1D [xmin,xmax], if 2D [[xmin,ymin],[xmax,ymax]]. Defaluts to data limits
    :type plot_limits: np.array
    :param fixed_inputs: a list of tuple [(i,v), (i,v)...], specifying that input dimension i should be set to value v.
    :type fixed_inputs: a list of tuples
    :param int resolution: The resolution of the prediction [default:200]
    :param bool plot_raw: plot the latent function (usually denoted f) only?
    :param bool apply_link: whether to apply the link function of the GP to the raw prediction.
    :param array-like visible_dims: which columns of the input X (!) to plot (array-like or list of ints)
    :param array-like which_data_ycols: which columns of y to plot (array-like or list of ints)
    :param int levels: the number of levels in the density (number bigger then 1, where 35 is smooth and 1 is the same as plot_confidence). You can go higher then 50 if the result is not smooth enough for you. 
    :param dict predict_kw: the keyword arguments for the prediction. If you want to plot a specific kernel give dict(kern=<specific kernel>) in here
    """
    canvas, kwargs = pl.get_new_canvas(kwargs)
    plots = _plot_density(self, canvas, plot_limits, 
                             fixed_inputs, resolution, plot_raw,  
                             apply_link, visible_dims, which_data_ycols, 
                             levels,
                             predict_kw, **kwargs)
    return pl.show_canvas(canvas, plots)

def _plot_density(self, canvas, plot_limits=None, fixed_inputs=None,
              resolution=None, plot_raw=False,
              apply_link=False, visible_dims=None,
              which_data_ycols=None,
              levels=35, 
              predict_kw=None, **kwargs):
    _, _, _, _, free_dims, Xgrid, x, y, _, _, resolution = helper_for_plot_data(self, plot_limits, visible_dims, fixed_inputs, resolution)

    ycols = get_which_data_ycols(self, which_data_ycols)

    update_not_existing_kwargs(kwargs, pl.defaults.density)  # @UndefinedVariable

    if len(free_dims)<=1:
        if len(free_dims)==1:
            _, percs, _ = helper_predict_with_model(self, Xgrid, plot_raw, 
                                          apply_link, np.linspace(2.5, 97.5, levels*2), 
                                          get_which_data_ycols(self, which_data_ycols), 
                                          predict_kw)
            # 1D plotting:
            fills = []
            for d in ycols:
                fills.append(pl.fill_gradient(canvas, Xgrid[:, free_dims[0]], [p[:,d] for p in percs], **kwargs))
            return dict(gpdensity=fills)
        else:
            pass # Nothing to plot!
    else:
        raise RuntimeError('Can only plot density in one input dimension')

def plot(self, plot_limits=None, fixed_inputs=None,
              resolution=None, 
              plot_raw=False, apply_link=False, 
              which_data_ycols='all', which_data_rows='all',
              visible_dims=None, 
              levels=20, samples=0, samples_likelihood=0, lower=2.5, upper=97.5, 
              plot_data=True, plot_inducing=True, plot_density=False,
              predict_kw=None, error_kwargs=None,
              **kwargs):  
    """
    Convinience function for plotting the fit of a GP.
    
    Give the Y_metadata in the predict_kw if you need it.

    :param plot_limits: The limits of the plot. If 1D [xmin,xmax], if 2D [[xmin,ymin],[xmax,ymax]]. Defaluts to data limits
    :type plot_limits: np.array
    :param fixed_inputs: a list of tuple [(i,v), (i,v)...], specifying that input dimension i should be set to value v.
    :type fixed_inputs: a list of tuples
    :param int resolution: The resolution of the prediction [default:200]
    :param bool plot_raw: plot the latent function (usually denoted f) only?
    :param bool apply_link: whether to apply the link function of the GP to the raw prediction.
    :param which_data_ycols: when the data has several columns (independant outputs), only plot these
    :type which_data_ycols: 'all' or a list of integers
    :param which_data_rows: which of the training data to plot (default all)
    :type which_data_rows: 'all' or a slice object to slice self.X, self.Y
    :param array-like visible_dims: which columns of the input X (!) to plot (array-like or list of ints)
    :param int levels: the number of levels in the density (number bigger then 1, where 35 is smooth and 1 is the same as plot_confidence). You can go higher then 50 if the result is not smooth enough for you. 
    :param int samples: the number of samples to draw from the GP and plot into the plot. This will allways be samples from the latent function.
    :param int samples_likelihood: the number of samples to draw from the GP and apply the likelihood noise. This is usually not what you want!
    :param float lower: the lower percentile to plot
    :param float upper: the upper percentile to plot
    :param bool plot_data: plot the data into the plot?
    :param bool plot_inducing: plot inducing inputs?
    :param bool plot_density: plot density instead of the confidence interval?
    :param dict predict_kw: the keyword arguments for the prediction. If you want to plot a specific kernel give dict(kern=<specific kernel>) in here
    :param dict error_kwargs: kwargs for the error plot for the plotting library you are using
    :param kwargs plot_kwargs: kwargs for the data plot for the plotting library you are using
    """
    canvas, kwargs = pl.get_new_canvas(kwargs)
    plots = _plot(self, canvas, plot_limits, fixed_inputs, resolution, plot_raw, 
                  apply_link, which_data_ycols, which_data_rows, visible_dims, 
                  levels, samples, samples_likelihood, lower, upper, plot_data, 
                  plot_inducing, plot_density, predict_kw, error_kwargs)
    return pl.show_canvas(canvas, plots)


def plot_f(self, plot_limits=None, fixed_inputs=None,
              resolution=None, 
              apply_link=False, 
              which_data_ycols='all', which_data_rows='all',
              visible_dims=None, 
              levels=20, samples=0, lower=2.5, upper=97.5, 
              plot_density=False,
              plot_data=True, plot_inducing=True, 
              predict_kw=None, error_kwargs=None,
              **kwargs):  
    """
    Convinience function for plotting the fit of a GP.
    
    This is the same as plot, except it plots the latent function fit of the GP!
    
    Give the Y_metadata in the predict_kw if you need it.

    :param plot_limits: The limits of the plot. If 1D [xmin,xmax], if 2D [[xmin,ymin],[xmax,ymax]]. Defaluts to data limits
    :type plot_limits: np.array
    :param fixed_inputs: a list of tuple [(i,v), (i,v)...], specifying that input dimension i should be set to value v.
    :type fixed_inputs: a list of tuples
    :param int resolution: The resolution of the prediction [default:200]
    :param bool apply_link: whether to apply the link function of the GP to the raw prediction.
    :param which_data_ycols: when the data has several columns (independant outputs), only plot these
    :type which_data_ycols: 'all' or a list of integers
    :param which_data_rows: which of the training data to plot (default all)
    :type which_data_rows: 'all' or a slice object to slice self.X, self.Y
    :param array-like visible_dims: an array specifying the input dimensions to plot (maximum two)
    :param int levels: the number of levels in the density (number bigger then 1, where 35 is smooth and 1 is the same as plot_confidence). You can go higher then 50 if the result is not smooth enough for you. 
    :param int samples: the number of samples to draw from the GP and plot into the plot. This will allways be samples from the latent function.
    :param float lower: the lower percentile to plot
    :param float upper: the upper percentile to plot
    :param bool plot_data: plot the data into the plot?
    :param bool plot_inducing: plot inducing inputs?
    :param bool plot_density: plot density instead of the confidence interval?
    :param dict predict_kw: the keyword arguments for the prediction. If you want to plot a specific kernel give dict(kern=<specific kernel>) in here
    :param dict error_kwargs: kwargs for the error plot for the plotting library you are using
    :param kwargs plot_kwargs: kwargs for the data plot for the plotting library you are using
    """
    canvas, kwargs = pl.get_new_canvas(kwargs)
    plots = _plot(self, canvas, plot_limits, fixed_inputs, resolution, 
                  True, apply_link, which_data_ycols, which_data_rows, 
                  visible_dims, levels, samples, 0, lower, upper, 
                  plot_data, plot_inducing, plot_density, 
                  predict_kw, error_kwargs)
    return pl.show_canvas(canvas, plots)



def _plot(self, canvas, plot_limits=None, fixed_inputs=None,
              resolution=None, 
              plot_raw=False, apply_link=False, 
              which_data_ycols='all', which_data_rows='all',
              visible_dims=None, 
              levels=20, samples=0, samples_likelihood=0, lower=2.5, upper=97.5, 
              plot_data=True, plot_inducing=True, plot_density=False,
              predict_kw=None, error_kwargs=None,
              **kwargs):  

        plots = {}
        if plot_data:
            plots.update(_plot_data(self, canvas, which_data_rows, which_data_ycols, visible_dims, error_kwargs))

        plots.update(_plot_mean(self, canvas, plot_limits, fixed_inputs, resolution, plot_raw, apply_link, visible_dims, which_data_ycols, levels, predict_kw))
        if not plot_density:
            plots.update(_plot_confidence(self, canvas, lower, upper, plot_limits, fixed_inputs, resolution, plot_raw, apply_link, visible_dims, which_data_ycols, predict_kw))
        else:
            plots.update(_plot_density(self, canvas, plot_limits, fixed_inputs, resolution, plot_raw, apply_link, visible_dims, which_data_ycols, levels, predict_kw))
        
        if samples > 0:
            plots.update(_plot_samples(self, canvas, plot_limits, fixed_inputs, resolution, True, apply_link, visible_dims, which_data_ycols, samples, predict_kw))
        if samples_likelihood > 0:
            plots.update(_plot_samples(self, canvas, plot_limits, fixed_inputs, resolution, False, apply_link, visible_dims, which_data_ycols, samples, predict_kw))

        if hasattr(self, 'Z') and plot_inducing:
            plots.update(_plot_inducing(self, canvas, visible_dims))
        
        return plots