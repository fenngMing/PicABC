from flask import Flask, jsonify, Response, request, current_app
import os
import base64
import random
import logging
from datetime import datetime

IMG_DIR = "/path/to/your/image/dir"
TOKEN = "YourToken"
logging.basicConfig(filename="./log/run.log",filemode="a",format="%(asctime)s-%(name)s-%(levelname)s-%(message)s",level=logging.INFO)

app = Flask(__name__)

@app.before_request
def before_request():
    logging.info("IP:%s Url:%s" %(request.remote_addr, request.url))

@app.route('/get/<img_name>', methods=['GET'])
def download(img_name):
    img_path = "%s/%s" %(IMG_DIR, img_name)
    if not os.path.isfile(img_path):
        return jsonify({"ret":-1, "msg":"invalid file name:%s" %(img_name)})

    mdict = {
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif'
    }
    img_type = (img_name.split('/')[-1]).split('.')[-1]
    if img_type not in mdict.keys():
        return jsonify({"ret":-1, "msg":"invalid file type:%s" %(img_name)})
    mime = mdict[img_type]
    with open(img_path, 'rb') as f:
        image = f.read()
    return Response(image, mimetype=mime)


@app.route('/upload/', methods=['POST'])
def upload():
    token = request.form.get("token")
    if token != TOKEN:
        rsp = {"ret":-1, "msg":"auth failed"}
        logging.info(str(rsp))
        return jsonify(rsp)

    FIELD_NAME = "img_data"
    fp = request.files.get(FIELD_NAME)
    if not fp:
        rsp = {"ret":-1, "msg":"upload failed"}
        logging.info(str(rsp))
        return jsonify(rsp)

    stream = fp.stream.read()
    suffix = fp.filename.split('.')[-1]
    rename = "%s_%s.%s" %(datetime.now().strftime('%Y%m%d%H%M%S'),str(random.randrange(0,1000)), suffix)
    new_path = "%s/%s" %(IMG_DIR, rename)
    logging.info("Upload %s to %s" %(fp.filename, new_path))
    with open(new_path, 'wb') as f:
        f.write(stream)
    rsp = {"ret":0, "url":"http://mypic.fenngming.xyz/get/%s" %(rename)}
    logging.info(str(rsp))
    return jsonify(rsp)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7777)
