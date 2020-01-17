# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 11:38:04 2019

@author: susanr
"""
import os
import pandas as pd
import csv
import numpy as np

def needs_human(log):
    if log not in human_logs:
        human_logs.append(log)

os.chdir(r'D:/Dropbox/Pahrump Maki/WellLogData')

# read in lithology binary classification dictionary
with open('lith_dict.csv', mode='r') as infile:
    reader = csv.reader(infile)
    lith_dict = {rows[0]:rows[1] for rows in reader}
        
os.chdir(r'D:/Dropbox/Pahrump Maki/WellLogData/WellLogData')
        
# get a list of all the logs to analyze
logs = os.listdir()
logs = [x for x in logs if '.csv' in x]

human_logs = []
sand_mod_list = ['sandy','silty','gravelly']
clay_mod_list = ['clayey']
cal_mod_list = ['soft','loose','water']
clay = '0'
sand = '1'
   
#log_mats = pd.DataFrame()

# read in each log, shift to lowercase, correct common weird punctuation
for log in logs:
    text = pd.read_csv(log, encoding='utf-8')
    #text = text[['material']]
    #log_mats= log_mats.append(text)  

    #log_mats = log_mats.reset_index()
    try:
        text['new_material'] = text['material'].str.lower()
    except:
        # add code to flag log for human review
        needs_human(log)
        continue
    text['new_material'] = text['new_material'].str.replace('& ','and ')
    text['new_material'] = text['new_material'].str.replace('w/ ','with ')
    text['new_material'] = text['new_material'].str.replace('w/','with ')
    text['new_material'] = text['new_material'].str.replace('(','')
    text['new_material'] = text['new_material'].str.replace(')','')
    text['new_material'] = text['new_material'].str.replace(',','')
    text['new_material'] = text['new_material'].str.replace('top soil','topsoil')
    
    text['final_material'] = ""
    text['binary'] = np.nan
    
    for i in range(0,len(text)):
        lith_match = []
        sand_mod = False
        clay_mod = False
        cal_mod = False
        material = text['new_material'][i]
        water = text['water_strata'][i]
        
        try:
            for w in material.split(" "):
                if w in lith_dict.keys():
                    lith_match.append(lith_dict[w])
                elif w in sand_mod_list:
                    sand_mod = True
                elif w in clay_mod_list:
                    clay_mod = True
                elif w in cal_mod_list:
                    cal_mod = True
            try:
                if lith_match[0] == '2' and cal_mod == False and water != 1.0:
                    text['final_material'][i] = 'Sand'
                    text['binary'][i] = 1
                elif lith_match[0] == '2' and (cal_mod == True or water == 1.0):
                    text['final_material'][i] = 'Sand-Clay'
                    text['binary'][i] = 0
                elif lith_match[0] == '0':
                    if sand in lith_match or sand_mod == True:
                        text['final_material'][i] = 'Sand-Clay'
                    else: 
                        text['final_material'][i] = 'Clay'
                    text['binary'][i] = 0
                elif lith_match[0] == '1':
                    if clay in lith_match or clay_mod == True:
                        text['final_material'][i] = 'Sand-Clay'
                    else:
                        text['final_material'][i] = 'Sand'
                    text['binary'][i] = 1
            except:
                # add code to flag for human review
                needs_human(log)
                continue

        except:
            # add code to flag for human review
            needs_human(log)
            continue
    
    text = text.drop(['new_material'], axis=1)
    text.to_csv(r'D:/Dropbox/Pahrump Maki/WellLogData/Interpretations/' + log)

                
        

#remove_words = ['grey ','green ','brown ','white ','black ','yellow ','red ','blue ','gray ','tan ','sticky ', 'soft ', 'hard ', 'light ']
#pat = r'\b(?:{})\b'.format('|'.join(remove_words))
#log_mats['new'] = log_mats['new'].str.replace(pat, '')

#key_words = ['sand','clay','gravel','rock','loam','caliche','granite','boulders','conglomerate','limestone','sandstone','shale','rocks',
#             'granite','quartz','cobbles','cobblestone','lime','tuff','siltstone','surface','topsoil']


#unique_lith = pd.DataFrame(log_mats['new'].unique())
