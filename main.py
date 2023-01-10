# Importing Required Libraries

import tempfile
import os
from google.cloud import storage
import numpy as np
import openpyxl
import uuid
import firebase_admin
from datetime import datetime as dt 
from firebase_admin import credentials, firestore
import math
import time
import fnmatch
import pickle
import yaml
import pandas as pd
# from src.utils.all_utils import *

# Bucket Realted parameters and functions

tempdir = tempfile.gettempdir()
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)
db = firestore.client()

tempdir = tempfile.mkdtemp()

client = storage.Client(project="friendlychat-bb9ff")


def uploadToBucket(bucketName, path, filepath):
    '''
    function to upload file to cloud storage bucket
    bucketName = bucket name where file is to be uploaded,
    path = path inside the bucket
    filepath = location of the file to be uploaded 

    assuming that file to be uploaded is always .xlsx file
    '''
    bucket = client.get_bucket(bucketName)

    blob = bucket.blob(path)
    
    with open(filepath, 'rb') as file:
        blob.upload_from_file(file)

    blob.make_public()

def downloadFromBucket(bucketName, path, filepath):
    bucket = client.get_bucket(bucketName)

    blob = bucket.blob(path)
    doesFileExist = blob.exists()
    print("download",filepath,path,bucketName)
    if not doesFileExist:
        raise Exception('remote file not present')
    
    blob.download_to_filename(filepath)

def exportDataFrameToExcel(dataframe, path):
    dataframe.to_excel(path, index = False)

def read_excel(filename):
    assert filename.split('.')[-1] in ['xlsx', 'xls'] ,'Not a excel file'
    return pd.read_excel(filename,header=None,engine='openpyxl')
  
def addSummaryFileMeta(summaryFilePath, uid, VENDORNAME):
  collection_ref = db.collection('/'.join(['userFiles', uid, 'summaryFiles']))

  data = {
    'filePath' : summaryFilePath,
    'bucket' : summary_bucket,
    'CREATEDAT' :dt.now(),
    'downloadURL' : '/'.join(['https://storage.googleapis.com',summary_bucket, summaryFilePath]),
    'ack' : False,
    'VENDORNAME' : VENDORNAME
  }

  collection_ref.add(data)

def onInventoryFileUpload(inventory, uid, VENDORNAME, CREATEDAT):
    inventory['VENDORNAME'] = VENDORNAME

    start_time = time.time()
    try:
        
        masterFilePath = get_master_file_path(uid);
        downloadFromBucket(
            master_bucket,
            masterFilePath,
            os.path.join(tempdir, 'master.xlsx')
        )
        
    except Exception:
        
        masterColumns = {}
        print('exceptiong new dataframe columns',inventory.columns)

        for col in inventory.columns:
            masterColumns[col] = []
            

        for col in ['CREATEDAT', 'LASTMODIFIEDAT']:
            masterColumns[col] = []

        emptyMasterFile = pd.DataFrame(columns = masterColumns)
        print("new dataframe created")
        exportDataFrameToExcel(emptyMasterFile, os.path.join(tempdir, 'master.xlsx'))
    print(3)
    
    master = read_excel(os.path.join(tempdir,'master.xlsx'))
    wb_master = openpyxl.load_workbook(os.path.join(tempdir,'master.xlsx'),data_only = True)
    print(3.1)
    master = mapping(master,wb_master.worksheets[0])
    print(3.2)
    print("master columns",master.columns)
    # inventory['REPORTNO'].replace('','0',inplace=True)
    # fileValue_df.fillna(value=0,inplace=True)
    # master['REPORTNO'] = master['REPORTNO'].astype(np.float64).astype(np.int64)
    # inventory['REPORTNO'] = inventory['REPORTNO'].astype(np.float64).astype(np.int64)
    print(4)
    masterDate= master.merge(inventory,how='outer',on='REPORTNO',indicator=True)
    print(masterDate.columns)
    print(5)
    masterDate['CREATEDAT'] = masterDate['CREATEDAT'].astype(str)
    masterDate['LASTMODIFIEDAT'] = masterDate['LASTMODIFIEDAT'].astype(str)
    masterDate['CREATEDAT'] = masterDate.apply(lambda row : mapDate(row, CREATEDAT), axis = 1)
    print(masterDate)
    print(5.1)
    masterDate['LASTMODIFIEDAT'] = masterDate.apply(lambda row : mapDate2(row, CREATEDAT), axis = 1)
    print(5.2)

    summary = masterDate[masterDate['_merge'] != 'left_only' ]
    print("5.3",summary)
    summary['summary'] = summary.apply(lambda row : map(row), axis = 1)
    print(5.4)
    summary['%Change']= summary.apply(lambda row: mapDiff(row),axis=1)
    print(5.5)
    summary = summary[[column for column in summary.columns if '_y' in column] + ['REPORTNO','CREATEDAT','%Change','summary','LASTMODIFIEDAT']]
    summary=summary.rename(columns={column:column.replace("_y", "") for column in summary.columns})
    print(5.6)
    summary['REPORTNOabc']=summary['REPORTNO']
    summary['%Changeabc']=summary['%Change']
    summary['summaryabc']=summary['summary']

    summary=summary.drop(['REPORTNO','%Change','summary'], axis = 1)
    summary=summary[[column for column in summary.columns if 'abc' in column]+ [column for column in summary.columns if 'abc' not in column]]
    summary=summary.rename(columns={column:column.replace("abc", "") for column in summary.columns})

    print(summary.columns)
    
    masterDate=masterDate[[column for column in masterDate.columns if '_y' not in column]] 
    masterDate=masterDate.rename(columns={column:column.replace("_x", "") for column in masterDate.columns})
    print(masterDate.columns)

    masterDate=pd.concat([masterDate,summary]).drop_duplicates(subset=['REPORTNO'],keep='last')
    masterDate=masterDate.drop(['summary','_merge','%Change'],axis=1)

    
    print(6)
    masterDate['REPORTNOabc']=masterDate['REPORTNO']

    # masterDate['VIDEOLINKabc']=masterDate['VIDEOLINK']
    # masterDate=masterDate.drop(['REPORTNO','VIDEOLINK'], axis = 1)
    masterDate=masterDate.drop(['REPORTNO'], axis = 1)
    masterDate=masterDate[[column for column in masterDate.columns if 'abc' in column]+ [column for column in masterDate.columns if 'abc' not in column]]
    masterDate=masterDate.rename(columns={column:column.replace("abc", "") for column in masterDate.columns})
    masterDate = masterDate.loc[:, masterDate.columns.notna()]
    print("masterDate columns", masterDate.columns)
    
    print(8)
    start_time = time.time()
    exportDataFrameToExcel(summary, os.path.join(tempdir, 'summary.xlsx'))
    summaryFilePath = '/'.join([uid, str(uuid.uuid4()), 'summary.xlsx'])

    uploadToBucket(
        summary_bucket,
        summaryFilePath,
        os.path.join(tempdir, 'summary.xlsx')
    )
    
    addSummaryFileMeta(summaryFilePath, uid, VENDORNAME)
    print(9)
    start_time = time.time()

    exportDataFrameToExcel(masterDate, os.path.join(tempdir, 'master.xlsx'))

    folder =  str(uuid.uuid4())
    newMasterFilePath = '/'.join([uid, folder, 'master.xlsx'])

    uploadToBucket(
        master_bucket,
        newMasterFilePath,
        os.path.join(tempdir, 'master.xlsx')
    )

    with open(os.path.join(tempdir, 'master.pickle'), 'wb+') as pickleFile:
        pickle.dump(masterDate, pickleFile)

    uploadToBucket(
        master_bucket,
        '/'.join([uid, folder, 'master.pickle']),
        os.path.join(tempdir, 'master.pickle')
    )
    
    addMasterFileMeta(newMasterFilePath, uid, VENDORNAME)
    print(10)
    print("{} entire data analysis code took ".format(time.time() - start_time))

