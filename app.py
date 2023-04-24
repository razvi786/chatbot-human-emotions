from flask import Flask, render_template, request, jsonify

from chat import get_response, get_mood, get_mood_percentage, get_emotion



app = Flask(__name__)

@app.get("/")
def index_get():
    return render_template("base.html")



@app.post("/predict")
def predict():
    text = request.get_json().get("message")

    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


@app.post("/mood")
def mood():
    text = request.get_json().get("message")

    response = get_mood(text)
    percentage = get_mood_percentage(text)
    # emotions = get_emotion(text)
    emotions = []
    message = {"answer": response, "percentage": percentage, "emotions": emotions}
    print(message)
    return jsonify(message)
   

if __name__ == "__main__":
    app.run(debug=True)
