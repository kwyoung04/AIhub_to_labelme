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
    imgname = imgname.replace('annotation', 'images')
    #imgname = os.path.basename(imgname) if os.path.isfile(imgname) else os.path.basename(imgname.replace('.jpg', '.png'))
    
    img = plt.imread(imgname)
    img_h, img_w = img.shape[:2]
    
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
        
    if not bbox_info:
        print("empty bbox")
        return []
    
    with open(save_dir, 'w', encoding='utf-8') as outfile:
        print("save bbox")
        data = {'version': '5.2.1', 'flags': {}, 'shapes': bbox_info, 'imagePath': imgname, 'imageData': None, 'imageHeight': img_h, 'imageWidth': img_w}
        json.dump(data, outfile, ensure_ascii=False, indent = 4)
   
def get_json_files(input_dir):
    json_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files
        
if __name__ == '__main__':
    print(sys.argv)
    json_files = get_json_files(sys.argv[1])
    labelme_path = sys.argv[2]

    check_list = {8, 9, 10}
    
    for json_file in json_files:
        print("# json_file: ", json_file)
        if json_file:
            new_path = labelme_path + json_file.split('/')[-1]
            new_path = new_path.replace('_BBOX.json', '.json')
            

            aihub_to_labelme(new_path, json_file, check_list)
