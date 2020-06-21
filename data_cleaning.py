#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 12:51:18 2020

@author: ismael
"""

import pandas as pd
import numpy as np
#make a dataframe
df = pd.read_csv('inmuebles24-distrito-federal-venta.csv')
#replace the NaN of rooms with the median of the rooms
medianr = df['rooms'].median()
df['rooms'].fillna(medianr, inplace=True)
#replace the NaN of bathrooms with the median of bathrooms
medianb = df['bathrooms'].median()
df['bathrooms'].fillna(medianb, inplace=True)
#remplace the NaN of terrain with the corresponding construction and viss
df['terrain (m2)'].fillna(df['construction (m2)'] , inplace=True)
df['construction (m2)'].fillna(df['terrain (m2)'] , inplace=True)
#delete the rows that have NaN in terrain or contruction (more important)
df = df.dropna()
B = df.isnull().sum()
print(B)
#add the divisa column
df['divisa'] = df['price'].apply(lambda x: x.split(' ')[0])
df['divisa'] = df['divisa'].apply(lambda x: 1 if 'MN' in x else 0)
#remove the , MN and USD from price
df['price'] = df['price'].apply(lambda x: x.split(' ')[1])
df['price'] = df['price'].apply(lambda x: x.replace(',',''))
#coverting price strings into float
df['price'] = pd.to_numeric(df['price'])
#converting USD to MN and then in Millons of Pesos
N = df['divisa'].isin([0,2])
df['price MP'] = np.where(N, df['price'].mul(22), df['price'])
df['price MP'] = df['price MP']/1000000
#add delegacion
df['Delegacion'] = df['location'].apply(lambda x: x.split(',')[-1])
#add colonia
df['colonia'] = df['location'].apply(lambda x: x.split(',')[-2])
df.Delegacion.value_counts()
#pasing of depto description (gimnasio,alberca,pet fiendly,etc)
#gym
df['gym'] = df['description'].apply(lambda x: 1 if 'gym' in x.lower() or 'gimnasio' in x.lower() else 0)
df.gym.value_counts()
#pool
df['pool'] = df['description'].apply(lambda x: 1 if 'pool' in x.lower() or 'alberca' in x.lower() else 0)
df.pool.value_counts()
#pet friendly
df['pet'] = df['description'].apply(lambda x: 1 if 'pet' in x.lower() or 'mascota' in x.lower() else 0)
df.pet.value_counts()
#garage
df['garage'] = df['description'].apply(lambda x: 1 if 'garage' in x.lower() or 'estacionamiento' in x.lower() else 0)
df.garage.value_counts()
#elevator
df['elevador'] = df['description'].apply(lambda x: 1 if 'elevador' in x.lower() or 'elevator' in x.lower() else 0)
df.elevador.value_counts()
#terraza
df['terrace'] = df['description'].apply(lambda x: 1 if 'terrace' in x.lower() or 'terraza' in x.lower() else 0)
df.terrace.value_counts()
#roof garden
df['garden'] = df['description'].apply(lambda x: 1 if 'garden' in x.lower() or 'verde' in x.lower() else 0)
df.garden.value_counts()
#droping the unusefull columns
df_clean = df.drop(['description'], axis=1)
df_clean = df_clean.drop(['price'], axis=1)
df_clean = df_clean.drop(['operation'], axis=1)
#saving in a csv
df_clean.to_csv('inmuebles24-data-cleaned.csv',index = False)