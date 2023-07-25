from all_functions import *
from parameters import *

train = open_json(TRAIN_DATA_FILE)
test = open_json(TEST_DATA_FILE)
val = open_json(VAL_DATA_FILE)

train_feats = open_feats(TRAIN_FEATS)
test_feats = open_feats(TEST_FEATS)
cal_feats = open_feats(VAL_FEATS)
images_labels = open_json(IMGS_LABEL)