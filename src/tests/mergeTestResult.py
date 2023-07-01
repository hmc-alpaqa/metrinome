import pandas as pd
import os


apc_csv_file_path = '/app/code/tests/data/apc_data.csv'
fcapc_csv_file_path = '/app/code/tests/data/fcapc_data.csv'
nfcapc_csv_file_path = '/app/code/tests/data/nfcapc_data.csv'
rapc_csv_file_path = '/app/code/tests/data/rapc_data.csv'
getrgfapc_csv_file_path = '/app/code/tests/data/getrgfapc_data.csv'

if os.path.exists(getrgfapc_csv_file_path):
    getrgfapc_df = pd.read_csv(getrgfapc_csv_file_path)
    getrgfapc_df = getrgfapc_df.iloc[:,1:]
else:
    print('PANIC, cannnot merge')

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

nfcapc_df = pd.DataFrame(columns = ['graph_name','nfcapc','nfcapc_time'])
nfcapc_df['graph_name'] = getrgfapc_df['graph_name']
nfcapc_df = nfcapc_df.fillna('na')
#############################################

if os.path.exists(apc_csv_file_path):  
    df = pd.read_csv(apc_csv_file_path)
    if df['graph_name'].equals(getrgfapc_df['graph_name']):
        apc_df = df
        apc_df = apc_df.iloc[:,1:]
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
        fcapc_df = fcapc_df.drop('nonZeroIndex',axis = 1)
if os.path.exists(nfcapc_csv_file_path):
    df = pd.read_csv(nfcapc_csv_file_path)
    if df['graph_name'].equals(getrgfapc_df['graph_name']):
        nfcapc_df = df
        nfcapc_df = nfcapc_df.iloc[:,1:]
        nfcapc_df = nfcapc_df.drop("longest for nfcapc",axis = 1)
        nfcapc_df = nfcapc_df.drop("longest time",axis = 1)
        nfcapc_df = nfcapc_df.drop("numNode",axis = 1)

# print(fcapc_df)
merge1 = pd.merge(apc_df,rapc_df)
merge2 = pd.merge(merge1, fcapc_df)
merge3 = pd.merge(merge2, nfcapc_df)
merge4 = pd.merge(merge3, getrgfapc_df)

new_order = ['graph_name','apc','rapc','fcapc','nfcapc','getrgfapc','apc_time','rapc_time','fcapc_time','nfcapc_time','getrgfapc_time','longest for getrgf','longest time']
merge4 = merge4[new_order]

print(merge4)

merge4.to_csv("/app/code/tests/data/merge_data.csv")