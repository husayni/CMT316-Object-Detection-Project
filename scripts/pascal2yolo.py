# Only Uses the validation split


VOC_ROOT    = '/kaggle/input/pascal-voc-2012/VOC2012'
IMG_DIR     = os.path.join(VOC_ROOT, 'JPEGImages')
ANN_DIR     = os.path.join(VOC_ROOT, 'Annotations')
VAL_LIST    = os.path.join(VOC_ROOT, 'ImageSets', 'Main', 'val.txt')
WORK_DIR    = '/kaggle/working/voc_yolo'
CONFIG_YAML = os.path.join(WORK_DIR, 'data.yaml')

# 2. Create output directories
for split in ['train', 'val']:
    os.makedirs(os.path.join(WORK_DIR, 'images', split), exist_ok=True)
    os.makedirs(os.path.join(WORK_DIR, 'labels', split), exist_ok=True)

# 3. Read and split val.txt (80% train / 20% val)
with open(VAL_LIST, 'r') as f:
    ids = [x.strip() for x in f if x.strip()]
random.seed(42)
random.shuffle(ids)
split_idx = int(0.8 * len(ids))
train_ids = ids[:split_idx]
val_ids   = ids[split_idx:]
print(f"Total {len(ids)} Images: {len(train_ids)} train, {len(val_ids)} val")

# 4. Scan XMLs for class names
tmp_classes = set()
for xml_file in os.listdir(ANN_DIR):
    if not xml_file.endswith('.xml'): continue
    tree = ET.parse(os.path.join(ANN_DIR, xml_file))
    root = tree.getroot()
    for obj in root.findall('object'):
        tmp_classes.add(obj.find('name').text)
classes = sorted(tmp_classes)
print(f"Found {len(classes)} classes: {classes}")
# map class→id
cls2id = {c:i for i,c in enumerate(classes)}
# write classes.txt
with open(os.path.join(WORK_DIR, 'classes.txt'), 'w') as cf:
    cf.write('\n'.join(classes))

# 5. Conversion helper
def convert_box(size, box):
    dw, dh = 1.0/size[0], 1.0/size[1]
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    return x*dw, y*dh, w*dw, h*dh

# 6. Process splits
for split, id_list in [('train', train_ids), ('val', val_ids)]:
    for img_id in tqdm(id_list, desc=f"Processing {split}"):
        # image symlink
        src_img = os.path.join(IMG_DIR, f"{img_id}.jpg")
        dst_img = os.path.join(WORK_DIR, 'images', split, f"{img_id}.jpg")
        if not os.path.exists(dst_img): os.symlink(src_img, dst_img)
        # parse XML
        xml_path = os.path.join(ANN_DIR, f"{img_id}.xml")
        tree = ET.parse(xml_path)
        root = tree.getroot()
        size = root.find('size')
        w, h = int(size.find('width').text), int(size.find('height').text)
        # write YOLO label
        lbl_path = os.path.join(WORK_DIR, 'labels', split, f"{img_id}.txt")
        with open(lbl_path, 'w') as out:
            for obj in root.findall('object'):
                diff = int(obj.find('difficult').text)
                cname = obj.find('name').text
                if diff == 1 or cname not in cls2id:
                    continue
                b = obj.find('bndbox')
                box = [float(b.find(x).text) for x in ('xmin','xmax','ymin','ymax')]
                bx = convert_box((w,h), box)
                cid = cls2id[cname]
                out.write(f"{cid} {bx[0]:.6f} {bx[1]:.6f} {bx[2]:.6f} {bx[3]:.6f}\n")

# 7. Write data.yaml with names as dict
names_dict = {i: c for i,c in enumerate(classes)}
data = {
    'path': WORK_DIR,
    'train': 'images/train',
    'val':   'images/val',
    'names': names_dict
}
with open(CONFIG_YAML, 'w') as df:
    yaml.dump(data, df)
