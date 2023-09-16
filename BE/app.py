from flask import Flask, request
from flask_cors import CORS
import re
from get_tweet import GetTweet

import pickle
import re
import pandas as pd
import numpy as np
from datasets import Dataset

from transformers import BertTokenizer,BertForSequenceClassification,TrainingArguments,Trainer



def is_url(string):
    pattern_ = r"https:\/\/twitter\.com\/\w+\/status\/\d+"
    if re.match(pattern_, string):
        return True
    else:
        return False


app = Flask(__name__)
CORS(app)

@app.route("/get")
def tweet_get():
    link = str(request.args.get('link')) 
    if is_url(link):
        tweet = get_tweet.get_text_form_tweet(link)
        return f'{tweet}'
    else:
        return '<NULL>'
    
@app.route("/predict")
def predict():
    
    tweet = str(request.args.get('tweet'))
    output_ds=preprocessing_data(tweet,tokenizer,max_word_length)
    outputs=trainer.predict(output_ds)
        
    if outputs.predictions.argmax(1)[0]==1:
        return 'YES'
    else:
        return 'NO'


    
def preprocessing_data(text, tokenizer, max_word_length):
    df=pd.DataFrame.from_dict({'text' : [text]})

    df['text']=df['text'].apply(lambda x: x.lower())
    df['text']=df['text'].apply(lambda x: x.replace("#", ""))
    df['text']=df['text'].apply(lambda x: re.sub(r'@\w+\s*', '', x))
    df['text']=df['text'].apply(lambda x: re.sub(r'http\S+|www\S+', '', x))
    df['text']=df['text'].apply(lambda x: re.sub(r'[^\w\s]', '', x))
    df['text']=df['text'].apply(lambda x: re.sub(r'\d+', '', x))
    df['text']=df['text'].apply(lambda x : re.compile(r'<.*?>').sub(r'', x))

    df['input_ids']=df['text'].apply(lambda x: tokenizer(x, max_length=max_word_length, padding='max_length')['input_ids'])
    df=df[['input_ids']]

    return Dataset.from_pandas(df)    


with open('bert_model.pkl', 'rb') as f:
    data = pickle.load(f)

tokenizer = data['tokenizer']
max_word_length = data['max_word_length']
model=data['model']
args=data['args']

trainer = Trainer(model=model,args=args)
    
if __name__ == "__main__":
    get_tweet = GetTweet("0326130017", r"project_ML_13072023")      
    app.run(debug=False)
