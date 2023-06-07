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

def aihub_to_labelme(save_dir, jsonfile, check_list):
    imgname = jsonfile.replace('_BBOX.json', '.png')
    imgname = imgname.replace('Annotations', 'Images')
    
    imgname = os.path.basename(imgname) if os.path.isfile(imgname) else os.path.basename(imgname.replace('.jpg', '.png'))
    
    #img = plt.imread(imgname)
    #img_h, img_w = img.shape[:2]
    img_h = 720
    img_w = 1280
    
    with open(jsonfile) as f :
        try :
            data = json.load(f)
        except :
            print("File not found: ", jsonfile)
            return []
        
    annotation_info = data['annotations']
    
    bbox_info = []
    
    for annot in annotation_info :
        
        label = annot['category_id']
        if label not in check_list :
            continue
            
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
    if not bbox_info:
        print("empty bbox")
        return        
    
    with open(save_dir, 'w', encoding='utf-8') as outfile:
        print("save bbox")
        data = {'version': '5.2.1', 'flags': {}, 'shapes': bbox_info, 'imagePath': imgname, 'imageData': None, 'imageHeight': img_h, 'imageWidth': img_w}
        json.dump(data, outfile, ensure_ascii=False, indent = 4)
        
if __name__ == '__main__':
    json_file = sys.argv[1]
    json_file = "/mnt/c/Users/Eric/Documents/src/AIhub_to_labelme/data/Validation/" + json_file
    
    #json_file = "data/V1F_HY_9344_20160212_020214_E_CH2_Seoul_Sun_Frontback_Day_41220_PLINE.json"
    #json_file = "./data/" + json_file
    #print("### json_file: ", json_file)
    check_list = {8, 9, 10}

    if json_file:
        new_path = "../labelme/" + json_file.split('/')[-1]
        new_path = new_path.replace('_BBOX.json', '.json')
        

        aihub_to_labelme(new_path, json_file, check_list)
