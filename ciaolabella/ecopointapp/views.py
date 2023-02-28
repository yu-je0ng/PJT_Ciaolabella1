import argparse
import json
import io
from PIL import Image
import torch
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

@app.route('/',methods=["GET", "POST"])
def predict():
    if request.method == 'POST':
        image = request.files['image']
        if not image:
            return jsonify({'result':'no image', 'msg': '선택한 이미지가 없습니다!'})

        img_bytes = image.read()
        img = Image.open(io.BytesIO(img_bytes))
        imgs = [img]
        model.conf = 0.5
        results = model(imgs)
        results.save(save_dir="/home/ubuntu/multi_pjt3/ciaolabella/static/ecopoint_static/img_output/ecopoint1/")
        result = json.loads(results.pandas().xyxy[0][['name', 'confidence']].to_json(orient='records'))
     
        return jsonify({'result': result})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=8001, type=int, help="port number")
    args = parser.parse_args()

    # yolo model 불러오기
    model = torch.hub.load('./yolov5' , 'custom', path='./yolov5/runs/train/rreal_final13/weights/best.pt', source='local')
    model.eval()
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat