#Repository for Healthcare Analytics – Recommender system for hospitals based on Medicare ratings and patient surveys in Python

#Project description

•	Downloaded the latest data set for Hospital Compare from data.medicare.gov and uncompressed it into numerous files in CSV format 
•	Processed All CSV files with an encoding of cp1252, removing any nulls, and writing them out in utf-8 encoding
•	Updated every file, every column with given naming standards with OS independent path fetching
•	Created an SQL based database using DB Browser for SQLite and then created a table to hold each of the files in the data set, and parse and load each of the data files into a table in the database. 
•	Fetched the overall ranking for hospitals defined at national and state level and then created excel sheets for different states and one for the US to capture top 100 hospitals.
•	Measured minimum, maximum, average and standard deviation statistics for Timely and Effective Care measures at Nationwide level and for every state level

•	Package used: os, glob, requests, openpyxl, sqlite3, zipfile, csv, operator, statistics
