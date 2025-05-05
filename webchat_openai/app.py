# webchat_openai/app.py

import os
import time
import openai
from flask import Flask, render_template, request, jsonify
from config.openai_settings import OPENAI_API_KEY, ASSISTANTS

openai.api_key = OPENAI_API_KEY

app = Flask(__name__, template_folder="templates")

@app.route('/')
def index():
    return render_template('index.html', assistants=ASSISTANTS)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    assistant_id = data.get('assistant_id')
    prompt = data.get('prompt')
    second_text = data.get('second_text')

    if not assistant_id or not prompt or not second_text:
        return jsonify({"error": "Brak wymaganych danych."}), 400

    full_message = f"{prompt}\n\n{second_text}"

    try:
        thread = openai.beta.threads.create()

        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=full_message
        )

        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # Polling - czekamy na odpowiedź
        while True:
            run_status = openai.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break
            elif run_status.status == "failed":
                error_info = getattr(run_status, "last_error", None)
                if error_info:
                    return jsonify({"error": f"Assistant run failed: {error_info}"}), 500
                else:
                    return jsonify({"error": "Assistant run failed. (no details)"}), 500
        time.sleep(1)

        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        last_message = messages.data[0].content[0].text.value

        return jsonify({"response": last_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