def uploadToBucket(bucketName, path, filepath):
        bucket = client.get_bucket(bucketName)

        blob = bucket.blob(path)
        
        with open(filepath, 'rb') as file:
            blob.upload_from_file(file)

        blob.make_public()

def exportDataFrameToExcel(dataframe, path):
        dataframe.to_excel(path)

def hello_firestore(event, context):
    """
    Triggered by a change to a Firestore document.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    print(event)
    resource_string = context.resource
    bucketName= event['value']['fields']['bucket']['stringValue']
    bucket = client.get_bucket(bucketName)

    bucketPathArray = event['value']['fields']['files']['arrayValue']['values']
    filenames=[]

    userId = None
    
    for everyobj in bucketPathArray:
        currentFilePath=everyobj['mapValue']['fields']['filePath']['stringValue']
        print(currentFilePath)
        blob=bucket.blob(currentFilePath)
        blob.download_to_filename(os.path.join(tempdir, currentFilePath.split('/')[-1]))
        fileValue=pd.ExcelFile(os.path.join(tempdir, currentFilePath.split('/')[-1]))
        list_of_sheetname=fileValue.sheet_names
        print("======Listing sheet name =======")
        print(list_of_sheetname)
        global_df=pd.DataFrame()
        global_df['REPORTNO']=[]
        wb = openpyxl.load_workbook(os.path.join(tempdir, currentFilePath.split('/')[-1]),data_only = True)
        for i in list_of_sheetname:
            fd=pd.read_excel(os.path.join(tempdir, currentFilePath.split('/')[-1]),sheet_name=i,header=None)
            print("=========fd with header None =======")
            print(fd.columns)
            print(fd.head())
            fd=pd.read_excel(os.path.join(tempdir, currentFilePath.split('/')[-1]),sheet_name=i)
            print("=========fd with header not None =======")
            print(fd.columns)
            print(fd.head())
            global_df=pd.concat([global_df,fd], axis=0)
        global_df=global_df.reset_index()
        global_df = global_df.drop(['index'], axis=1, errors='ignore')
        userId=currentFilePath.split('/')[0]
        filenames.append(os.path.join(tempdir,currentFilePath.split('/')[-1]))
        print("===========Printing global_df =============")
        print(global_df.head())