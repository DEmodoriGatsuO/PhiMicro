def create_prompt(user_input):
    """
    Phi-4-Miniに最適なプロンプトフォーマットを作成
    
    Args:
        user_input (str): ユーザーの入力テキスト
        
    Returns:
        str: フォーマット済みプロンプト
    """
    return f"<|user|>\n{user_input}\n<|assistant|>\n"

def extract_response(raw_output):
    """
    モデル出力から必要な部分を抽出
    
    Args:
        raw_output (str): モデルからの生の出力
        
    Returns:
        str: クリーニングされた応答テキスト
    """
    # 必要に応じて応答のポストプロセスを実装
    return raw_output.strip()