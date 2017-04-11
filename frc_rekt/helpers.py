#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Helper functions.

Use these so we don't write duplicate code.

"""
import datetime
import magic

import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt  # noqa pylint: disable=wrong-import-position


def get_file_encoding(file_path):
    """Return encoding for file path.

    :param file_path: Path to file
    :type file_path: str
    :returns: encoding
    :rtype: str

    """
    magic_instance = magic.Magic(mime_encoding=True)
    encoding = magic_instance.from_file(file_path)
    return encoding


def plot_func(dataframe, func, x_label=None, y_label=None,
              title=None):  # pragma: no cover
    """Plot best fit function.

    Generates points using the function, and plots those points
    against the original data.

    :param dataframe: the dataframe of original data
    :type dataframe: pandas.DataFrame
    :param func: the function to plot
    :type func: types.FunctionType
    :param x_label: the label of the x axis data in the dataframe
    :type x_label: str
    :param y_label: the label of the y axis data in the dataframe
    :type y_label: str

    """
    if not x_label:
        x_label = dataframe.columns[0]
    if not y_label:
        y_label = dataframe.columns[1]
    dataframe['fit'] = func(dataframe[x_label])
    plot_df = dataframe.loc[:, [x_label, y_label, 'fit']]
    plot_df.plot(x=x_label)
    if title:
        title = '{cls}_{x_label}_vs_{y_label}_fit'.format(
            cls=title, x_label=x_label, y_label=y_label)
    if not title:
        title = datetime.datetime.now().isoformat()
    plt.savefig('artifacts/{0}.png'.format(title))
