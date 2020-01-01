# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 20:17:36 2019

@author: Anusha
"""
#import the packages required
import pandas as pd

#variables needed for ease of file access
file_1= r'C:\Users\venka\Desktop\drug_abuse_data.csv'
file_2= r'C:\Users\venka\Desktop\ucr_by_state.csv'

#path to store the output files
output= r'C:/Users/venka/Desktop/'
output_file1='merged'
output_file2='corr'

#read the files into variables
drug_df=pd.read_csv(file_1)
drug_df.head()
crime_df=pd.read_csv(file_2)
crime_df.head()

#remove white spaces in the fields 'jurisdiction' from crime_df and 'state' from drug_df
crime_df['jurisdiction']=crime_df['jurisdiction'].str.strip(' ')
drug_df['state']=drug_df['state'].str.strip(' ')

#merge the two files on the keys 'state' and 'year' 
merged_df=drug_df.merge(crime_df, left_on=['state','year'],right_on=['jurisdiction','year'])
merged_df.head()

#columns of the merged data
merged_df.columns

#drop 'state_population' column as it is present in both the dataframes
merged_df = merged_df.drop('state_population',axis=1)
merged_df=merged_df.drop('jurisdiction',axis=1)

#check the data types of columns
merged_df.dtypes

#convert columns 'year' and 'state_code' to object type
merged_df['year']=merged_df['year'].astype('str')
merged_df['state_code']=merged_df['state_code'].astype('str')

#columns from and after 'violent_crime_total' has character ',' in the value which makes them object type
#process to convert them into numeric type

#get the index of the column 'violent_crime_total'
merged_df.columns.get_loc('violent_crime_total')

#remove the character ',' from the columns
for col in  merged_df.columns[14:]:    
    merged_df[col]=merged_df[col].str.replace(',','')

#change the datatypes to float64   
for col in  merged_df.columns[14:]:
    merged_df[col] = merged_df[col].astype('float64')


#datatypes are now converted
merged_df.dtypes

#check for the null values in the combined dataframe
merged_df.isnull().sum()
#no missing values are found in the dataframe 

#create a new calculated column 'Total_crime' and assign ''
merged_df['Total_crime']=''

#calculate the value of Total_crime as sum of all other crimes i.e, columns from index 14
cols=merged_df.columns.to_list()[14:]
merged_df['Total_crime']=merged_df[cols].sum(axis=1)

#calculated column 'Pct_crime' which is percent change of Total_crime for each year
merged_df['Pct_crime']=merged_df[['state','Total_crime']].groupby(by='state').pct_change()

#saving the dataframe into csv
merged_df.to_csv(output+output_file1,index_label='Rowid')

#state with highest crime over all the years
merged_df.groupby(by=['state']).sum()['Total_crime'].idxmax()
#state with highest gdp over all the years
merged_df.groupby(by=['state']).sum()['gdp_per_capita'].idxmax()

#correlation matrix
merged_corr=merged_df.corr()

merged_corr.to_csv(output+output_file2,index_label='index')










