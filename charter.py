
# Dominic Taraska
# Take home for Nielsen software engineer role
# 04/14/21



from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, url_for, session, redirect
)
from werkzeug.exceptions import abort
import os
from werkzeug.utils import secure_filename
import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64
from io import BytesIO

bp = Blueprint('charter', __name__,url_prefix='/home')
UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'csv'}

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/', methods=('GET', 'POST'))
def home():
    print(os.getcwd())
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))

            # opens file and converts to list, go in and count total viewership for Pitt and Cleve, store totals in size 3 array (1 index for each genre)
            with open(filename, newline='', errors='replace') as f:
                csvreader = csv.reader(f)
                data = list(csvreader)
            totals = [0,0,0]
            for row in data:
                
                if row[3] == 'Pittsburgh' or row[3] == 'Cleveland':
                    
                    print(row[3])
                    if row[1] == 'Sports':
                        
                        totals[0] += int(row[4])
                        print(totals[0])
                        

                    elif row[1] == 'Science Fiction':
                        totals[1] += int(row[4])
                        print(totals[1])

                    elif row[1] == 'Mystery':
                        totals[2] += int(row[4])
                        print(totals[2])

            # creates bar chart figure using matplotlib and then displays it to user 
            plt.figure(1)
            genres = ['Sports', 'Science Fiction', 'Mystery']
            y_pos = np.arange(len(genres))
            plt.bar(y_pos, totals, align='center', alpha=0.5)
            plt.xticks(y_pos, genres)
            plt.ylabel('Viewers')
            plt.title('Viewership from Cleveland/Pittsburgh')
            buf = BytesIO()
            plt.savefig(buf, format="png")
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            return f"<img src='data:image/png;base64,{data}'/>"
              

    return render_template('charter/home.html')


