# check_models.py
import google.generativeai as genai

# ここにAPIキーを入れてください
GOOGLE_API_KEY = "AIzaSyDlDHlxlK7tNO3poH2Rc2VaeiK1suziYuo" 

try:
    genai.configure(api_key=GOOGLE_API_KEY)
    
    print("=== あなたの環境で使えるモデル一覧 ===")
    print(f"現在のライブラリバージョン: {genai.__version__}")
    
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            available_models.append(m.name)
            
    if not available_models:
        print("\n× モデルが見つかりませんでした。APIキーか通信環境を確認してください。")
    else:
        print("\n◎ 成功！上記のモデル名のどれかを views.py にコピペしてください。")

except Exception as e:
    print(f"\nエラーが発生しました: {e}")
    print("まだライブラリが古いか、インストールがうまくいっていません。")