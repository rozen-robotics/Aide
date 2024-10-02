import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех доменов


GOOGLE_API_KEY = 'AIzaSyDSFTlciy3JIKYY4Ul6eiFUeuw-ttWpytI'
genai.configure(api_key=GOOGLE_API_KEY)


generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048, }


model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)

def get_answer(prompt, question):
    model = genai.GenerativeModel("gemini-1.5-flash")
    text = prompt + question
    response = model.generate_content(text)

    return response.text


@app.route('/ans', methods=['POST'])
def process_request():
    data = request.json
    request_type = data.get('request_type')
    text = data.get('text')

    if not request_type or not text:
        return jsonify({"error": "Invalid request. 'request_type' and 'text' are required."}), 400

    system_message = 'СИСТЕМНОЕ СООБЩЕНИЕ: Вы подключаетесь к голосовому помощнику и должны ответить как можно скорее.В качестве голосового помощника используйте короткие предложения и отвечайте непосредственно на запрос, не добавляя лишней информации. В ответ на следующие запросы вы произносите только важные слова, отдавая предпочтение логике и фактам, а не предположениям. Если вопрос некорректный, то в ответ пришли одно слово "ERROR". Вот вопрос: '
    system_message = system_message.replace(f'\n', '')


    api_response = get_answer(system_message, text)
    return jsonify(api_response)




if __name__ == '__main__':
    app.run(debug=True)
