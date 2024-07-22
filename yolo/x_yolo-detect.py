from ultralytics import YOLO
from icecream import ic

# Load a model
model = YOLO("yolov8n.pt")  # load an official model
#model = YOLO("path/to/best.pt")  # load a custom model

# Predict with the model
results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
#print(type(results))
#dir(results)
#for res in results:
#    print(res)
#res = results[0]
res = results[0]
probs = res.probs
print(type(probs))
ic(probs)

# objects = res.tojson()
# print(type(objects))

# for o in objects:
#     ic(o)
    
