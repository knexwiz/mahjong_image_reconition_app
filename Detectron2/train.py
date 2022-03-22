from Detectron2.utils import plot_samples
from detectron2.utils.logger import setup_logger

setup_logger()

from detectron2.data.datasets import register_coco_instances
from detectron2.engine import DefaultTrainer

import os
import pickle

from utils import *

CONFIG_FILE_PATH = "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"
CHECKPOINT_URL = "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"
OUTPUT_DIR = "./output/object_detection"

NUM_CLASSES = 1
DEVICE = "cpu"

TRAIN_DATASET_NAME = "LP_train"
TRAIN_IMAGES_PATH = "./train"
TRAIN_JSON_PATH = "train.json"

TEST_DATASET_NAME = "LP_test"
TEST_IMAGES_PATH = "./test"
TRAIN_JSON_PATH = "test.json"

CFG_SAVE_PATH = "OD_cfg.pickle"

#################################################################
register_coco_instances(name= TRAIN_DATASET_NAME, metadata={}, \
	json_file=TRAIN_JSON_PATH, image_root=TRAIN_IMAGES_PATH)

register_coco_instances(name= TEST_DATASET_NAME, metadata={}, \
	json_file=TEST_JSON_PATH, image_root=TEST_IMAGES_PATH)

# plot_samples(dataset_name=TRAIN_DATASET_NAME, n=2)

def main():
	cfg = get_train_cfg(CONFIG_FILE_PATH, CHECKPOINT_URL, TRAIN_DATASET_NAME, TEST_DATASET_NAME, \
		NUM_CLASSES, DEVICE, OUTPUT_DIR)
	
	with open(CFG_SAVE_PATH, 'wb') as f:
		pickle.dump(cfg, f, protocol=pickle.HIGHEST_PROTOCOL)

	os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)

	trainer = DefaultTrainer(cfg)
	trainer.resume_or_load(resume=False)

	trainer.train()


if __name__ == "__main__":
	main()