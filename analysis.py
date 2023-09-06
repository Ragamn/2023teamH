from textblob import TextBlob
import nltk
from google.cloud import translate_v2 as translate
if not nltk.data.find('tokenizers/punkt'):
    nltk.download('punkt')

# 'averaged_perceptron_tagger' リソースがインストールされているか確認
if not nltk.data.find('taggers/averaged_perceptron_tagger'):
    nltk.download('averaged_perceptron_tagger')

# 誰かのサービスアカウントキー
path = './rugged-alcove-398101-c4cdeb865efd.json'
# クライアントの初期化
translate_client = translate.Client.from_service_account_json(path)


def translate_text(text, target_language):
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']


def emotion_analysis(text):
    # 言語検出
    result = translate_client.detect_language(text)
    # 英語でなければ翻訳
    if result["language"] != 'en':
        translated_text = translate_text(text, "en")
        blob = TextBlob(translated_text)
        senti = blob.sentiment
        pol = senti.polarity
        Subjectivity = senti.subjectivity

        return pol, Subjectivity
    else:
        # Textblobオブジェクトに変換
        blob = TextBlob(text)
        # 感情分析
        senti = blob.sentiment
        # 極性。マイナスならネガティブ、プラスならポジティブ
        polarity = senti.polarity
        # 主観性。1に近い程主観的
        Subjectivity = senti.subjectivity
        # それぞれは数値として返ってくる
        return polarity, Subjectivity
