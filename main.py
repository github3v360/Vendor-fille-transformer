# Importing Required Libraries
import pandas as pd
from src import extraction_of_entire_file
import logging
import io
import tempfile
import os
import time
from google.cloud import storage
import traceback

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
        'Access-Control-Allow-Headers': 'Content-Type, Access-Control-Allow-Origin, crossDomain',        
        'Access-Control-Allow-Origin': '*'
    }
    
    if request.method == 'OPTIONS':
        return ('', 204, headers)
    try:
        start = time.time()
        """Responds to any HTTP request.
        Args:
            request (flask.Request): HTTP request object.
        Returns:
            The response text or any set of values that can be turned into a
            Response object using
            `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
        """
        # Retrieve the parameters from the request

        
        userId = request.args.get('userId')
        date = request.args.get('date')
        # print("called with ",userId,date)

        directory_path = os.path.join(*[userId,date,"User_files"])
        # directory_path = os.path.join(*["ewTMxJQbjlQBX3QCcGtk9tjVukB3","20230625","User_files"])

        file_paths = list_files_in_directory(inventory_bucket_name, directory_path)

        FailedFiles = []

        log_buffer = io.StringIO()
        logging.basicConfig(level=logging.INFO, stream=log_buffer)

        print(f'all file_paths: {file_paths}')

        for file_path in file_paths:

            if ( (file_path.endswith('.csv') or file_path.endswith('.xlsx') or file_path.endswith('.xls')) == False ):
                continue
            


            file_path_splitted = file_path.split("/")

            print(f"splitted file path: {file_path_splitted}")


            cur_vendor_name = file_path_splitted[-2]
            cur_file_name = file_path_splitted[-1]

            print(f'cur_vendor name is : {cur_vendor_name}')
            print(f'cur_file name is:  {cur_file_name}')

            

            file_path_download_to_tempdir = os.path.join(*[tempdir,cur_file_name])
            print("file_path_download_to_tempdir : "+file_path_download_to_tempdir)
            
            downloadFromBucket(inventory_bucket_name, file_path, file_path_download_to_tempdir)
            print("downloaded from bucket")
            try:
                print(file_path_download_to_tempdir)
                extractor = extraction_of_entire_file.EntireFileExtractor(file_path_download_to_tempdir,False,logger,date,cur_vendor_name)
                print("Started Converting to common format")
                out_df = extractor.extract()
                print("File Converted")
            except:
                FailedFiles.append(cur_file_name)
                print('Failed Due to: ')
                print(f"Logic Failed for {cur_file_name} file")
                print("-" *50)
                print("Traceback for file  "+cur_file_name)
                traceback.print_exc()
                continue
            try:
                df_clean, df_missing = out_df
                print(df_clean,df_missing,df_clean.empty,df_missing.empty)
                if df_clean.empty and df_missing.empty:
                    continue
                print("Clean file generated"+str(len(df_clean)))
                df_clean = df_clean.reset_index()
                df_clean = df_clean.drop(columns=['index'])
                df_clean.to_excel(os.path.join(tempdir, 'summary.xlsx'), index = False)

                if file_path.endswith(".csv") or file_path.endswith(".xls"):
                    file_path_for_summary_bucket = file_path[:-4]+ "_output" + ".xlsx"
                elif file_path.endswith(".xlsx"):
                    file_path_for_summary_bucket = file_path[:-5] + "_output" + ".xlsx"

                #delete_file_from_bucket(summary_bucket_name,file_path_for_summary_bucket)
                print("deleted old files from bucket since we need to replace it with new file")
                uploadToBucket(summary_bucket_name, file_path_for_summary_bucket, os.path.join(tempdir, 'summary.xlsx'))
                print(f"uploaded to bucket with filepath as: {file_path_for_summary_bucket}")
                # os.remove(os.path.join(tempdir, 'summary.xlsx'))

                # if not df_missing.empty:
                    # print("Missing file generated"+str(len(df_missing)))
                    # df_missing = df_missing.reset_index()
                    # df_missing = df_missing.drop(columns=['index'])
                    # df_missing.to_excel(os.path.join(tempdir, 'summary1.xlsx'), index = False)

                    # if file_path.endswith(".csv") or file_path.endswith(".xls"):
                    #     file_path_for_summary_bucket = file_path[:-4]+ "_nonparsed" + ".xlsx"
                    # elif file_path.endswith(".xlsx"):
                    #     file_path_for_summary_bucket = file_path[:-5] + "_nonparsed" + ".xlsx"
                    # #delete_file_from_bucket(summary_bucket_name,file_path_for_summary_bucket)
                    # #print("deleted old files from bucket since we need to replace it with new file")


                    # nonParsedFiles.append(file_path_for_summary_bucket)
                    # uploadToBucket(summary_bucket_name, file_path_for_summary_bucket, os.path.join(tempdir, 'summary1.xlsx'))
                    # print(f"uploaded to bucket with filepath as: {file_path_for_summary_bucket}")
                    # os.remove(os.path.join(tempdir1, 'summary1.xlsx'))
                
                    
            except Exception as e:
                FailedFiles.append(cur_file_name)
                print('Failed Due to: ')
                print(f"Logic Failed for {cur_file_name} file")
                print("-" *50)
                print("Traceback for file  "+cur_file_name)
                traceback.print_exc()
                continue

            os.remove(file_path_download_to_tempdir)
            print("Converted to common format")
        end = time.time()
        # print("Total time taken in converting all "+ len(file_paths) +" files : " +str({end - start}))
        # return ({"nonParsedFilePaths" : nonParsedFiles},200,headers)
        if len(FailedFiles)>0:
            return ({"failedfiles" : FailedFiles},210,headers)
        else:
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