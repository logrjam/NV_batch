# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 15:52:15 2020

@author: David.Eiriksson
"""
#Download Precip, SWE, Soil Moisture, and Reservoir Data into dataframes.
#see "LoadReportData" fucntion for valid inputs.  

#Inputs: Watershed, Year of interest, Month of Interest
#Outputs: Precip, SWE, Soil Moisture, and Reservoir Data.  Output into pandas dataframes
    

#IMPORTANT: Reservoir data in AWDB is stored as end of month data.  This function
#is set up with a first of month reference, so, if you input
#2 (Feb) as the month of interest, you are actually grabbing end of month January reservoir
#data.  The resulting datagframe will show the date as it is stored in AWDB (2019-1-1), but the
#actual reservoir measurement will have been made right around Feb `.    


def LoadReportData_NV(watershed,ReportYear,ReportMonth,prec_df_api,basin_res_df_api,res_d):
    global allsites
    global txt1
    global txt2
    global txt3
    global txt4
        
    #from SNOW_data_class_8_4 import SnowData_retrieve
    import pandas as pd
    import datetime as dt
    #from MinMaxForecast import MinMaxForecast  
    #from CalculateSWSI_v2 import CalculateSWSI_v2
    import math
    #from GetPctMed_NV import GetPctMed_NV
    import requests
    

    # watershedlist = [  
    #                         'state_of_nevada_and_eastern_sierra',
    #                         'lake_tahoe',
    #                         'truckee',
    #                         'carson',
    #                         'walker',
    #                         'northern_great_basin',
    #                         'upper_humboldt',
    #                         'lower_humboldt',
    #                         'clover_valley_and_franklin',
    #                         'snake',
    #                         'owyhee',
    #                         'eastern_nevada',
    #                         'spring_mountains',
    #                         'surprise_valley-warner_mtns',
    #                         'Upper_Colorado_Region'
    #                   ]
    
    # watershed = 'Upper_Colorado_Region'
    # ReportMonth = 1
    # ReportYear=2025
    
    wshed_alt = watershed.replace("_", " ")
    
    if watershed == 'Upper_Colorado_Region':
        wshed_alt = 'upper colorado region'
        basintype = '2'
    else: 
        basintype = 'nv'
    
    
    if ReportMonth == 1:
        loadmonths = [11,12,1]
    elif ReportMonth == 2:
        loadmonths = [11,12,1,2]
    elif ReportMonth == 3:
        loadmonths = [11,12,1,2,3]    
    elif ReportMonth == 4:
        loadmonths = [11,12,1,2,3,4]
    elif ReportMonth == 5:
        loadmonths = [11,12,1,2,3,4,5]
    
    ReportYear_str = str(ReportYear)
    ReportMonth_str = str(ReportMonth)
    allpcpmonths = []
    MonthlyPctMed = []
    
    for i in range(len(loadmonths)):
        print(f'Loading {wshed_alt} monthly precip Stats From the NWCC Apps API: '+str(loadmonths[i]))
        monthstr = str(loadmonths[i])
        print(monthstr)
        
        if loadmonths[i]>=11:
            yearstr = str(ReportYear-1)
        else:
            yearstr = str(ReportYear)
        print(yearstr)
        r = requests.get(f'https://nwcc-apps.sc.egov.usda.gov/aws-api/wsor/getPrecData?state=CO&pubMonth={monthstr}&pubYear={yearstr}&basinType={basintype}&format=json')
        r.ok
        j = r.json()
        prec_mnth_curr_per_med = j[wshed_alt][0]['basin_index']['prec_mnth_curr_per_med']
        allpcpmonths.append(prec_mnth_curr_per_med)
        
    MonthlyPctMed = pd.DataFrame(allpcpmonths).T
    
    if ReportMonth == 1:
        MonthlyPctMed.columns = ['Oct_pcp','Nov_pcp','Dec_pcp']
    if ReportMonth == 2:
        MonthlyPctMed.columns = ['Oct_pcp','Nov_pcp','Dec_pcp','Jan_pcp']
    if ReportMonth == 3:
        MonthlyPctMed.columns = ['Oct_pcp','Nov_pcp','Dec_pcp','Jan_pcp','Feb_pcp']
    if ReportMonth == 4:
        MonthlyPctMed.columns = ['Oct_pcp','Nov_pcp','Dec_pcp','Jan_pcp','Feb_pcp','March_pcp']
    if ReportMonth == 5:
        MonthlyPctMed.columns = ['Oct_pcp','Nov_pcp','Dec_pcp','Jan_pcp','Feb_pcp','March_pcp','Apr_pcp']
        
      
    pcp_pct_cur = requests.get(f'https://nwcc-apps.sc.egov.usda.gov/aws-api/wsor/getPrecData?state=CO&pubMonth={ReportMonth_str}&pubYear={ReportYear_str}&basinType={basintype}&format=json').json()[wshed_alt][0]['basin_index']['prec_ytd_curr_per_med']
    pcp_pct_month = requests.get(f'https://nwcc-apps.sc.egov.usda.gov/aws-api/wsor/getPrecData?state=CO&pubMonth={ReportMonth_str}&pubYear={ReportYear_str}&basinType={basintype}&format=json').json()[wshed_alt][0]['basin_index']['prec_mnth_curr_per_med']
    snow = requests.get(f'https://nwcc-apps.sc.egov.usda.gov/aws-api/wsor/getSnowData?state=CO&pubMonth={ReportMonth_str}&pubYear={ReportYear_str}&basinType={basintype}&format=json')  
    
    swe_pct_cur = snow.json()[wshed_alt][0]['basin_index']['wteq_curr_per_med']    
    swe_pct_last = snow.json()[wshed_alt][0]['basin_index']['wteq_ly_per_med']   
    
    if swe_pct_cur is None:
        swe_pct_cur = -9999
    else:
        swe_pct_cur = int(swe_pct_cur)
    
    if swe_pct_last is None:
        swe_pct_last = -9999
    else:
        swe_pct_last = int(swe_pct_last)
    

    
    if watershed =='state_of_nevada_and_eastern_sierra':
        allsites = ['Lake Tahoe','Marlette Lk nr Carson City','Donner Lake','Prosser Reservoir','Independence Lake','Stampede Reservoir','Boca Reservoir','Lahontan Reservoir','Topaz Lk nr Topaz','Bridgeport Reservoir','Rye Patch Re nr Rye Patch, NV','Chimney Creek Reservoir','Wild Horse Reservoir','Lake Mohave','Lake Mead','Lake Powell']
        subbasins = []
        subbasin_clean = []
        SWSI_shed = []
        fname = "00_NVCA_Statewide"
        wshed_alt = 'state of nevada and eastern sierra'
        cleantxt = 'State of Nevada and Eastern Sierra'     
    elif watershed == 'lake_tahoe':
        allsites = ['Lake Tahoe','Marlette Lk nr Carson City']
        subbasins = []
        subbasin_clean = []
        SWSI_shed = []
        fname = "01_Tahoe" 
        wshed_alt = 'lake tahoe'
        cleantxt = "Lake Tahoe Basin"
    elif watershed == 'truckee':
        allsites = ['Donner Lake','Prosser Reservoir','Independence Lake','Stampede Reservoir','Boca Reservoir']
        subbasins = []
        subbasin_clean = []
        SWSI_shed = []
        fname = "02_Truckee" 
        wshed_alt = 'truckee'
        cleantxt = "Truckee River Basin"
    elif watershed == 'carson':
        allsites = ['Lahontan Reservoir']
        subbasins = []
        subbasin_clean = []
        SWSI_shed = []
        fname = "03_Carson" 
        wshed_alt = 'carson'
        cleantxt = "Carson River Basin"
    elif watershed == 'walker':
        allsites = ['Topaz Lk nr Topaz','Bridgeport Reservoir']
        subbasins = []
        subbasin_clean = []
        SWSI_shed = []
        fname = "04_Walker" 
        wshed_alt = 'walker'
        cleantxt = "Walker River Basin"
    elif watershed == 'northern_great_basin':
        allsites = []
        subbasins = []
        subbasin_clean = []
        SWSI_shed = []
        fname = "05_NorthernGreatBasin" 
        wshed_alt = 'northern great basin'
        cleantxt = "Northern Great Basin"
    elif watershed == 'upper_humboldt':
        allsites = []
        subbasins = []
        subbasin_clean = []
        SWSI_shed = []
        fname = "06_UpperHumboldt" 
        wshed_alt = 'upper humboldt'
        cleantxt = "Upper Humboldt River Basin"
    elif watershed == 'lower_humboldt':
        allsites = ['Rye Patch Re nr Rye Patch, NV','Chimney Creek Reservoir']
        subbasins = []
        subbasin_clean = []
        SWSI_shed = []
        fname = "07_LowerHumboldt"
        wshed_alt = 'lower humboldt' 
        cleantxt = "Lower Humboldt River Basin"
    elif watershed == 'clover_valley_and_franklin':
        allsites = []
        subbasins = []
        subbasin_clean = []
        SWSI_shed = []
        fname = "08_CloverValley&Franklin" 
        wshed_alt = 'clover valley and franklin' 
        cleantxt = "Clover Valley and Franklin River Basin"
    elif watershed == 'snake':
        allsites = []
        subbasins = []
        subbasin_clean = []
        SWSI_shed = []
        fname = "09_Snake" 
        wshed_alt = 'snake' 
        cleantxt = "Snake River Basin"
    elif watershed == 'owyhee':
        allsites = ['Wild Horse Reservoir']
        subbasins = []
        subbasin_clean = []
        SWSI_shed = []
        fname = "10_Owyhee" 
        wshed_alt = 'owyhee'
        cleantxt = "Owyhee River Basin"
    elif watershed == 'eastern_nevada':
        allsites = []
        subbasins = []
        subbasin_clean = []
        SWSI_shed = []
        fname = "11_EasternNevada" 
        wshed_alt = 'eastern nevada'
        cleantxt = "Eastern Nevada"
    elif watershed == 'spring_mountains':
        allsites = []
        subbasins = []
        subbasin_clean = []
        SWSI_shed = []
        fname = "12_SpringMtns" 
        wshed_alt = 'spring mountains' 
        cleantxt = "Spring Mountains"
    elif watershed == 'surprise_valley-warner_mtns':
        allsites =[]
        subbasins=[]
        subbasin_clean=[]
        SWSI_shed=[]
        fname = '14_SurpriseValley'
        wshed_alt = 'surprise valley-warner mtns' 
        cleantxt = 'Surprise Valley - Warner Mountains'
    elif watershed == 'Upper_Colorado_Region':
        allsites =['Lake Powell','Lake Mead','Lake Mohave']
        subbasins=[]
        subbasin_clean=[]
        SWSI_shed=[]
        fname = '13_ColoradoBasin'
        wshed_alt = ['Upper Colorado Region']  
        cleantxt = 'Colorado Basin'   
        
    
    start = str(ReportYear-10)+'-'+'01'+'-'+'01'
    
    
    
    
    
    if allsites!=[] and watershed!='Upper_Colorado_Region': # for watersheds that have reservoirs, except CO, grab those below
        
        # reservoir station triplets from meta data are keys
        triplet_keys = list(res_d[wshed_alt]['site_meta'].keys()) #grab watershed according to its list index

        res_data = []
        for i in range(len(triplet_keys)): # loop through keys (triplets)
            
            res_data.append(
                {
                    'name': res_d[wshed_alt]['site_meta'][triplet_keys[i]]['name'],
                    'res_cap': res_d[wshed_alt]['res_cap'][triplet_keys[i]],
                    'res_curr': res_d[wshed_alt]['res_curr'][triplet_keys[i]],
                    'res_ly': res_d[wshed_alt]['res_ly'][triplet_keys[i]],
                   }
                )
        

        
        # create dataframe and add current and last year percent capacity
        ind_res_df = pd.DataFrame(res_data)
        ind_res_df['res_curr_per_cap'] = (ind_res_df['res_curr']/ind_res_df['res_cap']*100)
        ind_res_df['res_ly_per_cap'] = (ind_res_df['res_ly']/ind_res_df['res_cap']*100)
        ind_res_df = ind_res_df.set_index('name')
        
        
        # filter for reservoirs within the watershed only
        res = ind_res_df[ind_res_df.index.isin(allsites)]
    
    # reservoirs on colorado need to be handled differently    
    if  allsites!=[] and (watershed =='Upper_Colorado_Region' or watershed =='state_of_nevada_and_eastern_sierra') :  
        # need to grab lakes powell, mead, and mohave separately
        # make sure wy is converted to calendar year (only needed for autumn time reports)

        col_res_url = f'https://nwcc-apps.sc.egov.usda.gov/aws-api/wsor/getResData?basinType=ca&pubMonth={ReportMonth}&pubYear={ReportYear}&basin=Colorado&format=json'
        col_res_api = requests.get(col_res_url)
        col_res_json = col_res_api.json()
               
        col_keys = ['09379900:AZ:BOR','09421000:AZ:BOR','09422500:AZ:BOR']
        
        col_res =[]
        for key in col_keys:
            col_res.append(
                {
                    'name': col_res_json['colorado'][0]['site_meta'][key]['name'],
                    'res_cap': col_res_json['colorado'][0]['res_cap'][key],
                    'res_curr': col_res_json['colorado'][0]['res_curr'][key],
                    'res_ly': col_res_json['colorado'][0]['res_ly'][key],
                    }
                )
        col_res_df = pd.DataFrame(col_res)
        col_res_df['res_curr_per_cap'] = (col_res_df['res_curr']/col_res_df['res_cap']*100)
        col_res_df['res_ly_per_cap'] = (col_res_df['res_ly']/col_res_df['res_cap']*100)
        col_res_df = col_res_df.set_index('name')
        # slap colorado res numbers into bigger dataframe
        if watershed == 'state_of_nevada_and_eastern_sierra':
            res = pd.concat([res, col_res_df])
        else: res = col_res_df # for Upper Colorado Watershed
    elif allsites ==[]:
         res = []
    
    if allsites != []:     
        res.columns = [str(i) for i in res.columns] 
        basin_res_pct_last = int((res['res_ly'].sum()/res['res_cap'].sum())*100)
        basin_res_pct_this = int((res['res_curr'].sum()/res['res_cap'].sum())*100) 
    
    
    
    
    
    print('Downloading SWE, PCP, and Soil Moisture Data')
    if watershed !='state_of_nevada_and_eastern_sierra' and watershed !='surprise_valley-warner_mtns' and watershed != 'Upper_Colorado_Region':
        #download precip, swe, and soil moisture data from the web
        pcpall = pd.read_csv('https://nwcc-apps.sc.egov.usda.gov/awdb/basin-plots/POR/PREC/assocHUCnv_8/%s.csv' %(watershed))
        sweall = pd.read_csv('https://nwcc-apps.sc.egov.usda.gov/awdb/basin-plots/POR/WTEQ/assocHUCnv_8/%s.csv'%(watershed))
        moiall = pd.read_csv('https://nwcc-apps.sc.egov.usda.gov/awdb/basin-plots/POR/SMS/assocHUCnv_8/%s.csv'%(watershed))
    elif watershed =='state_of_nevada_and_eastern_sierra':
        #statewide data
        sweall = pd.read_csv('https://nwcc-apps.sc.egov.usda.gov/awdb/basin-plots/POR/WTEQ/assocHUCnv3/state_of_nevada_and_eastern_sierra.csv')
        pcpall = pd.read_csv('https://nwcc-apps.sc.egov.usda.gov/awdb/basin-plots/POR/PREC/assocHUCnv3/state_of_nevada_and_eastern_sierra.csv')
        moiall = pd.read_csv('https://nwcc-apps.sc.egov.usda.gov/awdb/basin-plots/POR/SMS/assocHUCnv3/state_of_nevada_and_eastern_sierra.csv')
    elif watershed == 'surprise_valley-warner_mtns':
        pcpall = pd.read_csv('https://nwcc-apps.sc.egov.usda.gov/awdb/basin-plots/POR/PREC/assocHUCnv2_8/%s.csv' %(watershed))
        sweall = pd.read_csv('https://nwcc-apps.sc.egov.usda.gov/awdb/basin-plots/POR/WTEQ/assocHUCnv2_8/%s.csv'%(watershed))
        moiall = []    
    elif watershed == 'Upper_Colorado_Region':   
        pcpall = pd.read_csv('https://nwcc-apps.sc.egov.usda.gov/awdb/basin-plots/POR/PREC/assocHUC2/14_%s.csv' %(watershed))
        sweall = pd.read_csv('https://nwcc-apps.sc.egov.usda.gov/awdb/basin-plots/POR/WTEQ/assocHUC2/14_%s.csv'%(watershed))
        moiall = pd.read_csv('https://nwcc-apps.sc.egov.usda.gov/awdb/basin-plots/POR/SMS/assocHUC2/14_%s.csv'%(watershed))   
    
    #identify columns of interest in the big dataframes downloaded above
    curyear_pcp = [col for col in pcpall if  col.startswith(str(ReportYear)) or col.startswith(str(ReportYear-1)) or col.startswith('Min') or col.startswith('Max') or col.startswith("Median ('91-'20)") or col.startswith('10%') or col.startswith('30%') or col.startswith('70%') or col.startswith('90%')     ]
    curyear_swe = [col for col in sweall if col.startswith(str(ReportYear)) or col.startswith(str(ReportYear-1)) or col.startswith('Min') or col.startswith('Max') or col.startswith("Median ('91-'20)") or col.startswith('10%') or col.startswith('30%') or col.startswith('70%') or col.startswith('90%')     ]
    
    if len(moiall)!=0:
        curyear_moi = [col for col in moiall if  col.startswith(str(ReportYear)) or col.startswith(str(ReportYear-1)) or col.startswith('Min') or col.startswith('Max') or col.startswith('Median (POR)') or col.startswith('10%') or col.startswith('30%') or col.startswith('70%') or col.startswith('90%')     ]
    
    #parse out the columns of interest
    pcp=pcpall[curyear_pcp]
    swe=sweall[curyear_swe]
    if len(moiall)!=0:
        moi=moiall[curyear_moi]
    else:
        moi = []
    
    #Generate datetime to use as index.  Note that the years don't really matter here.  I'm just using the 2020 water year as the index.
    temp = pd.to_datetime(pd.date_range(start = '2019-10-01', periods=366).strftime('%m-%d-%y'))
    
    #set the index for the figure dataframe.  
    #swe['Date'] = temp
    swe.set_index(temp,inplace=True)
    
    #pcp['Date'] = temp
    pcp.set_index(temp,inplace=True)
    
    #moi['Date'] = temp
    if len(moiall)!=0:
        moi.set_index(temp,inplace=True)
    
    
    
    #extract current, last year, and normal SWE.  calculate the percentages.  NOTE: '2020' is basically a dummy year in the index.
    s_cur=round(float(swe.loc['2020'+'-'+str(ReportMonth)+'-01',swe.columns.str.startswith(str(ReportYear))]),1)
    s_last=round(float(swe.loc['2020'+'-'+str(ReportMonth)+'-01',swe.columns.str.startswith(str(ReportYear-1))]),1)
    s_norm=round(float(swe.loc['2020'+'-'+str(ReportMonth)+'-01',swe.columns.str.startswith('Median')]),1)    
    
    
    
    
    
    if len(moiall)!=0:
        sm_cur=round(float(moi.loc['2020'+'-'+str(ReportMonth)+'-01',moi.columns.str.startswith(str(ReportYear))]))
        sm_last=round(float(moi.loc['2020'+'-'+str(ReportMonth)+'-01',moi.columns.str.startswith(str(ReportYear-1))]))
    else:
        sm_cur = []
        sm_last = []
    
    
                
    if s_cur == 0:
        txt1 = 'SNOTEL sites in the {} are currently snow free. '.format(cleantxt)
    if s_norm == 0 and s_cur >0:
        txt1 = 'SNOTEL sites in the {} are currently reporting {}" of Snow Water Equivalent. '.format(cleantxt,str(int(s_cur)))   
    if watershed == 'eastern_nevada' and s_cur >0:
        if swe_pct_cur == swe_pct_last:
            txt1 = 'Snowpack in {} is well below normal at {}% of median, which is the same as this time last year. '.format(cleantxt,str(int(swe_pct_cur)))
        elif swe_pct_cur<=70:
            txt1 = 'Snowpack in {} is well below normal at {}% of median, compared to {}% at this time last year. '.format(cleantxt,str(int(swe_pct_cur)),str(int(swe_pct_last)))           
        elif swe_pct_cur>70 and swe_pct_cur<90:
            txt1 = 'Snowpack in {} is below normal at {}% of median, compared to {}% at this time last year. '.format(cleantxt,str(int(swe_pct_cur)),str(int(swe_pct_last)))        
        elif swe_pct_cur>=90 and swe_pct_cur<=110:
            txt1 = 'Snowpack in {} is about normal at {}% of median, compared to {}% at this time last year. '.format(cleantxt,str(int(swe_pct_cur)),str(int(swe_pct_last)))
        elif swe_pct_cur>110 and swe_pct_cur<130:
            txt1 = 'Snowpack in {} is above normal at {}% of median, compared to {}% at this time last year. '.format(cleantxt,str(int(swe_pct_cur)),str(int(swe_pct_last)))
        elif swe_pct_cur>=130:
            txt1 = 'Snowpack in {} is well above normal at {}% of median, compared to {}% at this time last year. '.format(cleantxt,str(int(swe_pct_cur)),str(int(swe_pct_last)))              
    if watershed != 'eastern_nevada' and s_cur!=0:
        if swe_pct_cur == swe_pct_last:
            txt1 = 'Snowpack in the {} is well below normal at {}% of median, which is the same as this time last year. '.format(cleantxt,str(int(swe_pct_cur)))           
        elif swe_pct_cur<=70:
            txt1 = 'Snowpack in the {} is well below normal at {}% of median, compared to {}% at this time last year. '.format(cleantxt,str(int(swe_pct_cur)),str(int(swe_pct_last)))           
        elif swe_pct_cur>70 and swe_pct_cur<90:
            txt1 = 'Snowpack in the {} is below normal at {}% of median, compared to {}% at this time last year. '.format(cleantxt,str(int(swe_pct_cur)),str(int(swe_pct_last)))        
        elif swe_pct_cur>=90 and swe_pct_cur<=110:
            txt1 = 'Snowpack in the {} is about normal at {}% of median, compared to {}% at this time last year. '.format(cleantxt,str(int(swe_pct_cur)),str(int(swe_pct_last)))
        elif swe_pct_cur>110 and swe_pct_cur<130:
            txt1 = 'Snowpack in the {} is above normal at {}% of median, compared to {}% at this time last year. '.format(cleantxt,str(int(swe_pct_cur)),str(int(swe_pct_last)))
        elif swe_pct_cur>=130:
            txt1 = 'Snowpack in the {} is well above normal at {}% of median, compared to {}% at this time last year. '.format(cleantxt,str(int(swe_pct_cur)),str(int(swe_pct_last)))
    if watershed == 'state_of_nevada' and s_cur >0: 
        if swe_pct_cur == swe_pct_last:
            txt1 = 'The snowpack across Northern Nevada and the Eastern Sierra (Truckee, Tahoe, Carson and Walker basins) is well below normal at {}% of median, which is the same as this time last year. '.format(str(int(swe_pct_cur)))                       
        elif swe_pct_cur<=70:
            txt1 = 'The snowpack across Northern Nevada and the Eastern Sierra (Truckee, Tahoe, Carson and Walker basins) is well below normal at {}% of median, compared to {}% at this time last year. '.format(str(int(swe_pct_cur)),str(int(swe_pct_last))           )
        elif swe_pct_cur>70 and swe_pct_cur<90:
            txt1 = 'The snowpack across Northern Nevada and the Eastern Sierra (Truckee, Tahoe, Carson and Walker basins) is below normal at {}% of median, compared to {}% at this time last year. '.format(str(int(swe_pct_cur)),str(int(swe_pct_last)))        
        elif swe_pct_cur>=90 and swe_pct_cur<=110:
            txt1 = 'The snowpack across Northern Nevada and the Eastern Sierra (Truckee, Tahoe, Carson and Walker basins) is about normal at {}% of median, compared to {}% at this time last year. '.format(str(int(swe_pct_cur)),str(int(swe_pct_last)))
        elif swe_pct_cur>110 and swe_pct_cur<130:
            txt1 = 'The snowpack across Northern Nevada and the Eastern Sierra (Truckee, Tahoe, Carson and Walker basins) is above normal at {}% of median, compared to {}% at this time last year. '.format(str(int(swe_pct_cur)),str(int(swe_pct_last)))
        elif swe_pct_cur>=130:
            txt1 = 'The snowpack across Northern Nevada and the Eastern Sierra (Truckee, Tahoe, Carson and Walker basins) is well above normal at {}% of median, compared to {}% at this time last year. '.format(str(int(swe_pct_cur)),str(int(swe_pct_last)))    
    if watershed == 'Upper_Colorado_Region' and s_cur >0: 
        if swe_pct_cur == swe_pct_last:
            txt1 = 'Snowpack in the {} above Lake Powell is well below normal at {}% of median, which is the same as this time last year. '.format(cleantxt,str(int(swe_pct_cur)))           
        elif swe_pct_cur<=70:
            txt1 = 'Snowpack in the {} above Lake Powell is well below normal at {}% of median, compared to {}% at this time last year. '.format(cleantxt,str(int(swe_pct_cur)),str(int(swe_pct_last)))           
        elif swe_pct_cur>70 and swe_pct_cur<90:
            txt1 = 'Snowpack in the {} above Lake Powell is below normal at {}% of median, compared to {}% at this time last year. '.format(cleantxt,str(int(swe_pct_cur)),str(int(swe_pct_last)))        
        elif swe_pct_cur>=90 and swe_pct_cur<=110:
            txt1 = 'Snowpack in the {} above Lake Powell is about normal at {}% of median, compared to {}% at this time last year. '.format(cleantxt,str(int(swe_pct_cur)),str(int(swe_pct_last)))  
        elif swe_pct_cur>110 and swe_pct_cur<130:
            txt1 = 'Snowpack in the {} above Lake Powell is above normal at {}% of median, compared to {}% at this time last year. '.format(cleantxt,str(int(swe_pct_cur)),str(int(swe_pct_last)))
        elif swe_pct_cur>=130:
            txt1 = 'Snowpack in the {} above Lake Powell is well above normal at {}% of median, compared to {}% at this time last year. '.format(cleantxt,str(int(swe_pct_cur)),str(int(swe_pct_last)))
    if ReportMonth != 1:
        if pcp_pct_month<=70:
            txt2 = 'Precipitation in {} was well below normal at {}%, which brings the seasonal accumulation (October-{}) to {}% of median. '.format(dt.date(1900,ReportMonth-1,1).strftime('%B'),str(int(pcp_pct_month)),dt.date(1900,ReportMonth-1,1).strftime('%B'),str(int(pcp_pct_cur)))           
        elif pcp_pct_month>70 and pcp_pct_month<90:
            txt2 = 'Precipitation in {} was below normal at {}%, which brings the seasonal accumulation (October-{}) to {}% of median. '.format(dt.date(1900,ReportMonth-1,1).strftime('%B'),str(int(pcp_pct_month)),dt.date(1900,ReportMonth-1,1).strftime('%B'),str(int(pcp_pct_cur)))            
        elif pcp_pct_month>=90 and pcp_pct_month<=110:
            txt2 = 'Precipitation in {} was about normal at {}%, which brings the seasonal accumulation (October-{}) to {}% of median. '.format(dt.date(1900,ReportMonth-1,1).strftime('%B'),str(int(pcp_pct_month)),dt.date(1900,ReportMonth-1,1).strftime('%B'),str(int(pcp_pct_cur)))              
        elif pcp_pct_month>110 and pcp_pct_month<130:
            txt2 = 'Precipitation in {} was above normal at {}%, which brings the seasonal accumulation (October-{}) to {}% of median. '.format(dt.date(1900,ReportMonth-1,1).strftime('%B'),str(int(pcp_pct_month)),dt.date(1900,ReportMonth-1,1).strftime('%B'),str(int(pcp_pct_cur)))           
        elif pcp_pct_month>=130:
            txt2 = 'Precipitation in {} was well above normal at {}%, which brings the seasonal accumulation (October-{}) to {}% of median. '.format(dt.date(1900,ReportMonth-1,1).strftime('%B'),str(int(pcp_pct_month)),dt.date(1900,ReportMonth-1,1).strftime('%B'),str(int(pcp_pct_cur)))          
    else:
        if pcp_pct_month<=70:
            txt2 = 'Precipitation in {} was well below normal at {}%, which brings the seasonal accumulation (October-{}) to {}% of median. '.format(dt.date(1900,12,1).strftime('%B'),str(int(pcp_pct_month)),dt.date(1900,12,1).strftime('%B'),str(int(pcp_pct_cur)))           
        elif pcp_pct_month>70 and pcp_pct_month<90:
            txt2 = 'Precipitation in {} was below normal at {}%, which brings the seasonal accumulation (October-{}) to {}% of median. '.format(dt.date(1900,12,1).strftime('%B'),str(int(pcp_pct_month)),dt.date(1900,12,1).strftime('%B'),str(int(pcp_pct_cur)))         
        elif pcp_pct_month>=90 and pcp_pct_month<=110:
            txt2 = 'Precipitation in {} was about normal at {}%, which brings the seasonal accumulation (October-{}) to {}% of median. '.format(dt.date(1900,12,1).strftime('%B'),str(int(pcp_pct_month)),dt.date(1900,12,1).strftime('%B'),str(int(pcp_pct_cur)))   
        elif pcp_pct_month>110 and pcp_pct_month<130:
            txt2 = 'Precipitation in {} was above normal at {}%, which brings the seasonal accumulation (October-{}) to {}% of median. '.format(dt.date(1900,12,1).strftime('%B'),str(int(pcp_pct_month)),dt.date(1900,12,1).strftime('%B'),str(int(pcp_pct_cur)))         
        elif pcp_pct_month>=130:
            txt2 = 'Precipitation in {} was well above normal at {}%, which brings the seasonal accumulation (October-{}) to {}% of median. '.format(dt.date(1900,12,1).strftime('%B'),str(int(pcp_pct_month)),dt.date(1900,12,1).strftime('%B'),str(int(pcp_pct_cur)))   
    
    
    if watershed == 'surprise_valley-warner_mtns':
        txt3 = ''
    elif sm_cur==sm_last:       
       txt3 ='Soil moisture is at {}% saturation, same as last year at this time. '.format(str(sm_cur))
    elif len(moiall)!=0:
        txt3 = 'Soil moisture is at {}% saturation compared to {}% saturation last year. '.format(str(sm_cur),str(sm_last))
    else:    
        txt3 = ''    
      
    
    
    if allsites == []:
        txt4 = ''
    elif watershed == 'state_of_nevada_and_eastern_sierra':
        txt4=''
    elif basin_res_pct_this == basin_res_pct_last:
        txt4 = 'Reservoir storage is {}% of capacity, same as last year at this time. '.format(str(int(basin_res_pct_this)))
        #txt4 = 'Reservoir storage is at {}% of capactiy, compared to {}% last year. '.format(str(int(res['percent_cur'].sum())),str(int(res['percent_prev'].mean()))
    elif watershed == 'Upper_Colorado_Region':
        txt4 = 'Reservoir storage in the Lower Colorado Basin is {}% of capacity, compared to {}% last year. '.format(str(int(basin_res_pct_this)),str(int(basin_res_pct_last)))
    else:
        if math.isnan(basin_res_pct_this or basin_res_pct_last):
            txt4 = 'Reservoir storage is {}% of capacity, compared to {}% last year. '.format(str(basin_res_pct_this),str(basin_res_pct_last))
        else:   
            txt4 = 'Reservoir storage is {}% of capacity, compared to {}% last year. '.format(str(int(basin_res_pct_this)),str(int(basin_res_pct_last)))
    
    
    txt = txt1+txt2+txt3+txt4
    
    return(pcp,swe,moi,res,MonthlyPctMed,txt,fname,cleantxt,swe_pct_cur,pcp_pct_cur,sm_cur)
