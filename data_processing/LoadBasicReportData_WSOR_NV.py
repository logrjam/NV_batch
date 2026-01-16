# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 13:00:36 2025

@author: Logan.Jamison
"""
# load report data using the API

def LoadBasicReportData_WSOR_NV(ReportMonth,ReportYear):
    import requests
    import pandas as pd
    
    #########################
    # ReportMonth = 8
    # ReportYear = 2024 #If running on Oct 1, leave as previous WY
    #########################
    
    
    watershedlist = [  
                        'state of nevada and eastern sierra',
                        'lake tahoe',
                        'truckee',
                        'carson',
                        'walker',
                        'northern great basin',
                        'upper humboldt',
                        'lower humboldt',
                        'clover valley and franklin',
                        'snake',
                        'owyhee',
                        'eastern nevada',
                        'spring mountains',
                        'surprise valley-warner mtns'
                  ]

    
    
     
    
    
    #download data from API for each basin type
    
    #precip
    prec_url = f'https://nwcc-apps.sc.egov.usda.gov/aws-api/wsor/getPrecData?basinType=nv&pubMonth={ReportMonth}&pubYear={ReportYear}&format=json'
    prec_api = requests.get(prec_url)
    prec_json = prec_api.json()
    #reservoirs
    res_url = f'https://nwcc-apps.sc.egov.usda.gov/aws-api/wsor/getResData?basinType=nv&pubMonth={ReportMonth}&pubYear={ReportYear}&format=json'
    res_api = requests.get(res_url)
    res_json = res_api.json()
    
    # build lists for basin-wide precip, basin-wide res, and a dictionary for individual res values
    # the individual reservoir data is nice to have in nested format, so we don't want it in a dataframe yet
    prec_d = [] 
    basin_res_d = []
    res_d = {} # dictionary so we can use the keys later
    for watershed in watershedlist:
        
    
        #precipitation     
        prec_d.append(
                {
                    'prec_mnth_ly_per_med': prec_json[watershed][0]['basin_index']['prec_mnth_ly_per_med'],
                    'prec_ytd_curr_per_med': prec_json[watershed][0]['basin_index']['prec_ytd_curr_per_med'],
                    'prec_mnth_curr_per_med': prec_json[watershed][0]['basin_index']['prec_mnth_curr_per_med'],
                    'prec_ytd_ly_per_med': prec_json[watershed][0]['basin_index']['prec_ytd_ly_per_med']
                })
        #basin-wide reservoir 
        basin_res_d.append(
                {
                    'res_curr_per_cap': res_json[watershed][0]['basin_index']['res_curr_per_cap'],
                    'res_ly_per_cap': res_json[watershed][0]['basin_index']['res_ly_per_cap'],
                    'res_med_per_cap': res_json[watershed][0]['basin_index']['res_med_per_cap'],
                    'res_curr_per_med': res_json[watershed][0]['basin_index']['res_curr_per_med'],
                    'res_ly_per_med': res_json[watershed][0]['basin_index']['res_ly_per_med']
                })
        #individual reservoir stats
        res_d[watershed] = {
                'res_cap': res_json[watershed][0]['res_cap'],
                'res_curr': res_json[watershed][0]['res_curr'],
                'res_ly': res_json[watershed][0]['res_ly'],
                'site_meta': res_json[watershed][0]['site_meta']
            }
        
                
    # convert lists to dataframes. individual reservoirs stay in dictionary
    prec_df_api = pd.DataFrame(prec_d,index =[watershedlist])
    basin_res_df_api = pd.DataFrame(basin_res_d,index =[watershedlist])

    return(prec_df_api,basin_res_df_api,res_d)
   