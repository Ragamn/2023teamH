from textblob import TextBlob
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def emotion_analysis(text):
    blob = TextBlob(text)
    tags = blob.tags
    senti = blob.sentiment
    # pol = senti.polarity
    # Subjectivity = senti.subjectivity
    # senti_str = f"Polarity: {senti.polarity}, Subjectivity: {senti.subjectivity}"

    for tag in tags:
        print(f"{tag[0]} ({tag[1]})")

    return senti


print(emotion_analysis("I am so sadness"))
