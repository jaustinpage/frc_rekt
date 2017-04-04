#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import magic


def get_file_encoding(file_path):
    m = magic.Magic(mime_encoding=True)
    encoding = m.from_file(file_path)
    return encoding


def plot_fit(dataframe, fit_func, x_label, y_label):
    dataframe['fit'] = fit_func(dataframe[x_label])
    plot_df = dataframe.loc[:, [x_label, y_label, 'fit']]
    plot_df.plot(x=x_label)
