# /usr/bin/env python3

import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import transformer

UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024


def allowed_file(filename):
    return '_observations.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    downloadLink = {}
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        for file in request.files.getlist('file'):
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                output_name = transformer.transformer(file.filename)
                # 此处为本地测试用
                downloadLink[filename] = (output_name,
                                          url_for('uploaded_file', filename=output_name))
                # 注：此处'/eBird_to_birdreportcn'是为了适配服务器端
                #downloadLink[filename] = (output_name,
                #                         '/eBird_to_birdreportcn'+url_for('uploaded_file', filename=output_name))
                #return redirect('/eBird_to_birdreportcn'+url_for('uploaded_file',
                #                        filename=output_name))
    return render_template('eBird to birdreportcn.html', **{"downloadLink": downloadLink})
    #return render_template('eBird to birdreportcn.html')


'''
To remove uploaded files and generated files periodically, use cron:
30 * * * * rm -f *_observations.csv *_importable.xls *_importable_需要手动修复.xls
or use
30 * * * * cd /var/www/eBird_to_birdreportcn; mv *_observations.csv *_importable.xls *_importable_需要手动修复.xls keg/
'''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    #app.run('127.0.0.1', debug=True, port=8080)
    app.run('127.0.0.1', debug=False, port=8041)
