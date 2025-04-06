import os
import sys
from huggingface_hub import hf_hub_download
from config import MODEL_CONFIG

def download_model():
    """PhiMicroで使用するモデルをHugging Faceからダウンロード"""
    
    # モデルディレクトリの作成
    model_dir = os.path.dirname(MODEL_CONFIG['path'])
    os.makedirs(model_dir, exist_ok=True)
    
    # すでに存在する場合はスキップ
    if os.path.exists(MODEL_CONFIG['path']):
        print(f"モデルファイルはすでにダウンロード済みです: {MODEL_CONFIG['path']}")
        return
    
    try:
        print("Hugging Faceからモデルをダウンロード中...")
        
        # HuggingFace Hubからダウンロード
        hf_hub_download(
            repo_id="TheBloke/phi-4-mini-instruct-GGUF", 
            filename="phi-4-mini-instruct.Q4_K_M.gguf",
            local_dir=model_dir,
            local_dir_use_symlinks=False
        )
        
        # ファイル名を調整
        downloaded_path = os.path.join(model_dir, "phi-4-mini-instruct.Q4_K_M.gguf")
        if os.path.exists(downloaded_path) and downloaded_path != MODEL_CONFIG['path']:
            os.rename(downloaded_path, MODEL_CONFIG['path'])
            
        print(f"モデルのダウンロードが完了しました: {MODEL_CONFIG['path']}")
        
    except Exception as e:
        print(f"モデルのダウンロード中にエラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download_model()