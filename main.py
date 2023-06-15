# Importing Required Libraries
import pandas as pd
from src import extraction_of_entire_file
import logging
import io
import tempfile
import os
from google.cloud import storage

from pathlib import Path


# Bucket Realted parameters and functions

tempdir = tempfile.gettempdir()
tempdir = tempfile.mkdtemp()

client = storage.Client(project="friendlychat-bb9ff")

inventory_bucket_name = "business-inventory-files"
summary_bucket_name = "business-summary-files"

def downloadFromBucket(bucketName, path, filepath):
    bucket = client.get_bucket(bucketName)

    blob = bucket.blob(path)
    doesFileExist = blob.exists()
    print("download",filepath,path,bucketName)
    if not doesFileExist:
        raise Exception('remote file not present')
    
    blob.download_to_filename(filepath)


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
    

def delete_file_from_bucket(bucket_name, file_path):

    # Get a reference to your bucket
    bucket = client.bucket(bucket_name)

    # Get a reference to the blob to be deleted
    blob = bucket.blob(file_path)

    # Delete the blob if it exists
    if blob.exists():
        blob.delete()

from google.cloud import storage
import os

def list_files_in_directory(bucket_name, directory_path, folder_names_to_avoid):

    # Get a reference to your bucket
    bucket = client.bucket(bucket_name)

    # Get a list of all blobs in the bucket
    blobs = bucket.list_blobs()

    # Create an empty list to store the file paths
    file_paths = []

    # Loop through all the blobs in the bucket
    for blob in blobs:
        # Check if the blob is a file and is in the specified directory
        if not blob.name.endswith('/') and blob.name.startswith(directory_path):
            # Get the file path relative to the directory
            relative_path = os.path.relpath(blob.name, directory_path)

            folder_name = relative_path.split("/")[0]

            if folder_name in folder_names_to_avoid:continue

            # Add the file path to the list
            file_paths.append(blob.name)

    return file_paths


def convert_to_common_format(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    headers = {
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type,Access-Control-Allow-Origin,crossDomain',        
        'Access-Control-Allow-Origin': '*'
        }
    if request.method == 'OPTIONS':
        # Handle OPTIONS request
        return ('', 204, headers)
    try:
        # Retrieve the parameters from the request
        userId = request.args.get('userId')
        date = request.args.get('date')
        vendor_name = request.args.get('vendor_name')

        folder_names_to_avoid = ["user_files"]
        directory_path = os.path.join(userId,date)

        file_paths = list_files_in_directory(inventory_bucket_name, directory_path, folder_names_to_avoid)
        # sample_file_path = 'v2TGjuzXowbJYwez2BLZbqHSjHG2/20230417/manavnew/1.xlsx'

        log_buffer = io.StringIO()
        logging.basicConfig(level=logging.INFO, stream=log_buffer)

        for file_path in file_paths:

            if ( (file_path.endswith('.csv') or file_path.endswith('.xlsx') or file_path.endswith('.xls')) == False ):
                continue

            print(f"The file path is : {file_path}")

            file_path_splitted = file_path.split("/")

            cur_vendor_name = file_path_splitted[-2]
            cur_file_name = file_path_splitted[-1]


            print(f"Current vendor name: {cur_vendor_name} now changed to : {vendor_name}")
            # cur_vendor_name = vendor_name
            print(f"Current file name: {cur_file_name}")

            file_path_download_to_tempdir = os.path.join(*[tempdir,cur_vendor_name + "_" + cur_file_name])
            

            downloadFromBucket(inventory_bucket_name, file_path, file_path_download_to_tempdir)

            extractor = extraction_of_entire_file.EntireFileExtractor(file_path_download_to_tempdir,False,logging,date,cur_vendor_name)

            out_df = extractor.extract()
            out_df=out_df.reset_index()
            out_df.to_excel(os.path.join(tempdir, 'summary.xlsx'), index = False)

            file_path_for_summary_bucket = file_path_splitted[:-2] + f"/{vendor_name}/" + file_path_splitted[-1]
 
            delete_file_from_bucket(summary_bucket_name,file_path_for_summary_bucket)

            uploadToBucket(summary_bucket_name, file_path_for_summary_bucket, os.path.join(tempdir, 'summary.xlsx'))

            os.remove(file_path_download_to_tempdir)
            os.remove(os.path.join(tempdir, 'summary.xlsx'))
            return ("converted",200,headers)
    except Exception as e:
        return (str(e),200,headers)