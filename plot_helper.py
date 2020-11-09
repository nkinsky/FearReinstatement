# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 10:53:29 2018

@author: William Mau
"""
import matplotlib.pyplot as plt
import numpy as np


def pretty_plot(ax, round_ylim=False):
    """Generic function to make plot pretty, bare bones for now, will need updating
    :param round_ylim set to True plots on ticks/labels at 0 and max, rounded to the nearest decimal. default = False
    """

    # TODO: move this into a plot_function helper module or something similar
    # set ylims to min/max, rounded to nearest 10
    if round_ylim == True:
        ylims_round = np.round(ax.get_ylim(), decimals=-1)
        ax.set_yticks(ylims_round)
        ax.set_yticklabels([f'{lim:g}' for lim in iter(ylims_round)])

    # turn off top and right axis lines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    return ax


class ScrollPlot:
    """
    Plot stuff then scroll through it! A bit hacked together as of 2/28/2020. Better would be to input a figure and axes
    along with the appropriate plotting functions?

    :param
        plot_func: tuple of plotting functions to plot into the appropriate axes
        x: X axis data.
        y: Y axis data.
        xlabel = 'x': X axis label.
        ylabel = 'y': Y axis label.
        combine_rows = list of subplots rows to combine into one subplot. Currently only supports doing all bottom
        rows which must match the functions specified in plot_func


    """

    # Initialize the class. Gather the data and labels.
    def __init__(self, plot_func, xlabel='', ylabel='',
                 titles=([' '] * 10000), n_rows=1,
                 n_cols=1, figsize=(8, 6), combine_rows = [], **kwargs):
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

        self.fig, self.ax, = plt.subplots(self.n_rows, self.n_cols,
                                           sharey=self.share_y,
                                           sharex=self.share_x,
                                           figsize=self.figsize)
        if n_cols == 1 and n_rows == 1:
            self.ax = (self.ax,)

        # Make rows into one subplot if specified
        if len(combine_rows) > 0:
            for row in combine_rows:
                plt.subplot2grid((self.n_rows, self.n_cols), (row, 0), colspan=self.n_cols, fig=self.fig)
            self.ax = self.fig.get_axes()

        # Flatten into 1d array if necessary and not done already via combining rows
        if n_cols > 1 and n_rows > 1 and hasattr(self.ax, 'flat'):
             self.ax = self.ax.flat

        # Necessary for scrolling.
        if not hasattr(self, 'current_position'):
            self.current_position = 0

        # Plot the first plot of each function and label
        for ax_ind, plot_f in enumerate(self.plot_func):
            plot_f(self, ax_ind)
            self.apply_labels()
            # print(str(ax_ind))




        # Connect the figure to keyboard arrow keys.
        self.fig.canvas.mpl_connect('key_press_event',
                                    lambda event: self.update_plots(event))

    # Go up or down the list. Left = down, right = up.
    def scroll(self, event):
        if event.key == 'right' and self.current_position <= self.last_position:
            if self.current_position <= self.last_position:
                if self.current_position == self.last_position:
                    self.current_position = 0
                else:
                    self.current_position += 1
        elif event.key == 'left' and self.current_position >= 0:
            if self.current_position == 0:
                self.current_position = self.last_position
            else:
                self.current_position -= 1
        elif event.key == '6':
            if (self.current_position + 15) < self.last_position:
                self.current_position += 15
            elif (self.current_position + 15) >= self.last_position:
                if self.current_position == self.last_position:
                    self.current_position = 0
                else:
                    self.current_position = self.last_position
        elif event.key == '4':
            print('current position before = ' + str(self.current_position))
            if self.current_position > 15:
                self.current_position -= 15
            elif self.current_position <= 15:
                if self.current_position == 0:
                    self.current_position = self.last_position
                else:
                    self.current_position = 0
            print('current position after = ' + str(self.current_position))
        elif event.key == '9' and (self.current_position + 100) < self.last_position:
            self.current_position += 100
        elif event.key == '7' and self.current_position > 100:
            self.current_position -= 100

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
            # self.apply_labels()

        # Draw.
        self.fig.canvas.draw()

        if event.key == 'escape':
            plt.close(self.fig)


def neuron_number_title(neurons):
    titles = ["Neuron: " + str(n) for n in neurons]

    return titles