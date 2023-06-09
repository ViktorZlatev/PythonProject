from tensorflow.keras.layers import TextVectorization
import tensorflow as tf
import pandas as pd
import numpy as np

TOXICITY_FLAG = 0.80

# Loading tensorflow model and preprocessing data
model = tf.keras.models.load_model('../model_comment_toxicity_2.h5', compile=False)

# Loading data for vectorization
df = pd.read_csv('../comment_toxicity_train.csv')
X = df['comment_text']
y = df[df.columns[2:]].values
MAX_FEATURES = 200000
vectorizer = TextVectorization(max_tokens=MAX_FEATURES, output_sequence_length=1800, output_mode='int')
vectorizer.adapt(X.values)

# Tetx vectorization
def encode_text(text):
    encoded_input = vectorizer(text)
    encoded_input = np.expand_dims(encoded_input, 0) 
    return encoded_input

# Model prediction and return boolean
def classify_toxicity(text):
    res = model.predict(text)
    is_toxicity_arr = [type_toxicity for type_toxicity in res[0] if type_toxicity > TOXICITY_FLAG]
    is_toxicity = True if len(is_toxicity_arr) > 0 else False
    return is_toxicity



    # Model prediction   
    # input_str = vectorizer(new_chat)
    # res = model.predict(np.expand_dims(input_str, 0))
    # is_toxicity_arr = [type_toxicity for type_toxicity in res[0] if type_toxicity > TOXICITY_FLAG]
    # is_toxicity = True if len(is_toxicity_arr) > 0 else False
    # print(is_toxicity)
    # # If is_toxicity, then don't send this message
    # if is_toxicity == False:
    #     new_chat_message = Message.objects.create(body = new_chat , msg_sender = user , msg_reciver = profile , seen=False) 
    #     return JsonResponse(new_chat_message.body , safe=False)
    # else : return JsonResponse()