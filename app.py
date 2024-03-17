import streamlit as st
import string
import pickle
import re
import time
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from pymongo import MongoClient


model_path = "model/model.pkl"
with open(model_path, 'rb') as f:
    model, vectorizer = pickle.load(f)

stop_words = set(stopwords.words('english'))  
wn = WordNetLemmatizer()  
punc = list(string.punctuation) 

def validate_text(token):
    return  token not in stop_words and token not in punc  and len(token)>2

def clean_text(text):
    text = text.lower()
    clean_text = []
    text = re.sub("'","",text)
    text = re.sub(r"(\d|\W)+", " ", text)
    for word in word_tokenize(text):
        if validate_text(word):
            lematized_word = wn.lemmatize(word,pos = "v")
            clean_text.append(lematized_word)
    return " ".join(clean_text)

def predict_news(text):
    cleaned_text = clean_text(text)
    input_vect = vectorizer.transform([cleaned_text])
    prediction = model.predict(input_vect)
    return prediction[0]

# Streamlit app
def main():
    st.title("News Category Prediction")
    input_text = st.text_area("Enter Short News Content:")
    
    if st.button("Predict"):
        prediction = predict_news(input_text)
        st.write("Predicted category: " + prediction)
        data = {
            "news_content": input_text,
            "predicted_category": prediction
        }
        try:
            # Attempt to connect to MongoDB
            client = MongoClient("mongodb://mongoadmin:secret@mongodb:27017/")
            # Check if the connection is successful
            if client.server_info():
                # Access the database and collection
                db = client["news_database"]
                collection = db["news_collection"]
                collection.insert_one(data)
                time.sleep(1)
                st.write("This data is inserted in MongoDB!")
        except Exception as e:
            st.write(f"Cannot Connect to MongoDB: {e}")

if __name__ == "__main__":
    main()

    

