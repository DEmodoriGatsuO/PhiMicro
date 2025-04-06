from flask import Flask, request, jsonify, render_template, send_from_directory
from llama_cpp import Llama
import os
import time
import json
from config import MODEL_CONFIG, APP_CONFIG
import utils

app = Flask(__name__)

# モデルの初期化
print(f"モデルを読み込み中: {MODEL_CONFIG['path']}...")
start_time = time.time()

try:
    llm = Llama(
        model_path=MODEL_CONFIG['path'],
        n_ctx=MODEL_CONFIG['context_length'],
        n_batch=MODEL_CONFIG['batch_size'],
        n_gpu_layers=0,
        use_mlock=True
    )
    load_time = time.time() - start_time
    print(f"モデル読み込み完了（{load_time:.2f}秒）")
    model_ready = True
except Exception as e:
    print(f"モデル読み込みエラー: {e}")
    llm = None
    model_ready = False

# ルート - HTMLを提供
@app.route('/')
def index():
    return render_template('index.html')

# 静的ファイル
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# モデル情報API
@app.route('/api/info', methods=['GET'])
def model_info():
    if not model_ready:
        return jsonify({
            "status": "error",
            "message": "モデルが読み込まれていません"
        }), 500
    
    return jsonify({
        "status": "ready",
        "model": MODEL_CONFIG['name'],
        "context_length": MODEL_CONFIG['context_length'],
        "version": APP_CONFIG['version']
    })

# テキスト生成API
@app.route('/api/generate', methods=['POST'])
def generate():
    if not model_ready:
        return jsonify({"error": "モデルが読み込まれていません"}), 500
    
    data = request.json
    if not data or 'prompt' not in data:
        return jsonify({"error": "promptフィールドが必要です"}), 400
    
    user_prompt = data.get('prompt')
    formatted_prompt = utils.create_prompt(user_prompt)
    
    max_tokens = min(data.get('max_tokens', MODEL_CONFIG['default_max_tokens']), 
                     MODEL_CONFIG['max_tokens_limit'])
    temperature = data.get('temperature', MODEL_CONFIG['default_temperature'])
    
    try:
        start_time = time.time()
        
        output = llm(
            formatted_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=MODEL_CONFIG['stop_tokens']
        )
        
        inference_time = time.time() - start_time
        generated_text = output['choices'][0]['text'].strip()
        
        return jsonify({
            "generated_text": generated_text,
            "tokens_generated": len(generated_text.split()),
            "inference_time_seconds": round(inference_time, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ストリーミング応答API
@app.route('/api/generate_stream', methods=['POST'])
def generate_stream():
    if not model_ready:
        return jsonify({"error": "モデルが読み込まれていません"}), 500
    
    data = request.json
    if not data or 'prompt' not in data:
        return jsonify({"error": "promptフィールドが必要です"}), 400
    
    user_prompt = data.get('prompt')
    formatted_prompt = utils.create_prompt(user_prompt)
    
    max_tokens = min(data.get('max_tokens', MODEL_CONFIG['default_max_tokens']), 
                    MODEL_CONFIG['max_tokens_limit'])
    temperature = data.get('temperature', MODEL_CONFIG['default_temperature'])
    
    def generate():
        try:
            for chunk in llm(
                formatted_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=MODEL_CONFIG['stop_tokens'],
                stream=True
            ):
                text_chunk = chunk['choices'][0]['text']
                if text_chunk:
                    yield f"data: {text_chunk}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"
    
    return app.response_class(
        generate(),
        mimetype='text/event-stream'
    )

if __name__ == "__main__":
    app.run(debug=APP_CONFIG['debug'], host='0.0.0.0', port=APP_CONFIG['port'])