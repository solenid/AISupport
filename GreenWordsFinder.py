import tensorflow as tf
import pickle

# Загрузка модели
loadedModel = tf.keras.models.load_model('AiModel/modelGreenFlagPRManager.keras')
with open('AiModel/tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

def predictSentence(sentence):
    sequence = tokenizer.texts_to_sequences([sentence])
    padSequence = tf.keras.preprocessing.sequence.pad_sequences(sequence, maxlen=10)
    prediction = loadedModel.predict(padSequence)
    return prediction[0][0] > 0.2  # Если вероятность > 0.5, то содержит ключевое слово

def greenWordInPosts(postTexts, count):
    greenFlag = False
    for text in postTexts:
        for word in text.split():
            if len(word) > 1:
                if predictSentence(word):
                    greenFlag = True
                    break
        if greenFlag:
            count += 1
            greenFlag = False
    return count