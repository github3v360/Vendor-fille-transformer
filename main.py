import pandas as pd
from src import Extraction_of_entire_file
import logging
import io

def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    file_ = request.files.get("file")

    log_buffer = io.StringIO()
    logging.basicConfig(level=logging.INFO, stream=log_buffer)

    out_df = Extraction_of_entire_file.extract_entire_file(file_,False,logging)

    out_df=out_df.reset_index()

    return out_df.to_json()