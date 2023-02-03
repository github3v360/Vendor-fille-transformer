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
import logging
import io

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

def collect_logs(handler):
    log_data = []
    for record in handler.records:
        log_data.append(handler.formatter.format(record))
    return "\n".join(log_data)

import logging
import io
import google.cloud.storage as storage

def log_message(message, log_buffer):
    # Log the message to a buffer
    logging.basicConfig(level=logging.INFO, stream=log_buffer)
    logging.info(message)

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

    log_bucket_name = os.environ['LOGS_BUCKET']
    log_bucket = client.bucket(log_bucket_name)
    log_blob = bucket.blob("logs.log")
    
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    log_buffer = io.StringIO()

    log_message("Function processed a request please bhai ho ja", log_buffer)
    log_message("ksdnsnkncnncfkenekn", log_buffer)
    log_string = log_buffer.getvalue()
    print(log_string)
    log_blob.upload_from_string(log_string)
    print("hi")
    log_blob.make_public()
    
    for everyobj in bucketPathArray:
        currentFilePath=everyobj['mapValue']['fields']['filePath']['stringValue']
    
        blob=bucket.blob(currentFilePath)
        blob.download_to_filename(os.path.join(tempdir, currentFilePath.split('/')[-1]))

        out_df = Extraction_of_entire_file.extract_entire_file(os.path.join(tempdir, currentFilePath.split('/')[-1]),False,logger)
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

        log_blob.upload_from_string(collect_logs(handler), content_type='text/plain')