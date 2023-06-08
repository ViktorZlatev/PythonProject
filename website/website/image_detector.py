from nudenet import NudeClassifier
from pathlib import Path
import os



# image_path = os.path.abspath(r"website\static\img\up_img\test_image.jpg")
# print(image_path)
# img_pth = Path(os.path.abspath(r"\PythonProject\website\static\img\23\test_image.jpg"))


# video_path = r"C:\Users\sas\Videos\SusCam video\iphone_email.mp4"

THRESHOLD = 0.65

classifier = NudeClassifier()

def classify_nudity_image(image_path):
    yhat = classifier.classify(image_path)
    unsafe_value = list(yhat.values())[0]['unsafe']
    if unsafe_value > THRESHOLD:
        return True
    return False

def classify_nudity_video(video_path):
    yhat = classifier.classify_video(video_path)
    preds = list(list(yhat.values())[1].values())
    max_value = 0
    for pred in preds:
        if pred['unsafe'] > max_value:
            max_value = pred['unsafe']
            
    if max_value > THRESHOLD:
        return True
    return False


# print(classify_nudity_image(image_path))
# print(classify_nudity_image(image_path))
# print(classify_nudity_video(video_path))


# This is the result of classify_nudity_image {'C:\\Users\\sas\\Pictures\\test_image.jpg': {'safe': 0.2413514405488968, 'unsafe': 0.7586485743522644}}

# This is the result of classify_nudity_video {'metadata': {'fps': 60.0, 'video_length': 6041, 'video_path': 'C:\\Users\\sas\\Videos\\SusCam video\\SusCam video ready.mp4'}, 'preds': {1: {'unsafe': 0.07879355, 'safe': 0.9212064}, 31: {'unsafe': 0.004511086, 'safe': 0.99548894}

