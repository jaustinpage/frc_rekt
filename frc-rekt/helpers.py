#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

""" Helper functions 

Use these so we don't write duplicate code.

"""

import magic


def get_file_encoding(file_path):
    """returns encoding

    returns the encoding of the file path.

    :param file_path: Path to file
    :type file_path: str
    :returns: encoding
    :rtype: str

    """
    magic_instance = magic.Magic(mime_encoding=True)
    encoding = magic_instance.from_file(file_path)
    return encoding


def plot_func(dataframe, func, x_label, y_label):
    """plots best fit function

    generates points using the function, and plots those points
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
    dataframe['fit'] = func(dataframe[x_label])
    plot_df = dataframe.loc[:, [x_label, y_label, 'fit']]
    plot_df.plot(x=x_label)
