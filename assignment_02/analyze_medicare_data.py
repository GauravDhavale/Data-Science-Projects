# -*- coding: utf-8 -*-
"""
Created on Tue July 07 19:00:00 2017

@author: Gaurav
"""

import os 
import glob 
import requests
import openpyxl
import sqlite3 

#url for CSV FLAT zip file from data.medicare.gov for Hospital Compare data
url_hospital =  "https://data.medicare.gov/views/bg9k-emty/files/0a9879e0-3312-4719-a1db-39fd114890f1?content_type=application%2Fzip%3B%20charset%3Dbinary&filename=Hospital_Revised_Flatfiles.zip"

#create a directory 
staging_dir_name = "staging"
fix_staging_dir_name = "staging_fixed"  #csv files stored in this directory after null fixup

def createDirectory(dir_name):
    if not os.path.isdir(dir_name): #directory exists or not check
        #create a directory as it does not exists
        os.mkdir(dir_name)
        
        
#This function is used to access the dataset URL, fetch the data and load it into the directory
def fetchExtractOnlineDataset():
    import zipfile
    # using os.path.join will make your code OS independent
    zip_file_name = os.path.join(staging_dir_name,"hospital_compare_data.zip")
    if not os.path.isfile(zip_file_name):
        r = requests.get(url_hospital)
        zf = open(zip_file_name, "wb")
        zf.write(r.content) # write content to hospital_compare_data.zip file
        zf.close()
    z = zipfile.ZipFile(zip_file_name, 'r') #read the zip file
    z.extractall(staging_dir_name) #extract the zip file
    z.close()

#read every csv file and write a new file which exclude null from original file
def removeNullFromFile():
    glob_dir = os.path.join(staging_dir_name, "*.csv")
    for file_name in glob.glob(glob_dir):
        fn =  os.path.join(staging_dir_name,os.path.basename(file_name))
        in_fp = open(fn, 'rt', encoding ='cp1252')   #rt = read text
        input_data = in_fp.read()
        in_fp.close()
        #getting file name 
        new_file_name = os.path.basename(file_name)
        createDirectory(fix_staging_dir_name)
        #store files into new directory after null fixup
        ofn =  os.path.join(fix_staging_dir_name,new_file_name)
        out_fp = open(ofn, 'wt', encoding ='utf-8')  # wt = write text
        for c in input_data:
            if c != '\0':
                out_fp.write(c)
        out_fp.close()

#this function is used to transform given value into the required format
def transformName(input_name, name_type):
    new_input_name = input_name
    #Convert all letters to lower case
    new_input_name = new_input_name.lower()
    #Replace each blank “ “ with an underscore “_”
    new_input_name = new_input_name.strip()
    new_input_name = new_input_name.replace(" ", "_")
    #Replace each dash or hyphen “-“ with an underscore “_”
    new_input_name = new_input_name.replace("-", "_")
    #Replace each percent sign “%” with the string “pct”
    new_input_name = new_input_name.replace("%", "pct")
    #Replace each forward slash “/” with an underscore “_”
    new_input_name = new_input_name.replace("/", "_")
    #If a table name starts with anything other than a letter “a” through “z” then 
    # prepend “t_” to the front of the table name
    if name_type == "tableName":
        if not new_input_name[0].isalpha():
            new_input_name = "t_" + new_input_name
    else:
        if not new_input_name[0].isalpha():
            # its column so prepend "c_"
            new_input_name = "c_" + new_input_name
    return new_input_name

