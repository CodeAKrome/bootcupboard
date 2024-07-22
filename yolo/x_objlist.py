from ultralytics import YOLO
from collections import defaultdict

model = YOLO("yolov8n.pt")
names = model.names  # Get the class names

def image_to_objects(image_path):
    results = model(image_path)  # results list
    objects = defaultdict(int)
    for r in results:
        for c in r.boxes.cls:
            objects[names[int(c)]] += 1
    return objects

res = image_to_objects("bus.jpg")
objects = []
for r in res:
    objects.append(f"{r}: {res[r]}")
print(", ".join(objects))