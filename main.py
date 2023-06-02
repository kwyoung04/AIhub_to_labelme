import matplotlib.pyplot as plt
from glob import glob
import os, json
import sys
import numpy as np
import os.path as osp
from glob import glob
from PIL import Image

def check_img(jsonfile):
    pass


def aihub_to_labelme(save_dir, jsonfile):
    imgname = jsonfile.replace('_BBOX.json', '.png')
    imgname = imgname.replace('Annotations', 'Images')
    
    img = plt.imread(imgname)
    imgname = os.path.basename(imgname) if os.path.isfile(imgname) else os.path.basename(imgname.replace('.jpg', '.png'))
    
    img_h, img_w = img.shape[:2]
    with open(jsonfile) as f :
        try :
            data = json.load(f)
        except :
            print(jsonfile)
            return []
        
    annotation_info = data['annotations']
    
    bbox_info = []
    
    for annot in annotation_info :
        
        label = annot['category_id']
        x, y, w, h = annot['bbox']
        bbox = [[x, y],
                [x+w, y+h]]
        bbox_info.append({'label': str(label),
                          'points': bbox,
                          'group_id': None,
                          "description": "",
                          'shape_type':'rectangle',
                          'flags': {}})
        
    #fname = os.path.join(save_dir, os.path.basename(jsonfile))
    
    with open(save_dir, 'w', encoding='utf-8') as outfile:
        data = {'version': '5.2.1', 'flags': {}, 'shapes': bbox_info, 'imagePath': imgname, 'imageData': None, 'imageHeight': img_h, 'imageWidth': img_w}
        json.dump(data, outfile, ensure_ascii=False, indent = 4)
        
if __name__ == '__main__':
    #json_file = sys.argv[1]
    json_file = "./data/Validation/Annotations/TOA/5.Mainroad_F02/V2F_HY_2262_20201224_101430_N_CH1_Seoul_Sun_Mainroad_Day_80792_BBOX.json"

    if json_file:
        new_path = "./data/labelme/" + json_file.split('/')[-1]
        new_path = new_path.replace('_BBOX.json', '.json')
        
        aihub_to_labelme(new_path, json_file)
