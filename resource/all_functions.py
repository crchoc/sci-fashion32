import torch
import torch.nn as nn
from torchvision import models
import torchvision.transforms as transforms
import json

# open JSON file
def open_json(file_path):
    with open(file_path) as f:
        content = json.load(f)
    return content

# close JSON file
def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return print(file_path + ': file is SAVED')

# Put IDS to tags
def put_id_to_tags(data):
    data_list = list(set(data))
    data_list.sort()
    data_dict = dict()
    i = 0
    for d in data_list:
        data_dict[d] = i
        i += 1
    return data_dict

def resnet_model():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = models.resnet50(pretrained=True)
    model = nn.Sequential(*list(model.children())[:-1])
    model = model.to(device)
    return device, model

def process_image(image, transform, model, device):
    im = transform(im)
    im = im.unsqueeze_(0)
    im = im.to(device)
    out = model(im)
    return out.squeeze()