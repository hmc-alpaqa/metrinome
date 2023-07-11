import pandas as pd
import os
import sys


apc_csv_file_path = '/app/code/experiments/function_calls/data/apc_data.csv'
rapc_csv_file_path = '/app/code/experiments/function_calls/data/rapc_data.csv'
fcapc_csv_file_path = '/app/code/experiments/function_calls/data/fcapc_data.csv'
getrgfapc_csv_file_path = '/app/code/experiments/function_calls/data/getrgfapc_data.csv'

if os.path.exists(getrgfapc_csv_file_path):
    getrgfapc_df = pd.read_csv(getrgfapc_csv_file_path)
    getrgfapc_df = getrgfapc_df.iloc[:,1:]
else:
    print("PANIC, no getrgf data, cannot proceed")
    sys.exit()
    

###########Initializing dataframs##############
apc_df = pd.DataFrame(columns = ['graph_name','apc','apc_time'])
apc_df['graph_name'] = getrgfapc_df['graph_name']
apc_df = apc_df.fillna('na')

rapc_df = pd.DataFrame(columns = ['graph_name','rapc','rapc_time'])
rapc_df['graph_name'] = getrgfapc_df['graph_name']
rapc_df = rapc_df.fillna('na')

fcapc_df = pd.DataFrame(columns = ['graph_name','fcapc','fcapc_time'])
fcapc_df['graph_name'] = getrgfapc_df['graph_name']
fcapc_df = fcapc_df.fillna('na')
#############################################

if os.path.exists(apc_csv_file_path):  
    df = pd.read_csv(apc_csv_file_path)
    if df['graph_name'].equals(getrgfapc_df['graph_name']):
        apc_df = df
        apc_df = apc_df.iloc[:,1:] #drop first column
if os.path.exists(rapc_csv_file_path):
    df = pd.read_csv(rapc_csv_file_path)
    if df['graph_name'].equals(getrgfapc_df['graph_name']):
        rapc_df = df
        rapc_df = rapc_df.iloc[:,1:]
if os.path.exists(fcapc_csv_file_path):
    df = pd.read_csv(fcapc_csv_file_path)
    if df['graph_name'].equals(getrgfapc_df['graph_name']):
        fcapc_df = df
        fcapc_df = fcapc_df.iloc[:,1:]

merge1 = pd.merge(apc_df,rapc_df)
merge2 = pd.merge(merge1, fcapc_df)
mergefinal = pd.merge(merge2, getrgfapc_df)

new_order = ['graph_name','apc','rapc','fcapc','getrgfapc','apc_time','rapc_time','fcapc_time','getrgfapc_time','longest for getrgf','longest time','case','gamma']
mergefinal = mergefinal[new_order]

print('=========================printing final data table=================================')
print(mergefinal)
# print(mergefinal[['apc','rapc','fcapc','ogapc','nfcapc','getrgfapc']])

mergefinal.to_csv("/app/code/experiments/function_calls/data/final_data.csv")