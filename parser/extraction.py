#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Alexey Koshevoy

import pandas as pd
import numpy as np
import json
import collections


data = pd.read_csv('informants.csv')

data = data[np.isfinite(data['year of birth'])]

data = data.dropna(subset=['languages'])

# data = data[data['7'].str.contains('неизвестно') == False]


def add_languages(df):
    """
    Extract languages data from pandas dataframe and return complete dataframe
    with language columns added
    :param df: pandas dataframe
    :return: pandas dataframe
    """

    df = df.reset_index()

    languages = df['languages']

    languages_d = []

    for element in languages:
        json_acceptable_string = element.replace("'", "\"")
        d = json.loads(json_acceptable_string)
        languages_d.append(d)

    element_dict = list(languages_d[1].keys())

    # df = df.drop(['index', 'Unnamed: 0'], axis=1)
    df = df.drop(['languages', 'index', 'Unnamed: 0'], axis=1)

    df = df.join(pd.DataFrame(languages_d))

    for element in element_dict:
        lang = element

        df[lang] = df[lang].replace([-1, 0, 1], 0)
        df[lang] = df[lang].replace(2, 1)

    return df

dfs = []

for element in collections.Counter(data['expedition']):
    print(element)
    dfs.append(add_languages(data[data['expedition'] == element]))

finall = pd.concat(dfs, ignore_index=True)

print(finall.shape)

finall = finall.fillna(0)

finall = finall.reset_index()

finall.to_csv('data_250518.csv')
