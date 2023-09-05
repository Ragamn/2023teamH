from textblob import TextBlob
import nltk
from google.cloud import translate_v2 as translate
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# 俺のサービスアカウントキー
path = './rugged-alcove-398101-c4cdeb865efd.json'
# クライアントの初期化
translate_client = translate.Client.from_service_account_json(path)


def translate_text(text, target_language):
    result = translate_client.translate(text, target_language=target_language)
    return result['input'], result['translatedText']


def emotion_analysis(text):
    blob = TextBlob(text)
    result = translate_client.detect_language(text)
    if result["language"] == "ja":
        tags = blob.tags
        senti = blob.sentiment
        pol = senti.polarity
        Subjectivity = senti.subjectivity
        senti_str = f"Polarity: {senti.polarity}, Subjectivity: {senti.subjectivity}"

        for tag in tags:
            print(f"{tag[0]} ({tag[1]})")

        return senti
    return 0


print(emotion_analysis("こんにちは。お元気ですか。"))

# input_text = "Hello, how are you?"
# target_language = "ja"
# input_text, translated_text = translate_text(input_text, target_language)
# print(translated_text)
