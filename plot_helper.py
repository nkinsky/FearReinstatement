# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 10:53:29 2018

@author: William Mau
"""
import matplotlib.pyplot as plt


class ScrollPlot:
    """ 
    Plot stuff then scroll through it!

    :param
        x: X axis data.
        y: Y axis data.
        xlabel = 'x': X axis label.
        ylabel = 'y': Y axis label.


    """

    # Initialize the class. Gather the data and labels.
    def __init__(self, plot_func, xlabel='', ylabel='',
                 titles=([' '] * 10000), n_rows=1,
                 n_cols=1, figsize=(8, 6), **kwargs):
        self.plot_func = plot_func
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.titles = titles
        self.n_rows = n_rows  # NK can make default = len(plot_func)
        self.n_cols = n_cols
        self.share_y = False
        self.share_x = False
        self.figsize = figsize

        # Dump all arguments into ScrollPlot.
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.fig, self.ax = plt.subplots(self.n_rows, self.n_cols,
                                           sharey=self.share_y,
                                           sharex=self.share_x,
                                           figsize=self.figsize)
        if n_cols == 1 and n_rows == 1:
            self.ax = (self.ax,)

        # Necessary for scrolling.
        if not hasattr(self, 'current_position'):
            self.current_position = 0

        # Plot the first plot of each function and label
        for ax_ind, plot_f in enumerate(self.plot_func):
            plot_f(self, ax_ind)
            self.apply_labels()

        # Connect the figure to keyboard arrow keys.
        self.fig.canvas.mpl_connect('key_press_event',
                                    lambda event: self.update_plots(event))

    # Go up or down the list. Left = down, right = up.
    def scroll(self, event):
        if event.key == 'right' and self.current_position < self.last_position:
            self.current_position += 1
        elif event.key == 'left' and self.current_position > 0:
            self.current_position -= 1
        elif event.key == '6' and (self.current_position + 15) < self.last_position:
            self.current_position += 15
        elif event.key == '4' and self.current_position > 15:
            self.current_position -= 15

    # Apply axis labels.
    def apply_labels(self):
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.title(self.titles[self.current_position])

    # Update the plot based on keyboard inputs.
    def update_plots(self, event):
        # Clear axis.
        try:
            for ax in self.ax:
                ax.cla()
                # print('Cleared axes!')
        except:
            self.ax.cla()

        # Scroll then update plot.
        self.scroll(event)

        # Run the plotting function.
        for ax_ind, plot_f in enumerate(self.plot_func):
            plot_f(self, ax_ind)
            self.apply_labels()

        # Draw.
        self.fig.canvas.draw()

        if event.key == 'escape':
            plt.close(self.fig)


def neuron_number_title(neurons):
    titles = ["Neuron: " + str(n) for n in neurons]

    return titles