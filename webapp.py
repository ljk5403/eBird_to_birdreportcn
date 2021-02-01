# /usr/bin/env python3

import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import transformer

UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

def allowed_file(filename):
    return '_observations.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            output_name = transformer.transformer(file.filename)
            return redirect('/eBird_to_birdreportcn'+url_for('uploaded_file',
                                    filename=output_name))
    return '''
    <!doctype html>
    <title>eBird to birdreportcn</title>
    <h1>eBird to birdreportcn</h1>
    <h2>将ebird的观察数据转换为中国观鸟记录中心可以接受的数据格式</h2>
    <p>步骤：</p>

    <ol>
    <li>从 <a href="https://ebird.org/mychecklists" target="_blank">eBird - 我的记录</a> 下载一个或多个checklist，得到若干名为 <code>xxyyzzww_observations.csv</code> 的文件。</li>
    <li>选中一个csv文件上传，注意不要改变文件名字！</li>
    <li>得到结果为 <code>xxyyzzww_importable.xls</code> 或 <code>xxyyzzww_importable_需要手动修复.xls</code>，后者需要手动修复一些没能转换的数据，结果将自动下载。</li>
    <li>到<a href="http://www.birdreport.cn/member/index.html" target="_blank">中国观鸟记录中心</a>上传记录。</li>
    </ol>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

'''
To remove uploaded files and generated files periodically, use cron:
30 * * * * rm -f *_observations.csv *_importable.xls *_importable_需要手动修复.xls
'''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

if __name__ =="__main__":
    #app.run('127.0.0.1', debug=True, port=8080)
    app.run('127.0.0.1', debug=False, port=8041)