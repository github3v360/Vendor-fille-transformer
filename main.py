# Importing Required Libraries
import pandas as pd
from src import extraction_of_entire_file
import logging
import io
import tempfile
import os
from google.cloud import storage

# Bucket Realted parameters and functions

tempdir = tempfile.gettempdir()
tempdir = tempfile.mkdtemp()

client = storage.Client(project="friendlychat-bb9ff")

def convert_to_common_format(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    file_ = request.files['file']
    file_name = file_.filename
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, file_name)
    file_.save(file_path)

    vendor_name = request.args.get('vendor_name')
    date = request.args.get('date')

    log_buffer = io.StringIO()
    logging.basicConfig(level=logging.INFO, stream=log_buffer)

    extractor = extraction_of_entire_file.EntireFileExtractor(file_path,False,logging,date,vendor_name)
    out_df = extractor.extract()
    out_df=out_df.reset_index()
    return out_df.to_json()