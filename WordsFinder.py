import re
import string
import tensorflow as tf
import pickle

# Загрузка модели для матов
modelForBadie = tf.keras.models.load_model('AiModel/modelBadWords.keras')
# Загрузка модели для полезных слов
modelPR = tf.keras.models.load_model('AiModel/modelGreenFlagPRManager.keras')
# Загрузка токенизатора для матов
with open('AiModel/tokenizerForBadWords.pkl', 'rb') as handle:
    tokenzForBadie = pickle.load(handle)
# Загрузка токенизатора для полезных слов
with open('AiModel/tokenizer.pkl', 'rb') as handle:
    tokenizerForPr = pickle.load(handle)

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

#Используем модель для анализа текста (ПОИСК МАТОВ)
def predictBadWord(sentence):
    sequence = tokenzForBadie.texts_to_sequences([sentence])
    padSequence = tf.keras.preprocessing.sequence.pad_sequences(sequence, maxlen=4)
    prediction = modelForBadie.predict(padSequence)
    return prediction[0][0] > 0.95  # Если вероятность > 0.95, то содержит ключевое слово


#Используем модель для анализа текста (ПОИСК ПОЛЕЗНЫХ СЛОВ)
def predictPrSentence(sentence):
    sequence = tokenizerForPr.texts_to_sequences([sentence])
    padSequence = tf.keras.preprocessing.sequence.pad_sequences(sequence, maxlen=14)
    prediction = modelPR.predict(padSequence)
    return prediction[0][0] > 0.7  # Если вероятность > 0.7, то содержит ключевое слово

# Идет по тексту в постах, для удобства и точности каждый текст разбиваю каждые 5 пробелов,
# если кусок текста ему кажется подозрительным, то он идет по каждому слову в этом куске
# и если находит слово-триггер сразу записывает пост в релевантные
# + теперь смотрим пост на наличие матов, там жесткий отбор, так что нет надобности по каждому слову
def WordsSearch(postTexts, countGreen, countRed):
    redFlag = False
    greenFlag = False
    for text in postTexts:
        for textsPart in spliter(text, 5):
            if not redFlag:
                if (predictBadWord(textsPart)):
                    print(f"МАТ - {textsPart}") #ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!
                    redFlag = True
            if not greenFlag:
                if predictPrSentence(textsPart):
                    print(f"ПОДОЗРЕНИЕ на pr - {textsPart}") #ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!
                    for word in textsPart.split():
                        if predictPrSentence(word):
                            print(f"PR слово - {word}") #ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!
                            greenFlag = True
                            break
            if greenFlag and redFlag:
                break
        if redFlag:
            countRed += 1
            redFlag = False
        if greenFlag:
            countGreen += 1
            greenFlag = False
    return [countRed, countGreen]

# Подсчет экстремистских слов
def countExtremismWords(text: str) -> int:
    try:
        with open("Dictionaries/extremism_words_file.txt", 'r', encoding='utf-8') as file:
            forbiddenWords = [line.strip().lower() for line in file if line.strip()]
        translator = str.maketrans('', '', string.punctuation)
        textClean = text.translate(translator).lower()
        totalCount = 0
        for word in forbiddenWords:
            pattern = r'\b' + re.escape(word) + r'\b'
            matches = re.findall(pattern, textClean)
            totalCount += len(matches)
        return totalCount
    except FileNotFoundError:
        return 0
    except Exception:
        return 0

# Подсчет слов-угроз
def countThreatWords(text: str) -> int:
    try:
        with open("Dictionaries/threat_words_file.txt", 'r', encoding='utf-8') as file:
            forbiddenWords = [line.strip().lower() for line in file if line.strip()]
        translator = str.maketrans('', '', string.punctuation)
        textClean = text.translate(translator).lower()
        totalCount = 0
        for word in forbiddenWords:
            pattern = r'\b' + re.escape(word) + r'\b'
            matches = re.findall(pattern, textClean)
            totalCount += len(matches)
        return totalCount
    except FileNotFoundError:
        return 0
    except Exception:
        return 0
