#-coding: utf-8-
import os
import re
from flask import Flask, request, render_template

UPLOAD_FOLDER_5 = u'/data/homeworkSubmit/clientFiles/experiment1/5班'.encode('utf-8')
UPLOAD_FOLDER_6 = u'/data/homeworkSubmit/clientFiles/experiment1/6班'.encode('utf-8')

app = Flask(__name__)
app.config['SECRET_KEY'] = '000000'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

def allowed_file(filename):
	name_left = filename.rsplit('.', 1)[0]
	INVALID_CHARS = ['.', '/', ' ', '-']
	for invalid_char in INVALID_CHARS:
		if invalid_char in name_left:
			return False
	p = re.compile(r'^\d{8}(\W){2,4}实验1([\(（]\d+[\)）])?\.(zip|ZIP)$'.decode('utf-8'))
	match = p.match(filename)
	if match:
		return True
	else:
		return False

def file_not_existed(filename, dir):
	li = os.listdir(dir)
	return filename not in li

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	feedback = u'请选择文件'
	filename = None
	if request.method == 'POST':
		file = request.files['file']
		if file:
			class_num = request.values.get('class-num')
			if class_num == None:
				feedback = u'请选择班级'
			else:
				if not allowed_file(file.filename):
					feedback = u'上传失败！请检查文件格式及命名'
				else:
					UPLOAD_FOLDER = UPLOAD_FOLDER_5 if class_num == u'5班' else UPLOAD_FOLDER_6
					if not file_not_existed(filename=file.filename.encode('utf-8'), dir=UPLOAD_FOLDER):
						feedback = u'上传失败！同名文件已存在！'
					else:
						file.save(os.path.join(UPLOAD_FOLDER, file.filename.encode('utf-8')))
						feedback = u'上传成功！'
						filename = class_num + '/' + file.filename
	return render_template('file_upload.html', feedback=feedback, filename=filename)

@app.errorhandler(413)
def request_entity_too_large(error):
	return render_template('file_upload.html', feedback=u'上传失败！文件大小超出限制', filename=None), 413

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)
