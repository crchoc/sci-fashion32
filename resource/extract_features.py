from all_functions import * # frequently used functions
from parameters import * # parameters of the project
from tqdm import tqdm
from skimage.transform import resize
from skimage import img_as_ubyte
from skimage.color import gray2rgb, rgba2rgb
from PIL import Image
import skimage.io
import torch
import torch.nn as nn
from torchvision import models
import torchvision.transforms as transforms
import pickle as pkl
import numpy as np
import os

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = models.resnet50(pretrained=True)
model = nn.Sequential(*list(model.children())[:-1])
model = model.to(device)
model.eval()

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                    std=[0.229, 0.224, 0.225])

transform = transforms.Compose([
                transforms.ToPILImage(),
                transforms.Resize(256), transforms.CenterCrop(224),
                transforms.ToTensor(), normalize
            ])

def process_image(im):
    im = transform(im)
    im = im.unsqueeze_(0)
    im = im.to(device)
    out = model(im)
    return out.squeeze()

train = open_json(TRAIN_DATA_FILE)
test = open_json(TEST_DATA_FILE)
val = open_json(VAL_DATA_FILE)

loop = ['TRAIN', 'TEST', 'VAL']
ids  = dict()

for l in loop:
    data = open_json(l+'_DATA_FILE')
    for outfit in data:
        for item in data[outfit]['items']:
            id = item['sku_id']
            their_id = '{}_{}_{}'.format(outfit, item['cate3_id'], item['index'])
            ids[id] = their_id
    
    features = dict()
    count = dict() 
    i = 0
    n_items = len(ids.keys())
    with torch.no_grad():
        for id in tqdm(ids):
            outfit_id, cate3_id, index = ids[id].split('_')
            image = str(outfit_id) + '_' + str(cate3_id) + '_' + str(id) + '.jpg'
            image_path = IMG_DIR + '/' + outfit_id + '/' + image
            assert os.path.exists(image_path)

            im = skimage.io.imread(image_path)
            if len(im.shape) == 2:
                im = gray2rgb(im)
            if im.shape[2] == 4:
                im = rgba2rgb(im)
            
            im = resize(im, (256, 256))
            im = img_as_ubyte(im)

            feats = process_image(im).cpu().numpy()

            if id not in features:
                features[id] = feats
                count[id] = 0
            else:
                features[id] += feats
            count[id] += 1

            if i%1000 == 0 and i> 0:
                print('{}/{}'.format(i, n_items))
                i += 1
    feat_dict = {}
    for id in features:
        feats = features[id]
        feats = np.array(feats)/count[id]
        feat_dict[id] = feats    
    with open(l+'_FEATS', 'wb') as handle:
        pkl.dump(feat_dict, handle, protocol=pkl.HIGHEST_PROTOCOL)
print('DONE!')
