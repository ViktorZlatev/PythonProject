from nudenet import NudeClassifier

image_path = r"C:\Users\sas\Pictures\test_image.jpg"

classifier = NudeClassifier()

def classify_nudity(image_path):
    print(classifier.classify(r'{image_path}'))
    return classifier.classify(image_path)
    
classify_nudity(image_path) 