from info import info
from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
results = model.predict(
  source='https://ultralytics.com/images/bus.jpg',
  save=True,
  save_txt=True
)
