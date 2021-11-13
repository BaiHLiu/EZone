import argparse
import os
import sys
import json
import cv2
import numpy as np
import torch
from yolox.data.data_augment import ValTransform
from yolox.data.datasets import COCO_CLASSES
from yolox.exp import get_exp
from yolox.utils import postprocess, vis
from flask import Flask, jsonify, request

IMAGE_EXT = [".jpg", ".jpeg", ".webp", ".bmp", ".png"]


def make_parser():
    parser = argparse.ArgumentParser("YOLOX Demo!")
    parser.add_argument("--path", default='assets/', help="path to images or dir")
    parser.add_argument("-f", "--exp_file", default=r'exps/default/yolox_s.py', type=str,
                        help="input your experiment description file")
    parser.add_argument("-n", "--name", type=str, default='yolox-s', help="model name")
    parser.add_argument("-c", "--ckpt", default='weights/best_ckpt.pth', type=str, help="ckpt for eval")
    parser.add_argument("--device", default="cpu", type=str, help="device to run our model, can either be cpu or gpu")
    parser.add_argument("--nms", default=0.45, type=float, help="test nms threshold")
    return parser


def get_image_list(path):
    image_names = []
    for maindir, subdir, file_name_list in os.walk(path):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            ext = os.path.splitext(apath)[1]
            if ext in IMAGE_EXT:
                image_names.append(apath)
    return image_names


class Predictor(object):
    def __init__(self, model, exp, cls_names=COCO_CLASSES, device="cpu"):
        self.model = model
        self.cls_names = cls_names
        self.num_classes = exp.num_classes
        self.confthre = exp.test_conf
        self.nmsthre = exp.nmsthre
        self.test_size = exp.test_size
        self.device = device
        self.preproc = ValTransform(legacy=False)

    def inference(self, imgs):
        img_info = {"id": 0}
        img_info["file_name"] = os.path.basename(imgs)
        img = cv2.imread(imgs)
        if img is None:
            img = cv2.imdecode(np.fromfile(imgs, dtype=np.uint8), -1)
            img = img[:,:,0:3]
        '''
        height, width = img.shape[:2]
        img_info["height"] = height
        img_info["width"] = width
        img_info["raw_img"] = img
        ratio = min(self.test_size[0] / img.shape[0], self.test_size[1] / img.shape[1])
        img_info["ratio"] = ratio
        '''
        img, _ = self.preproc(img, None, self.test_size)
        img = torch.from_numpy(img).unsqueeze(0)
        img = img.float()
        if self.device == "gpu":
            img = img.cuda()
        with torch.no_grad():
            outputs = self.model(img)
            outputs = postprocess(
                outputs, self.num_classes, self.confthre,
                self.nmsthre, class_agnostic=True
            )
        return outputs, img_info

    def visual(self, output, img_info, cls_conf=0.35):
        ratio = img_info["ratio"]
        img = img_info["raw_img"]
        if output is None:
            return img
        output = output.cpu()

        bboxes = output[:, 0:4]

        # preprocessing: resize
        bboxes /= ratio
        cls = output[:, 6]
        scores = output[:, 4] * output[:, 5]

        vis_res = vis(img, bboxes, scores, cls, cls_conf, self.cls_names)
        return vis_res


def image_demo(predictor, path):
    if os.path.isdir(path):
        files = get_image_list(path)
    else:
        files = [path]
    files.sort()
    list = {}
    for image_name in files:
        outputs, img_info = predictor.inference(image_name)
        if outputs[0] is not None:
            box_nums = outputs[0].shape[0]
        else:
            box_nums = 0
        '''
        result_image = predictor.visual(outputs[0], img_info, predictor.confthre)
        cv2.imshow('test', result_image)
        ch = cv2.waitKey(0)
        if ch == 27 or ch == ord("q") or ch == ord("Q"):
            break
        '''
        list[image_name] = box_nums
    return list


app = Flask(__name__)


@app.route('/main', methods=['POST', 'GET'])
def main():
    args = make_parser().parse_args()
    exp = get_exp(args.exp_file, 'yolox-s')
    json_ = str(request.values.get('dir'))

    args.path = json_
    exp.test_conf = 0.25
    if args.nms is not None:
        exp.nmsthre = args.nms
    exp.test_size = (640, 640)  # img_size
    model = exp.get_model()
    if args.device == "gpu":
        model.cuda()
    model.eval()
    ckpt_file = args.ckpt
    ckpt = torch.load(ckpt_file, map_location="cpu")
    model.load_state_dict(ckpt["model"])
    predictor = Predictor(model, exp, COCO_CLASSES, args.device)
    list = image_demo(predictor, args.path)
    return json.dumps(list, ensure_ascii=False)


if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except:
        port = 12345

    # main(exp, args)
    app.run(port=port, debug=True)
