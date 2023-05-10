from info import info
import requests

with open('bus.jpg', 'rb') as binary_image:
    response = requests.post('http://192.168.178.160:8080/yolo', data=binary_image)

info(response.text)
info(response.status_code)
