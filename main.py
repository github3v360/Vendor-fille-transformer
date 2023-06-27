# Importing Required Libraries
import pandas as pd
from src import extraction_of_entire_file
import logging
import io
import tempfile
import os
import time
from flask_cors import cross_origin
from google.cloud import storage
import traceback

from pathlib import Path


# Bucket Realted parameters and functions

tempdir = tempfile.gettempdir()
tempdir = tempfile.mkdtemp()

client = storage.Client(project="d360-assist-dev")

inventory_bucket_name = "assist-dev-inventory-bucket"
summary_bucket_name = "assist-dev-summary-bucket"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def downloadFromBucket(bucketName, path, filepath):
    bucket = client.get_bucket(bucketName)

    blob = bucket.blob(path)
    doesFileExist = blob.exists()
    if not doesFileExist:
        raise Exception('remote file not present')
    print("before download to file name",blob)
    blob.download_to_filename(filepath)
    print("after download to file name")


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

def get_file_paths(bucket_name, directory_path):

    primary_folder_path = directory_path
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=primary_folder_path)

    file_paths = []
    # Iterate over the blobs
    for blob in blobs:
        # Get the blob path
        blob_path = blob.name

        if blob_path != primary_folder_path:
            # Append the file path to the list
            file_paths.append(blob_path)
            print(blob_path)
    return file_paths

def list_files_in_directory(bucket_name, directory_path):
    print("bucket name : ",bucket_name)
    print("dr_path:",directory_path)
    # Get a reference to your bucket
    bucket = client.bucket(bucket_name)
    print("Bucket : ",bucket)
    
    # Get a list of all blobs in the bucket
    blobs = bucket.list_blobs()
    print("Blobs : ",blobs)
    # Create an empty list to store the file paths
    file_paths = []

    # Loop through all the blobs in the bucket
    for blob in blobs:
        # Check if the blob is a file and is in the specified directory
        print("Blob name : ",blob.name)
        if not blob.name.endswith('/') and blob.name.startswith(directory_path):
            # Add the file path to the list
            file_paths.append(blob.name)
            print(blob.name)
    print("File Paths ",file_paths)
    return file_paths

def convert_to_common_format(request):
    print("In the function")

    headers = {
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type,Access-Control-Allow-Origin,crossDomain',        
        'Access-Control-Allow-Origin': '*'
        }

    if request.method == 'OPTIONS':
        return ('', 204, headers)
    try:
        # Retrieve the parameters from the request
        userId = request.args.get('userId')
        date = request.args.get('date')
        vendor_name = request.args.get('vendor_name')
        print("All arguments are retrived")
        directory_path = os.path.join(userId,date,"Vendor_files",vendor_name)

        file_paths = get_file_paths(inventory_bucket_name, directory_path)
        print("All file paths discovered in "+str(vendor_name)+"are : ")
        # print(str(len(file_paths)))
        log_buffer = io.StringIO()
        logging.basicConfig(level=logging.INFO, stream=log_buffer)

        nonParsedFiles = []

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

            extractor = extraction_of_entire_file.EntireFileExtractor(file_path_download_to_tempdir,False,logger,date,cur_vendor_name)
            try:
                print(file_path_download_to_tempdir)
                print("Started Converting to common format")
                out_df = extractor.extract()
                print("File Converted")
            except:
                print('Failed Due to: ')
                print(f"Logic Failed for {cur_file_name} file")
                print("-" *50)
                print("Traceback for file  "+cur_file_name)
                traceback.print_exc()
                continue
            try:
                df_clean, df_missing = out_df
                if df_clean.empty and df_missing.empty:
                    continue
                print("Clean file generated"+str(len(df_clean)))
                df_clean = df_clean.reset_index()
                df_clean = df_clean.drop(columns=['index'])
                df_clean.to_excel(os.path.join(tempdir, 'summary.xlsx'), index = False)

                file_dir_for_summary_bucket = os.path.join(*file_path_splitted[:-2],f"/Vendor_files/{vendor_name}","")
                file_path_for_summary_bucket = os.path.join(*file_path_splitted[:-2],f"/Vendor_files/{vendor_name}/",file_path_splitted[-1])

                print(f"File path for summary bucket is {file_path_for_summary_bucket}")

                if file_path.endswith(".csv"):
                    file_path_for_summary_bucket = file_path[:-4]+ "_output" + ".xlsx"
                elif file_path.endswith(".xlsx"):
                    file_path_for_summary_bucket = file_path[:-5] + "_output" + ".xlsx"

                print(f"File path for summary bucket is {file_path_for_summary_bucket}")
                uploadToBucket(summary_bucket_name, file_path_for_summary_bucket, os.path.join(tempdir, 'summary.xlsx'))

                # if not df_missing.empty:
                #     print("Missing file generated"+str(len(df_missing)))
                #     df_missing = df_missing.drop(columns=['index'])
                #     df_missing.to_excel(os.path.join(tempdir1, 'summary1.xlsx'), index = False)

                #     file_dir_for_summary_bucket = os.path.join(*file_path_splitted[:-2],f"/Vendor_files/{vendor_name}","")
                #     file_path_for_summary_bucket = os.path.join(*file_path_splitted[:-2],f"/Vendor_files/{vendor_name}/",file_path_splitted[-1])

                #     print(f"File path for summary bucket is {file_path_for_summary_bucket}")

                #     if file_path.endswith(".csv"):
                #         file_path_for_summary_bucket = file_path[:-4]+ "_nonparsed" + ".xlsx"
                #     elif file_path.endswith(".xlsx"):
                #         file_path_for_summary_bucket = file_path[:-5] + "_nonparsed" + ".xlsx"

                #     nonParsedFiles.append(file_path_for_summary_bucket)

                #     print(f"File path for summary bucket is {file_path_for_summary_bucket}")
                #     uploadToBucket(summary_bucket_name, file_path_for_summary_bucket, os.path.join(tempdir1, 'summary1.xlsx'))     
            
            except Exception as e:
                print('Failed Due to: ')
                print(f"Logic Failed for {cur_file_name} file")
                print("-" *50)
                print("Traceback for file  "+cur_file_name)
                traceback.print_exc()
                continue

            
            os.remove(file_path_download_to_tempdir)
            os.remove(os.path.join(tempdir, 'summary.xlsx'))
        print("Converted to common format")
        # return ({"nonParsedFilePaths":nonParsedFiles},200,headers)
        return ("converted",200,headers)
    except Exception as e:
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print("sys exception info :")
        # print(exc_type, fname, exc_tb.tb_lineno)
        print("Traceback")
        traceback.print_exc()
        print("printed Exception")
        print(str(e))
        print(e)
        return (str(e),201,headers)