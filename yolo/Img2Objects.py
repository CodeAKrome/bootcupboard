import sys
from ultralytics import YOLO
from collections import defaultdict
""" Read image paths from stdin and print 2 columns: image path, comma separated list of objects found in image. """

model = YOLO("yolov8n.pt")
names = model.names

def image_to_objects(image_path):
    results = model(image_path)
    objects = defaultdict(int)
    for r in results:
        for c in r.boxes.cls:
            objects[names[int(c)]] += 1
    return objects

for line in sys.stdin:
    image_path = line.strip()
    objects = image_to_objects(image_path)
    print(f"{image_path}\t{','.join([f'{k}:{v}' for k, v in objects.items()])}")
