TOXICITY_FLAG = 0.65

# Loading tensorflow model and preprocessing data
model = tf.keras.models.load_model('../model_comment_toxicity_2.h5', compile=False)

df = pd.read_csv('../comment_toxicity_train.csv')
X = df['comment_text']
y = df[df.columns[2:]].values
MAX_FEATURES = 200000
vectorizer = TextVectorization(max_tokens=MAX_FEATURES, output_sequence_length=1800, output_mode='int')
vectorizer.adapt(X.values)