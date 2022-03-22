from detectron2.engine import DefaultPredictor
import os
import pickle
from utils import *

CFG_SAVE_PATH = "OD_cfg.pickle"
IMAGE_PATH = "test/....." #TODO

def main():
    with open(CFG_SAVE_PATH, 'wb') as f:
        cfg = pickle.load(f)

    cfg.MODEL_WEIGTHS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")
    cfg.MODEL_ROI_HEADS.SCORE_THRESH_TEST = 0.5
    predictor = DefaultPredictor(cfg)

    on_image(image_path, predictor)


if __name__ == "__main__":
	main()