from parameters import * # parameters of the project
from all_functions import * # frequently used functions in the project
from tqdm import tqdm # scroll bar

# GET INFO AND GIVE IT AN ID
data_dict = open_json(ALL_DATA_FILE) # get all info
labels_type = list() # labels
image_to_label = dict() # labels/output to image
pattern_type = list() # pattern
material_type = list() # material
sleeve_type = list() # sleeve type
cat_type = list() # category
fit = list() # fit
gender = list() # gender
occasion = list() # occasion
style = list() # style

# go through all data
for data in tqdm(data_dict):
    print(data, '-------->')
    items = data_dict[data]['Items'] # data - outfit, items - items in an outfit
    for item in items:
        tags = item['Tags']
        image_to_label[item['Image']] = []
        if '98' in tags.keys(): # women's clothes
            label_list = []
            for t in tags['98']:
                label_list.append(t['label_name'])
            labels_type.extend(label_list)
            if len(image_to_label[item['Image']])==0:
                image_to_label[item['Image']] = label_list
        if '99' in tags.keys(): # men's clothes
            label_list = []
            for t in tags['99']:
                label_list.append(t['label_name'])
            labels_type.extend(label_list)
            if len(image_to_label[item['Image']])==0:
                image_to_label[item['Image']] = label_list
        if '93' in tags.keys(): # pattern type
            patt_list = []
            for t in tags['93']:
                patt_list.append(t['label_name'])
            pattern_type.extend(patt_list)
        if '94' in tags.keys(): # material
            mat_list = []
            for t in tags['94']:
                mat_list.append(t['label_name'])
            material_type.extend(mat_list)
        if '95' in tags.keys(): # sleeve type
            sleeve_list = []
            for t in tags['95']:
                sleeve_list.append(t['label_name'])
            sleeve_type.extend(sleeve_list)
        if '97' in tags.keys(): # category
            cat_list = []
            for t in tags['97']:
                cat_list.append(t['label_name'])
            cat_type.extend(cat_list)
    fit.append(data_dict[data]['Outfit_Fit']) # fit
    gender.append(data_dict[data]['Outfit_Gender']) # gender
    occasion.append(data_dict[data]['Outfit_Occasion']) # occasion
    style.append(data_dict[data]['Outfit_Style']) # style

# put IDs
labels_dict = put_id_to_tags(labels_type)
pattern_dict = put_id_to_tags(pattern_type)
material_dict = put_id_to_tags(material_type)
sleeve_dict = put_id_to_tags(sleeve_type)
category_dict = put_id_to_tags(cat_type)
fit_dict = put_id_to_tags(fit)
gender_dict = put_id_to_tags(gender)
occasion_dict = put_id_to_tags(occasion)
style_dict = put_id_to_tags(style)

# save images and their labels (outputs)
for image in image_to_label:
    image_to_label[image] = labels_dict[image_to_label[image][0]]

# save files
write_json(LABELS_FILE, labels_dict)
write_json(IMGS_LABEL, image_to_label)
write_json(PATTERNS_FILE, pattern_dict)
write_json(MATERIAL_FILE, material_dict)
write_json(SLEEVE_TYPE_FILE, sleeve_dict)
write_json(CATEGORY_FILE, category_dict)
write_json(FIT_FILE, fit_dict)
write_json(GENDER_FILE, gender_dict)
write_json(OCCASION_FILE, occasion_dict)
write_json(STYLE_FILE, style_dict)

print('Number of labels: ', len(labels_dict), 
      '\nNumber of patterns: ', len(pattern_dict), 
      '\nNumber of materials: ', len(material_dict), 
      '\nNumber of sleeve types: ', len(sleeve_dict), 
      '\nNumber of images: ', len(image_to_label))
print('Labels ready, DONE!')
