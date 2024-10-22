import torch
import re
import string
from transformers import BertTokenizer, BertForSequenceClassification
from dictionaries import *

model_dir = 'profanity_detection_model'
tokenizer = BertTokenizer.from_pretrained(model_dir)
model = BertForSequenceClassification.from_pretrained(model_dir)

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device)
model.eval()

def forbidden_words_search(test_texts, count) -> int:
    predictions = predict_profanity_forbidden(test_texts)
    for text, pred in zip(test_texts, predictions):
        if pred == 1:
            count += 1
    return count



def predict_profanity_forbidden(texts):
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt", max_length=128)
    inputs = {key: value.to(device) for key, value in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=1).cpu().numpy()
    return predictions


def count_extremism_words(text: str) -> int:
    try:
        with open("extremism_words_file.txt", 'r', encoding='utf-8') as file:
            forbidden_words = [line.strip().lower() for line in file if line.strip()]
        translator = str.maketrans('', '', string.punctuation)
        text_clean = text.translate(translator).lower()
        total_count = 0
        for word in forbidden_words:
            pattern = r'\b' + re.escape(word) + r'\b'
            matches = re.findall(pattern, text_clean)
            total_count += len(matches)
        return total_count
    except FileNotFoundError:
        return 0
    except Exception:
        return 0

def count_threat_words(text: str) -> int:
    try:
        with open("threat_words_file.txt", 'r', encoding='utf-8') as file:
            forbidden_words = [line.strip().lower() for line in file if line.strip()]
        translator = str.maketrans('', '', string.punctuation)
        text_clean = text.translate(translator).lower()
        total_count = 0
        for word in forbidden_words:
            pattern = r'\b' + re.escape(word) + r'\b'
            matches = re.findall(pattern, text_clean)
            total_count += len(matches)
        return total_count
    except FileNotFoundError:
        return 0
    except Exception:
        return 0