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
  """
  Checks if a string is a URL.

  Args:
    string: The string to check.

  Returns:
    True if the string is a URL, False otherwise.
  """

  regex = r"^(http|https):\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(\/\S*)?$"
  match = re.match(regex, string)
  return bool(match)


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
    if is_url(tweet):
        tweet = get_tweet.get_text_form_tweet(tweet)
        
        output_ds=preprocessing_data(tweet,tokenizer,max_word_length)
        trainer = Trainer(
                    model=model,
                    args=args, 
        )
        outputs=trainer.predict(output_ds)
        
        if outputs.predictions.argmax(1)[0]==1:
            return 'YES'
        else:
            return 'NO'
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


    
if __name__ == "__main__":
    get_tweet = GetTweet("0326130017", r"project_ML_13072023")       
    app.run(debug=False)
