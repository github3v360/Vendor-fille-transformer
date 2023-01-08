from flask import *  
import pandas as pd
from src.utils.all_utils import *
app = Flask(__name__)  

@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        print(f.filename)  
        f.save(f.filename)  
        pd_read = pd.read_csv(str(f.filename))
        out_df = transform_df(pd_read)

        return render_template("success.html", name = str(out_df.head()))  

if __name__ == '__main__':  
    app.run(host= '0.0.0.0', debug = True,port=8000)  
