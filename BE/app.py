from flask import Flask, request
from flask_cors import CORS
import re
from get_tweet import GetTweet

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

@app.route("/predict")
def predict():
    msg = str(request.args.get('s'))
    if is_url(msg):
        tweet = get_tweet.get_text_form_tweet(msg)
        return f'{tweet}'
    else:
        return 'NO'

if __name__ == "__main__":
    get_tweet = GetTweet("0326130017", r"project_ML_13072023")
    app.run(debug=False)
