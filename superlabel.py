import logging
import os
import time
import traceback
import json
import random
import string
import cv2
from flask import Flask, request, jsonify,render_template, Response, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS
from configparser import SafeConfigParser
from utilities import rcode
#from src import tuyen_ocr
app = Flask(__name__)
CORS(app)
api = Api(app)
#######################################
#####LOAD CONFIG####
config = SafeConfigParser()
config.read("config/superlabel.cfg")
LOG_PATH = str(config.get('main', 'LOG_PATH'))
SERVER_IP = str(config.get('main', 'SERVER_IP'))
SERVER_PORT = int(config.get('main', 'SERVER_PORT'))
UPLOAD_FOLDER = str(config.get('main', 'UPLOAD_FOLDER'))
UPLOAD_RESIZE_FOLDER = str(config.get('main', 'UPLOAD_RESIZE_FOLDER'))
RESULT_FOLDER = str(config.get('main', 'RESULT_FOLDER'))
#######################################
#####CREATE LOGGER#####
logging.basicConfig(filename=os.path.join(LOG_PATH, str(time.time())+".log"), filemode="w", level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
logging.getLogger("").addHandler(console)
logger = logging.getLogger(__name__)
#######################################
print("LOG_PATH", LOG_PATH)
print("SERVER_IP", SERVER_IP)
print("SERVER_PORT", SERVER_PORT)
print("UPLOAD_FOLDER", UPLOAD_FOLDER)
print("UPLOAD_RESIZE_FOLDER", UPLOAD_RESIZE_FOLDER)
print("RESULT_FOLDER", RESULT_FOLDER)
print("service ready")   
#######################################
class send_result(Resource):
    def post(self):
        ###################
        #####
        print("send_result")
        ###################
        try:
            start_time = time.time()
            result = None
            try:
                json_data = request.get_json(force=True)
                version = json_data['version']
                fname = json_data['fname']
                label = json_data['label']
                print("fname", fname)
            except Exception as e:
                print(str(e))
                print(str(traceback.print_exc()))
                return_result = {'code': '609', 'status': rcode.code_609}
                return;            
            ####################
            data = {'fname': fname, 'label': label}
            with open(os.path.join(RESULT_FOLDER, ''.join(fname.split('.')[:-1])+".json"), "w") as jf:
                json.dump(data, jf)
            ####################
            return_result = {'status': 'done', 'code': '1000'}
        except Exception as e:
            logger.error(str(e))
            logger.error(str(traceback.print_exc()))
            return_result = {'code': '1001', 'status': rcode.code_1001}
        finally:
            return jsonify(return_result)

class get_img_name(Resource):
    def get(self):
        #####
        print("get_img_name")
        ###################
        try:
            start_time = time.time()
            result = None
            try:
                version = request.args.get('version')
                mode = request.args.get('mode')
                index = int(request.args.get('index'))
                print(version, mode, index)
            except Exception as e:
                print(str(e))
                print(str(traceback.print_exc()))
                return_result = {'code': '609', 'status': rcode.code_609}
                return;            
            ####################
            file_list = os.listdir(UPLOAD_FOLDER)
            if mode == 'index':
                if index >= len(file_list):
                    fname = file_list[0]
                    index = -1
                else:
                    fname = file_list[index]
            else:
                fname = random.choice(file_list)
            return_result = {'code': '1000', 'status': rcode.code_1000, 'data':{'fname': fname, 'index': index}}
        except Exception as e:
            logger.error(str(e))
            logger.error(str(traceback.print_exc()))
            return_result = {'code': '1001', 'status': rcode.code_1001}
        finally:
            return jsonify(return_result)
            
class get_label(Resource):
    def get(self):
        #####
        print("get_label")
        ###################
        try:
            start_time = time.time()
            result = None
            try:
                version = request.args.get('version')
                fname = str(request.args.get('fname'))
                print(version, fname)
            except Exception as e:
                print(str(e))
                print(str(traceback.print_exc()))
                return_result = {'code': '609', 'status': rcode.code_609}
                return;            
            ####################
            if os.path.isfile(os.path.join(RESULT_FOLDER, ''.join(fname.split('.')[:-1])+".json")):
                with open(os.path.join(RESULT_FOLDER, ''.join(fname.split('.')[:-1])+".json"), "r") as jf:
                    jdata = json.loads(jf.read())
                label = jdata['label']
                return_result = {'code': '1000', 'status': rcode.code_1000, 'data':{'fname': fname, 'label': label}}
            else:
                return_result = {'code': '1201', 'status': rcode.code_1201}
        except Exception as e:
            logger.error(str(e))
            logger.error(str(traceback.print_exc()))
            return_result = {'code': '1001', 'status': rcode.code_1001}
        finally:
            return jsonify(return_result)
        
api.add_resource(get_img_name, '/get_img_name')
api.add_resource(send_result, '/send_result')
api.add_resource(get_label, '/get_label')
#######################################
@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/get_ori_img')
def get_ori_img():
    filename = request.args.get('filename')
    img = cv2.imread(os.path.join(UPLOAD_FOLDER, filename))
#    img = cv2.resize(img, (750, 250)) 
    ret, jpeg = cv2.imencode('.jpg', img)
    return  Response((b'--frame\r\n'
                     b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tostring() + b'\r\n\r\n'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#######################################
if __name__ == '__main__':
     app.run(host=SERVER_IP, port=SERVER_PORT, debug=True)
     
     
     





