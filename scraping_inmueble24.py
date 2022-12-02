#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 10:43:37 2020

@author: ismael
"""


"""
Module to scrape Inmuebles 24
and stores data in local storage as CSV.
Fetched Fields:
name, description, location, link, price, operation, rooms, bathrooms, construction (m2), terrain (m2)
"""
import requests
import statistics
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
import os
import re

from urllib.request import Request, urlopen

import warnings
warnings.filterwarnings('ignore')

# Vars
query_date = date.today().strftime("%Y-%m-%d")
_root = 'https://www.inmuebles24.com/'
_state = 'ciudad-de-mexico'
_operation = 'venta'
_base_url = _root + "departamentos-en-" + _operation + "-en-" + _state + "-pagina-{}.html"
#user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"
user_agent = "Mozilla/5.0"
ddir = 'ds_realestate_proj/data/'


def save(depts):
    """ Append page data
        Params:
        -----
        depts : pd.Dataframe()
            Dataframe of Departments
    """
    # Read Existant file to append
    _fname = ddir + "/inmuebles24" + "-" + _state + "-" + _operation + "-" + query_date + ".csv"
    try:
        df = pd.read_csv(_fname, delimiter=',')
    except:
        print('New file, creating folder..')
        try:
            os.mkdir(ddir)
            print('Created folder!')
        except:
            print('Folder exists already!')
        df = pd.DataFrame()
    # Append data
    # print(depts.head(1).to_dict())
    try:
        if df.empty:
            depts.set_index(['name', 'location']).to_csv(_fname, sep=',')
            print('Correctly saved file: {}'.format(_fname))
        else:
            df = pd.concat([df, depts])
            df.set_index(['name', 'location']).to_csv(_fname, sep=',')
            print('Correctly saved file: {}'.format(_fname))
    except Exception as e:
        print(e)
        print('Could not save file: {}'.format(_fname))

def scrape_individual(appartment_content):
    """ Scrape individual page of each apartment """
    temp_dict = {}
    
    soup = BeautifulSoup(appartment_content, 'html.parser')
    feats = soup.find_all(class_="icon-feature")
    #print(feats)
    for li in feats:
        li = li.text.strip().lower()
        if 'rec' in li:
            temp_dict['rooms'] = statistics.mean([int(s) for s in li.split() if s.isdigit()])
        elif 'baños' in li:
            temp_dict['bathrooms'] = statistics.mean([int(s) for s in li.split() if s.isdigit()])
        elif 'cons' in li:
            temp_dict['construction (m2)'] = statistics.mean([int(s) for s in li.split() if s.isdigit()])
        elif 'total' in li:
            temp_dict['terrain (m2)'] = statistics.mean([int(s) for s in li.split() if s.isdigit()])
        elif 'estac' in li:
            temp_dict['estacionamientos'] = statistics.mean([int(s) for s in li.split() if s.isdigit()])
        elif 'medio' in li:
            temp_dict['toilets'] = statistics.mean([int(s) for s in li.split() if s.isdigit()])
        elif 'estrenar' in li:
            temp_dict['age'] = 0
        elif 'años' in li:
            temp_dict['age'] = statistics.mean([int(s) for s in li.split() if s.isdigit()])

    # SE INTENTARON EXTRAER LOS MAIN FEATURES PERO SE REQUIERE UN API PARA ACCEDER A LOS DATOS CON $=0
    wanted_string= "const POSTING"#["Características generales", "Servicios", "Amenidades"]
    wanted=None
    scripts = soup.findAll('script')
    for script in scripts:
        if wanted_string in script.text:
            wanted = script.text
        else:
            continue
    #print(wanted)

    wanted_strings = ["Características generales", "Servicios", "Amenidades", "Exteriores", "developmentFeatures"]
    for i in range(len(wanted_strings)-1):
        #print(i)
        try:
            result = re.search('{0}(.*){1}'.format(wanted_strings[i], wanted_strings[i+1]), wanted)
            if result:
                temp_dict[wanted_strings[i]] = result.group(1)[2:-1]
            else:
                result = re.search('{0}(.*){1}'.format(wanted_strings[i], wanted_strings[i+2]), wanted)
                temp_dict[wanted_strings[i]] = result.group(1)[2:-1] if result else None
            #print(temp_dict[wanted_strings[i]])
        except Exception:
            continue

    location = "postingGeolocation"
    end_loc = "urlStaticMap"
    result = re.search('{0}(.*){1}'.format(location, end_loc), wanted)
    if result:
        temp_dict['geolocation'] = result.group(1)[2:-2] + '}'
    else:
        temp_dict["geolocation"] = None

    #print(temp_dict)
    return temp_dict

def scrape(content):
    """ Scrape all listings per page """
    columns = ['name',
               'description',
               'location',
               'link',
               'price',
               'operation',
               'rooms',
               'bathrooms',
               'construction (m2)',
               'terrain (m2)',
               'estacionamientos',
               'toilets',
               'age',
               'Características generales',
               'Servicios',
               'Amenidades', 
               'Exteriores',
               'geolocation']

    data = pd.DataFrame(columns=columns)
    # Generate soup
    soup = BeautifulSoup(content, 'html.parser')
    # print(soup.prettify())
    # Get Characteristics
    apps = soup.find_all("div", {"class":"components__CardContainer-sc-1tt2vbg-3 dxVYDq"})
    # print(len(apps))
    for d in apps:#soup.find_all(class_="posting-card"): 
        #postingCardstyles_PostingCardContainer-ilodl-1 ZcXGN'
        temp_dict = {}
        try:
            temp_dict['name'] = d.find(class_="postingCardstyles__PostingTitleLink-i1odl-11 UQSQc").text.strip()
            temp_dict['description'] = d.find(class_="postingCardstyles__PostingDescription-i1odl-12 hXoNF").text.strip()
            temp_dict['location'] = ' '.join([j.strip() for j in d.find(class_="components__LocationLocation-ge2uzh-2 cGROxm").text.strip().split('\n')])
            temp_dict['link'] = d.find(class_="postingCardstyles__PostingTitle-i1odl-10 bEIaee").find('a').get('href')
            temp_dict['price'] = d.find(class_="components__Price-sc-12dh9kl-4 inzZeR").text.strip()
            temp_dict['operation'] = _operation
            #print(temp_dict['link'])
            try:
                appartment_url = _root + temp_dict['link'][1:]
                r = requests.get(appartment_url,
                                headers={'user-agent': user_agent})
                if r.status_code != 200:
                    raise Exception("Wrong Response")
                #print('Scraping individual page')
                #print(appartment_url)
                extra_features = scrape_individual(r.content)
                temp_dict.update(extra_features)
                #print(temp_dict)
                #break
            except Exception as e:
                print('ocurrio una expecion:', e)
                continue
                #print('Finishing to retrieve info.')
                #break

        except Exception as e:
            print(e)
            continue

        data = data.append(temp_dict, ignore_index=True)
    
    print('Found {} depts'.format(len(data['name'])))
    return data


def paginate():
    """ Loop over pages to retrieve all info available
        Returns:
        -----
        pg_nums : int
            Number of pages scraped
    """
    pg_nums = 796
    while True:
        try:
            print(_base_url.format(pg_nums))
            r = requests.get(_base_url.format(pg_nums),
                             headers={'user-agent': user_agent})
            if r.status_code != 200:
                raise Exception("Wrong Response")
            depts = scrape(r.content)
            if depts.empty:
                raise Exception("No more departments")
        except Exception as e:
            print(e)
            print('Finishing to retrieve info.')
            break
        # Store values
        save(depts)
        # break
        pg_nums += 1
    return pg_nums


def main():
    """ Main method """
    print('Starting to scrape Inmuebles24')
    paginate()
    return "Done"


if __name__ == '__main__':
    main()
