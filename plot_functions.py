"""
List of plotting functions to pass through ScrollPlot
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def plot_traces(obj):
    """
    For plotting calcium traces.
    :param
        obj: ScrollPlot class object.
    """
    obj.ax.plot(obj.t, obj.traces[obj.current_position])
    obj.last_position = len(obj.traces) - 1


def plot_events(obj):
    """
    For plotting calcium events.
    :param
        obj: ScrollPlot class object.
    :return:
    """
    obj.ax.scatter(obj.event_times[obj.current_position], obj.event_values[obj.current_position],marker='.')
    obj.last_position = len(obj.event_values) - 1


def overlay_events(obj):
    """
    For plotting calcium events over traces.
    :param
        obj: ScrollPlot class object.
    :return:
    """
    plot_traces(obj)
    plt.hold(True)
    plot_events(obj)


def display_frame(obj, ida):
    """
    For plotting FreezeFrame video frames.
    :param obj:
    :return:
    """

    if obj.current_position == 0:
        obj.current_position = round(obj.n_frames / 2)

    obj.ax[ida].imshow(obj.movie[obj.current_position], cmap='gray')
    obj.last_position = obj.n_frames - 1


def display_frame_and_position(obj, ida):
    if obj.current_position == 0:
        obj.current_position = round(obj.n_frames / 2)

    obj.ax[ida].imshow(obj.movie[obj.current_position], cmap='gray')
    obj.ax[ida].plot(obj.position[obj.current_position, 0], obj.position[obj.current_position, 1], 'ro')
    obj.last_position = obj.n_frames - 1


def display_frame_and_freezing(obj, ida):
    if obj.current_position == 0:
        obj.current_position = round(obj.n_frames / 2)

    obj.ax[ida].imshow(obj.movie[obj.current_position], cmap='gray')
    if obj.freezing[obj.current_position]:
        obj.ax[ida].plot(obj.position[obj.current_position, 0], obj.position[obj.current_position, 1], 'bo')
    else:
        obj.ax[ida].plot(obj.position[obj.current_position, 0], obj.position[obj.current_position, 1], 'ro')
    obj.last_position = obj.n_frames - 1


def plot_freezing_traces(obj):  # NK ScrollPlot updates have likely broken this
    for i, this_epoch in enumerate(obj.epochs):
        obj.ax[i].plot(obj.t[this_epoch[0]:this_epoch[1]],
                       obj.traces[obj.current_position, this_epoch[0]:this_epoch[1]])

    obj.last_position = len(obj.traces) - 1


def plot_heatmap(obj, ida):
    obj.ax[ida].imshow(obj.heatmap[obj.current_position])
    plt.axis('tight')

    obj.last_position = len(obj.heatmap) - 1


def plot_multiple_traces(obj, ida):
    for i, trace in enumerate(obj.traces[obj.current_position]):
        c = cm.gray(i/len(obj.traces[obj.current_position]),1)
        obj.ax[ida].plot(obj.t, trace, color=c)

    obj.last_position = len(obj.traces) - 1


def plot_footprints_over_days(obj): # NK ScrollPlot updates have likely broken this
    for i,footprint in enumerate(obj.footprints[obj.current_position]):
        obj.ax[i].imshow(footprint, cmap='gray')
        obj.ax[i].axis('equal')
        obj.ax[i].axis('off')

    obj.last_position = len(obj.footprints) - 1


def plot_traces_over_days(obj): # NK ScrollPlot updates have likely broken this
    for i,trace in enumerate(obj.traces[obj.current_position]):
        obj.ax[i].plot(obj.t[i], trace)

    obj.last_position = len(obj.traces) - 1


def plot_raster(obj, ida):
    obj.ax[ida].eventplot(obj.events[obj.current_position])
    obj.ax[ida].set_xlim([-obj.window, 0])

    obj.last_position = len(obj.events) - 1


def scatter_box(data, ax=None, f=None, xlabels=None, ylabel=None,
                spread=0.04, alpha=0.1, box_color='k'):
    """
    Plots a scatter and box plot overlaid.
    Parameters
    ---
    data: list of arrays or lists, data to be plotted.
    ax: Axes object, to plot on. If none (default), makes a new figure.
    f: Figure object, see above.
    xlabels: list of x axis labels.
    ylabel: str, y axis label.
    spread: scalar, x spread of scatter plot points.
    alpha: scalar, transparency.
    box_color: RGB or color str, color of box.
    Returns
    ---
    f: Figure object.
    ax: Axes object.
    """
    if ax is None:
        f, ax = plt.subplots()

    # Box plot.
    ax.boxplot(data, whis=[5, 95], sym='',
               medianprops=dict(color=box_color))

    # For each element in the list, scatter.
    for i, group in enumerate(data):
        x = np.random.normal(i + 1, spread, size=len(group))
        ax.scatter(x, group, alpha=alpha, s=5, c='k')

    # Label axes.
    if xlabels is not None:
        ax.set_xticklabels(xlabels)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    return f, ax


def scatter_bar(data, ax=None, f=None, xlabels=None, ylabel=None,
                spread=0.04, alpha=0.1, color='b'):
    """
    Same as scatter_box (above) but only plots mean and in bar graph format.
    :param data:
    :param ax:
    :param f:
    :param xlabels:
    :param ylabel:
    :param spread:
    :param alpha:
    :param box_color:
    :return: f, ax
    """

    if ax is None:
        f, ax = plt.subplots()

    # Box plot.
    ax.bar(np.arange(0, len(data)), [np.nanmean(frz) for frz in data],
           color=color, edgecolor='k', width=0.6, alpha=0.5)

    # For each element in the list, scatter.
    for i, group in enumerate(data):
        x = np.random.normal(i, spread, size=len(group))
        ax.scatter(x, group, alpha=alpha, s=5, c='k')

    # Label axes.
    if xlabels is not None:
        ax.set_xticks(np.arange(0, len(data)))
        ax.set_xticklabels(xlabels)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    return f, ax
