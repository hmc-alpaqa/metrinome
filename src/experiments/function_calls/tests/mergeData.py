import pandas as pd
import os
import sys

rapc_csv_file_path = '/app/code/experiments/function_calls/data/rapc_data.csv'
fcapc_csv_file_path = '/app/code/experiments/function_calls/data/fcapc_data.csv'
getrgfapc_csv_file_path = '/app/code/experiments/function_calls/data/getrgfapc_data.csv'
npath_csv_file_path ='/app/code/experiments/function_calls/data/npath_data.csv'

if os.path.exists(getrgfapc_csv_file_path):
    getrgfapc_df = pd.read_csv(getrgfapc_csv_file_path)
    getrgfapc_df = getrgfapc_df.iloc[:,1:]
else:
    print("PANIC, no getrgf data, cannot proceed")
    sys.exit()
    

###########Initializing dataframes##############

rapc_df = pd.DataFrame(columns = ['graph_name','rapc','rapc_time'])
rapc_df['graph_name'] = getrgfapc_df['graph_name']
rapc_df = rapc_df.fillna('na')

fcapc_df = pd.DataFrame(columns = ['graph_name','fcapc','fcapc_time', 'naiveMathTime','naiveFirstHalfTime'])
fcapc_df['graph_name'] = getrgfapc_df['graph_name']
fcapc_df = fcapc_df.fillna('na')

npath_df = pd.DataFrame(columns = ['graph_name','npath','npath_time'])
npath_df['graph_name'] = getrgfapc_df['graph_name']
npath_df = npath_df.fillna('na')
#############################################

if os.path.exists(rapc_csv_file_path):
    df = pd.read_csv(rapc_csv_file_path)
    if df['graph_name'].equals(getrgfapc_df['graph_name']):
        rapc_df = df
        rapc_df = rapc_df.iloc[:,1:] #drop first column
if os.path.exists(fcapc_csv_file_path):
    df = pd.read_csv(fcapc_csv_file_path)
    df.rename(columns = {'firstHalfTime':'naiveFirstHalfTime'}, inplace = True)
    if df['graph_name'].equals(getrgfapc_df['graph_name']):
        fcapc_df = df
        fcapc_df = fcapc_df.iloc[:,1:]
if os.path.exists(npath_csv_file_path):
    df = pd.read_csv(npath_csv_file_path)
    if df['graph_name'].equals(getrgfapc_df['graph_name']):
        npath_df = df
        npath_df = npath_df.iloc[:,1:] #drop first column

merge1 = pd.merge(rapc_df,fcapc_df)
merge2 = pd.merge(merge1, getrgfapc_df)
mergefinal = pd.merge(merge2, npath_df)

new_order = ['graph_name','rapc','fcapc','getrgfapc','npath','rapc_time','fcapc_time','getrgfapc_time','npath_time','firstHalfTime','naiveFirstHalfTime','getrgfTime', 'naiveMathTime','longest for getrgf','longest time','case','gamma']
mergefinal = mergefinal[new_order]

# CHANGES FOR ISSTA SUBMISSION ARTIFACT DOCKER IMAGE (change csvs for readability during test replication)
# comment out when not pushing to docker
# new_order = ['graph_name','rapc','fcapc','getrgfapc','rapc_time','fcapc_time','getrgfapc_time','firstHalfTime','naiveFirstHalfTime','getrgfTime', 'naiveMathTime','longest time','case']
# mergefinal = mergefinal[new_order]
# mergefinal.rename(columns = {'graph_name':'program name'}, inplace = True)
# mergefinal.rename(columns = {'rapc':'apc-r'}, inplace = True)
# mergefinal.rename(columns = {'fcapc':'napc-ip'}, inplace = True)
# mergefinal.rename(columns = {'getrgfapc':'apc-ip'}, inplace = True)
# mergefinal.rename(columns = {'rapc_time':'apc-r time'}, inplace = True)
# mergefinal.rename(columns = {'fcapc_time':'napc-ip time'}, inplace = True)
# mergefinal.rename(columns = {'getrgfapc_time':'apc-ip time'}, inplace = True)
# mergefinal.rename(columns = {'naiveFirstHalfTime':'napc-ip eliminate time'}, inplace = True)
# mergefinal.rename(columns = {'firstHalfTime':'apc-ip eliminate time'}, inplace = True)
# mergefinal.rename(columns = {'getrgfTime':'apc-ip bounding time (GETRGF)'}, inplace = True)
# mergefinal.rename(columns = {'naiveMathTime':'napc-ip bounding time (SYMB-CALC)'}, inplace = True)
# stop commenting out here

print('=========================printing final data table=================================')
print(mergefinal)
# print(mergefinal[['apc','rapc','fcapc','ogapc','nfcapc','getrgfapc']])

mergefinal.to_csv("/app/code/experiments/function_calls/data/final_data.csv")