import google.generativeai as genai
from django.conf import settings

class EmailGeneratorService:
    @staticmethod
    def generate_email(recipient_name, context_notes, tone_setting):
        # settings.py に登録したキーを設定
        genai.configure(api_key="AIzaSyAoxJcO2LLdvrr3iSLrdd9AO7OUt4rKrC4")
        
        # GoogleのAIモデル（Gemini Pro）を準備
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            f"あなたは有能なビジネス秘書です。以下の条件で日本のビジネスメールを作成してください。\n\n"
            f"【宛先】{recipient_name}\n"
            f"【要件・背景】{context_notes}\n"
            f"【トーン】{tone_setting}\n\n"
            f"出力形式: 1行目に「件名:〇〇」を入れ、2行目以降に本文を書いてください。"
        )

        try:
            # AIに生成させる
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            # エラーが起きた場合
            return f"生成に失敗しました: {str(e)}"