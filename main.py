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
from src import Extraction_of_entire_file

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

def helloFirestore(event, context):
    """
    Triggered by a change to a Firestore document.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    
    bucketName= event['value']['fields']['bucket']['stringValue']
    bucket = client.get_bucket(bucketName)

    bucketPathArray = event['value']['fields']['files']['arrayValue']['values']
    filenames=[]

    userId = None
    
    for everyobj in bucketPathArray:
        currentFilePath=everyobj['mapValue']['fields']['filePath']['stringValue']
    
        blob=bucket.blob(currentFilePath)
        blob.download_to_filename(os.path.join(tempdir, currentFilePath.split('/')[-1]))

        log_path = os.path.join(temp_dir,'test.log')

        out_df = Extraction_of_entire_file.extract_entire_file(os.path.join(tempdir, currentFilePath.split('/')[-1]),debug=False,log_path)
        out_df=out_df.reset_index()

        userId=currentFilePath.split('/')[0]
        filenames.append(os.path.join(tempdir,currentFilePath.split('/')[-1]))
    
        summary_bucket = os.environ['SUMMARY_BUCKET']
        exportDataFrameToExcel(out_df, os.path.join(tempdir, 'summary_2.xlsx'))
        summaryFilePath = '/'.join([userId, str(uuid.uuid4()), 'summary_2.xlsx'])
        print("==========user Id and uuid ========")
        print(userId,str(uuid.uuid4()))
        uploadToBucket(
        summary_bucket,
        summaryFilePath,
        os.path.join(tempdir, 'summary_2.xlsx')
        )