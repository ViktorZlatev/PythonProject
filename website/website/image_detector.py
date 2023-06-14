from nudenet import NudeClassifier


THRESHOLD = 0.65

classifier = NudeClassifier()

def classify_nudity_image(file_path):
    yhat = classifier.classify(file_path)
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


# This is the result of classify_nudity_image {'C:\\Users\\sas\\Pictures\\test_image.jpg': {'safe': 0.2413514405488968, 'unsafe': 0.7586485743522644}}

# This is the result of classify_nudity_video {'metadata': {'fps': 60.0, 'video_length': 6041, 'video_path': 'C:\\Users\\sas\\Videos\\SusCam video\\SusCam video ready.mp4'}, 'preds': {1: {'unsafe': 0.07879355, 'safe': 0.9212064}, 31: {'unsafe': 0.004511086, 'safe': 0.99548894}

