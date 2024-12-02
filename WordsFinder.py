import re
import string
import tensorflow as tf
import pickle

# Загрузка модели для матов
modelRed = tf.keras.models.load_model('AiModel/WordsFinderModels/modelBadWords.keras')
# Загрузка токенизатора для матов
with open('AiModel/WordsFinderModels/tokenizerForBadWords.pkl', 'rb') as handle:
    tokeniRed = pickle.load(handle)

modelGreen = ''
tokeniGreen = ''


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
    sequence = tokeniRed.texts_to_sequences([sentence])
    padSequence = tf.keras.preprocessing.sequence.pad_sequences(sequence, maxlen=4)
    prediction = modelRed.predict(padSequence)
    return prediction[0][0] > 0.95  # Если вероятность > 0.95, то содержит ключевое слово


#Используем модель для анализа текста (ПОИСК ПОЛЕЗНЫХ СЛОВ)
def predictGreenWordSentence(modelGreen,tokeniGreen,sentence):
    sequence = tokeniGreen.texts_to_sequences([sentence])
    padSequence = tf.keras.preprocessing.sequence.pad_sequences(sequence, maxlen=14)
    prediction = modelGreen.predict(padSequence)
    return prediction[0][0] > 0.7  # Если вероятность > 0.7, то содержит ключевое слово

# Идет по тексту в постах, для удобства и точности каждый текст разбиваю каждые 5 пробелов,
# если кусок текста ему кажется подозрительным, то он идет по каждому слову в этом куске
# и если находит слово-триггер сразу записывает пост в релевантные
# + теперь смотрим пост на наличие матов, там жесткий отбор, так что нет надобности по каждому слову
def WordsSearch(postTexts, countGreen, countRed, type):

    #--------------------------------------------------------------------
    if type == -1:
        # Загрузка модели для полезных слов
        modelGreen = tf.keras.models.load_model('AiModel/WordsFinderModels/modelGreenFlagPRManager.keras')
        # Загрузка токенизатора для полезных слов
        with open('AiModel/WordsFinderModels/tokenizerForPRManager.pkl', 'rb') as handle:
            tokeniGreen = pickle.load(handle)
    # --------------------------------------------------------------------
    elif type == 0:
        # Загрузка модели для полезных слов
        modelGreen = tf.keras.models.load_model('AiModel/WordsFinderModels/modelNature.keras')
        # Загрузка токенизатора для полезных слов
        with open('AiModel/WordsFinderModels/tokenizerForNature.pkl', 'rb') as handle:
            tokeniGreen = pickle.load(handle)
    elif type == 1:
        # Загрузка модели для полезных слов
        modelGreen = tf.keras.models.load_model('AiModel/WordsFinderModels/modelHuman.keras')
        # Загрузка токенизатора для полезных слов
        with open('AiModel/WordsFinderModels/tokenizerForHuman.pkl', 'rb') as handle:
            tokeniGreen = pickle.load(handle)
    elif type == 2:
        # Загрузка модели для полезных слов
        modelGreen = tf.keras.models.load_model('AiModel/WordsFinderModels/modelSymbol.keras')
        # Загрузка токенизатора для полезных слов
        with open('AiModel/WordsFinderModels/tokenizerForSymbol.pkl', 'rb') as handle:
            tokeniGreen = pickle.load(handle)
    elif type == 3:
        # Загрузка модели для полезных слов
        modelGreen = tf.keras.models.load_model('AiModel/WordsFinderModels/modelTech.keras')
        # Загрузка токенизатора для полезных слов
        with open('AiModel/WordsFinderModels/tokenizerForTech.pkl', 'rb') as handle:
            tokeniGreen = pickle.load(handle)
    elif type == 4:
        # Загрузка модели для полезных слов
        modelGreen = tf.keras.models.load_model('AiModel/WordsFinderModels/modelArt.keras')
        # Загрузка токенизатора для полезных слов
        with open('AiModel/WordsFinderModels/tokenizerForArt.pkl', 'rb') as handle:
            tokeniGreen = pickle.load(handle)
    else:
        print("!!! ОШИБКА ПОИСКА СЛОВ, НЕИЗВЕСТНЫЙ ТИП ЧЕЛОВЕКА")
        exit()

    redFlag = False
    greenFlag = False
    for text in postTexts:
        for textsPart in spliter(text, 5):
            if not redFlag:
                if (predictBadWord(textsPart)):
                    print(f"МАТ - {textsPart}") #ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!
                    redFlag = True
            if not greenFlag:
                if predictGreenWordSentence(modelGreen, tokeniGreen,textsPart):
                    print(f"ПОДОЗРЕНИЕ на GreenFlag - {textsPart}") #ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!
                    for word in textsPart.split():
                        if predictGreenWordSentence(modelGreen, tokeniGreen, word):
                            print(f"GreenFlag слово - {word}") #ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!#ОТЛАДКА!
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

def gerchikovKeyWords(str, subs: bool):
    result = 0
    if subs == True:
        with open('Dictionaries/gerchikovSubs.txt', 'r', encoding='utf-8') as f:
            keyWords = [line.strip() for line in f.readlines()]
        for word in str:
            if word in keyWords:
                result += 1
    else:
        with open('Dictionaries/gerchikovWall.txt', 'r', encoding='utf-8') as f:
            keyWords = [line.strip() for line in f.readlines()]
        for text in str:
            for word in text:
                if word in keyWords:
                    result += 1
    return result