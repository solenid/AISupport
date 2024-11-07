import torch
import re
import string
import transformers
from transformers import pipeline

modelDir = 'profanity_detection_model'
tokenizer = transformers.BertTokenizer.from_pretrained(modelDir)
model = transformers.BertForSequenceClassification.from_pretrained(modelDir)

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device)
model.eval()


def forbiddenWordsSearch(testTexts, count) -> int:
    predictions = predictProfanityForbidden(testTexts)
    for text, pred in zip(testTexts, predictions):
        if pred == 1:
            count += 1
    return count


def predictProfanityForbidden(texts):
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt", max_length=128)
    inputs = {key: value.to(device) for key, value in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=1).cpu().numpy()
    return predictions


def countExtremismWords(text: str) -> int:
    try:
        with open("dictionaries/extremism_words_file.txt", 'r', encoding='utf-8') as file:
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


def countThreatWords(text: str) -> int:
    try:
        with open("dictionaries/threat_words_file.txt", 'r', encoding='utf-8') as file:
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
