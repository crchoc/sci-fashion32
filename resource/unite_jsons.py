from parameters import IMG_DIR, ALL_DATA_FILE # project parameters
from all_functions import * # frequently used functions in the project
import os

# get list of all sets in dataset folder
all_outfits = list(os.listdir(IMG_DIR))
if '.DS_Store' in all_outfits:
    all_outfits.remove('.DS_Store')

# get json from all sets and unite into one
data = dict()
for fold in all_outfits:
    outfit_json = open_json(IMG_DIR + '/' 
                            + fold + '/'
                            + fold + '.json')
    data[fold] = outfit_json
write_json(ALL_DATA_FILE, data) # save into one json