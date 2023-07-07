from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route("/predict")
def predict():
    msg = str(request.args.get("link"))
    if len(msg) > 10:
        return 'YES'
    else:
        return 'NO'

if __name__ == "__main__":
    app.run(debug=True)
