import tensorflow as tf
import pickle

# Загрузка модели
loadedModel = tf.keras.models.load_model('AiModel/modelGreenFlagPRManager.keras')
with open('AiModel/tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

#Делит строки по определенному количеству пробелов
def spliter(input_string, n):
    parts = []
    current_part = []
    space_count = 0
    for char in input_string:
        current_part.append(char)
        if char == ' ':
            space_count += 1
            if space_count == n: # Если достигли n пробелов, добавляем текущую часть в список
                parts.append(''.join(current_part).strip())
                current_part = []  # Сброс текущей части
                space_count = 0  # Сброс счетчика пробелов
    if current_part: # Добавляем оставшуюся часть, если она не пустая
        parts.append(''.join(current_part).strip())
    return parts

#Используем модель для анализа текста
def predictSentence(sentence):
    sequence = tokenizer.texts_to_sequences([sentence])
    padSequence = tf.keras.preprocessing.sequence.pad_sequences(sequence, maxlen=14)
    prediction = loadedModel.predict(padSequence)
    return prediction[0][0] > 0.6  # Если вероятность > 0.6, то содержит ключевое слово

# Идет по тексту в постах, для удобства и точности каждый текст разбиваю каждые 5 пробелов,
# если куско текста ему кажется подозрительным, то он идет по каждому слову в этом куске
# и если находит слово-триггер сразу записывает пост в ревелантные
def greenWordInPosts(postTexts, count):
    greenFlag = False
    for text in postTexts:
        for textsPart in spliter(text, 5):
            if predictSentence(textsPart):
                print(textsPart)
                for word in textsPart.split():
                    if predictSentence(word):
                        print(word)
                        greenFlag = True
                        break
                if greenFlag:
                    break
        if greenFlag:
            count += 1
            greenFlag = False
    return count