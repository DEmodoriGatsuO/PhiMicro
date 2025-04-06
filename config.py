import os

# モデル設定
MODEL_CONFIG = {
    'name': 'phi-4-mini-instruct-q4_k_m',
    'path': os.path.join(os.path.dirname(__file__), "models", "phi-4-mini-instruct-q4_k_m.gguf"),
    'context_length': 4096,
    'batch_size': 8,
    'default_max_tokens': 256,
    'max_tokens_limit': 512,
    'default_temperature': 0.7,
    'stop_tokens': ["<|user|>", "</s>"]
}

# アプリケーション設定
APP_CONFIG = {
    'version': '1.0.0',
    'debug': False,
    'port': 8080
}