#This function will create database and table definition
def createDatabaseAndTable():
    try:
        import csv
        conn = sqlite3.connect("medicare_hospital_compare.db")
        c1 = conn.cursor()
        glob_dir = os.path.join(fix_staging_dir_name, "*.csv")
        for file_name in glob.glob(glob_dir):
            #This file is corrupt hence ignored
            if not os.path.basename(file_name) == "FY2015_Percent_Change_in_Medicare_Payments.csv":
                new_table_name = transformName(os.path.splitext(os.path.basename(file_name))[0], "tableName")
                file_path = os.path.join(fix_staging_dir_name,os.path.basename(file_name))
                with open(file_path, "r", encoding ='utf-8') as f:
                    reader = csv.reader(f)
                    col_list = next(reader)
                #prepare table creation query
                sql_str_create = """create table if not exists """ + new_table_name+ """ ( """
                for col_name in col_list:
                    sql_str_create += transformName(col_name, "column") + " text, "
                #remove last extra delimiter
                sql_str_create = sql_str_create[:-2]
                sql_str_create += " ) "
                sql_str_drop = """drop table if exists """ + new_table_name 
                c1.execute(sql_str_drop)
                c1.execute(sql_str_create)
                # table insert query 
                sql_str_insert = """insert into  """ + new_table_name+ """ ( """ + ', '.join( transformName(row, 'column') for row in col_list)+ """ ) values ( """+ ''.join('?, ' for col in col_list)
                sql_str_insert = sql_str_insert[:-2] + """ ) """
                #print(new_table_name)
                #print(sql_str_insert)
                #insert rows into table
                with open(file_path, "r", encoding ='utf-8') as f:
                    reader = csv.reader(f)
                    next(f)
                    for row in reader:                       
                        if len(row) <= len(col_list):
                            #empty rows binding issue resolution
                            if len(row) == 1 :
                                #excluding empty rows
                                if row[0].strip() != '':
                                    counter = len(col_list) - len(row)
                                    while(counter > 0):
                                        row.append('')
                                        counter = counter - 1
                                    #print(new_table_name)
                                    #print(row)  
                                    sql_row = tuple(row)
                                    c1.execute(sql_str_insert, sql_row)
                            else:
                                #rows and column are equal
                                counter = len(col_list) - len(row)
                                while(counter > 0):
                                    row.append('')
                                    counter = counter -1
                                #print(new_table_name)
                                #print(row)  
                                sql_row = tuple(row)
                                c1.execute(sql_str_insert, sql_row)
                        
                conn.commit()
        conn.close()
    finally:
        conn.close() #close database connection
        

# This function will create excel workbooks
def createInHouseHospitalRankingWorkbook():
    #MS Excel Workbook of In House Proprietary Hospital Rankings and Focus List of States
    k_url = 'http://kevincrook.com/utd/hospital_ranking_focus_states.xlsx'
    r = requests.get(k_url)
    xf = open("hospital_ranking_foucus_states.xlsx", "wb") 
    xf.write(r.content)
    xf.close()

def createHospitalRankingWorkbook():
    wb = openpyxl.Workbook()
    sheet_1 = wb.create_sheet("Nationwide")
    #add headers to excel sheet
    sheet_1.cell(row = 1 , column =1, value = "Provider ID")
    sheet_1.cell(row = 1 , column =2, value = "Hospital Name")
    sheet_1.cell(row = 1 , column =3, value = "City")
    sheet_1.cell(row = 1 , column =4, value = "State")
    sheet_1.cell(row = 1 , column =5, value = "County")
    wb.remove_sheet(wb.get_sheet_by_name("Sheet"))
    #load data for top 100 hospital
    wb2 = openpyxl.load_workbook("hospital_ranking_foucus_states.xlsx")
    ranking_sheet = wb2.get_sheet_by_name("Hospital National Ranking")
    list_provider_id = []
    i= 2 #start with 2 to ignore header
    while ranking_sheet.cell(row = i, column = 2).value <= 100 :
        list_provider_id.append(ranking_sheet.cell(row = i, column = 2).value)
        #write data into hospital_ranking file
    try:
        #connect to database
        conn = sqlite3.connect("medicare_hospital_compare.db")
        c1 = conn.cursor()
        sql_str = "select provider_id, hospital_name, city, state, county_name from hospital_general_information where provider_id in ({})".format(','.join('?' * len(list_provider_id)))
        sql_tupple = list(list_provider_id) 
        rows = c1.execute(sql_str, sql_tupple)
        for row in rows:
            print(row) 
    finally:
        conn.close()     
    wb.save("hospital_ranking.xlsx")
    wb.close()

    
#used to invoke functions in sequence
def executeFunctions():
    #create directory to store dataset
    createDirectory(staging_dir_name)
    #fwtch dataset from online source and extract to directory
    fetchExtractOnlineDataset()
    #remove null data from csv files
    removeNullFromFile()
    #store data from csv file to database
    createDatabaseAndTable() 
    #create workbooks
    createInHouseHospitalRankingWorkbook()
    #createHospitalRankingWorkbook()
    
executeFunctions()