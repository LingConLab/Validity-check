#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Alexey Koshevoy

import pandas as pd
import numpy as np
import json


data = pd.read_csv('informants.csv')

data = data[np.isfinite(data['1'])]

data = data.dropna(subset=['4'])

# data = data[data['7'].str.contains('неизвестно') == False]


def add_languages(df):
    """
    Extract languages data from pandas dataframe and return complete dataframe
    with language columns added
    :param df: pandas dataframe
    :return: pandas dataframe
    """
    df = df.reset_index()

    languages = df['4']

    languages_d = []

    for element in languages:
        json_acceptable_string = element.replace("'", "\"")
        d = json.loads(json_acceptable_string)
        languages_d.append(d)

    element_dict = list(languages_d[1].keys())

    df = df.drop(['4', 'index', 'Unnamed: 0'], axis=1)

    df = df.join(pd.DataFrame(languages_d))

    for element in element_dict:
        lang = element

        df[lang] = df[lang].replace([-1, 0, 1], 0)
        df[lang] = df[lang].replace(2, 1)

    return df

ACS = data[data['5'] == 'Archib, Chitab, Shalib']
ACS = add_languages(ACS)

AKLK = data[data['5'] == 'Arkhit, Kug, Laka, Khiv']
AKLK = add_languages(AKLK)

BTSK = data[data['5'] == 'Balkhar, Tsulikana, Shukty, Kuli']
BTSK = add_languages(BTSK)

CDDC = data[data['5'] == 'Chankurbe, Durgeli, Durangi, Chabanmakhi']
CDDC = add_languages(CDDC)

CTU = data[data['5'] == 'Chuni, Tsukhta, Ubekimakhi']
CTU = add_languages(CTU)

DEDD = data[data['5'] == 'Darvag, Ersi, Dyubek, Dzhavgat']
DEDD = add_languages(DEDD)

KG = data[data['5'] == "Kina, Gel'mets"]
KG = add_languages(KG)

MUS = data[data['5'] == 'Mukar, Uri, Shangoda']
MUS = add_languages(MUS)

RC = data[data['5'] == 'Richa, Chirag']
RC = add_languages(RC)

RKZ = data[data['5'] =='Rikvani, Kizhani, Zilo']
RKZ = add_languages(RKZ)

SOM = data[data['5'] =='Shangoda, Obokh, Megeb']
SOM = add_languages(SOM)

YMCT = data[data['5'] =='Yangikent, Mallakent, Chumli, Tumenler']
YMCT = add_languages(YMCT)

finall = BTSK.append([CDDC, CTU, DEDD, KG, MUS, RC, RKZ, SOM, YMCT])

finall = finall.fillna(0)

finall.to_csv('finall.csv')
