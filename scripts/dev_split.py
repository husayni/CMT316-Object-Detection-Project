import os
import xml.etree.ElementTree as ET

import numpy as np
from iterstrat.ml_stratifiers import MultilabelStratifiedShuffleSplit

VOC_ROOT = "/Users/hussain/Downloads/VOCdevkit/VOC2012"

# Input train list and where to write dev list
TRAIN_TXT = os.path.join(VOC_ROOT, 'ImageSets/Main/train.txt')
DEV_TXT   = os.path.join(VOC_ROOT, 'ImageSets/Main/dev.txt')

# Folder with annotation XMLs
ANN_DIR = os.path.join(VOC_ROOT, 'Annotations')

# VOC class list (20 classes)
CLASSES = [
    'aeroplane','bicycle','bird','boat','bottle',
    'bus','car','cat','chair','cow','diningtable',
    'dog','horse','motorbike','person','pottedplant',
    'sheep','sofa','train','tvmonitor'
]
# ------------------------------------

# 1) Read all train image IDs
with open(TRAIN_TXT, 'r') as f:
    image_ids = [line.strip() for line in f if line.strip()]

# Map class name → column index
class2idx = {c:i for i,c in enumerate(CLASSES)}

# 2) Build binary label matrix (N_images × 20)
N = len(image_ids)
Y = np.zeros((N, len(CLASSES)), dtype=int)

for i, img_id in enumerate(image_ids):
    xml_path = os.path.join(ANN_DIR, f'{img_id}.xml')
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for obj in root.findall('object'):
        cls = obj.find('name').text
        if cls in class2idx:
            Y[i, class2idx[cls]] = 1

# 3) Stratified split: 80% train / 20% dev
msss = MultilabelStratifiedShuffleSplit(
    n_splits=1,
    test_size=0.2,
    random_state=42
)
# .split returns generator of (train_idx, test_idx)
_, dev_idx = next(msss.split(image_ids, Y))

dev_ids = [image_ids[i] for i in dev_idx]

# 4) Write out dev.txt
with open(DEV_TXT, 'w') as f:
    for img_id in dev_ids:
        f.write(f"{img_id}\n")

print(f"Created {DEV_TXT} with {len(dev_ids)} images ({len(dev_ids)/N:.1%} of original train set).")