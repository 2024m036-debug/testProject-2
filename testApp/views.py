from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from django.template.loader import render_to_string # 追加
from django.http import JsonResponse # 追加
from .forms import EmailGenerationForm
from .models import EmailGeneration
import json
import re

# ▼▼▼ Gemini設定 ▼▼▼
import google.generativeai as genai

# ★APIキー設定
GOOGLE_API_KEY = "AIzaSyDlDHlxlK7tNO3poH2Rc2VaeiK1suziYuo"
genai.configure(api_key=GOOGLE_API_KEY)


def generate_email_with_gemini(target_name, request_content, category, tone):
    """
    Gemini APIを使ってメールを生成し、件名と本文を返す関数
    """
    try:
        # スクリーンショットで成功が確認できたモデル名を使用
        model = genai.GenerativeModel('gemini-flash-latest')

        prompt = f"""
        あなたは優秀なビジネスメール作成アシスタントです。
        以下の条件でメールを作成し、必ずJSON形式のみで返してください。
        解説やMarkdownの装飾（```jsonなど）は一切不要です。
        
        宛先: {target_name}
        要件: {request_content}
        カテゴリ: {category}
        トーン: {tone}

        出力形式:
        {{
            "subject": "件名",
            "body": "本文"
        }}
        """

        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )

        # レスポンスのクリーニング
        result_text = response.text.replace("```json", "").replace("```", "").strip()
        result_json = json.loads(result_text)
        
        return result_json.get('subject', '件名なし'), result_json.get('body', '生成エラー')

    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None, f"エラーが発生しました: {e}"


@login_required
def create_email(request):
    if request.method == 'POST':
        form = EmailGenerationForm(request.POST)
        if form.is_valid():
            email_obj = form.save(commit=False)
            email_obj.user = request.user
            
            # Gemini呼び出し
            try:
                # フォームのフィールド名に合わせて取得
                cat = form.cleaned_data.get('category', 'ビジネス全ば')
                tone = form.cleaned_data.get('tone_setting', '標準')

                subject, body = generate_email_with_gemini(
                    target_name=email_obj.recipient_name,
                    request_content=email_obj.context_notes,
                    category=cat,
                    tone=tone
                )

                if subject:
                    email_obj.subject = subject
                    email_obj.body = body
                else:
                    email_obj.subject = "生成エラー"
                    email_obj.body = body

            except Exception as e:
                email_obj.subject = "システムエラー"
                email_obj.body = f"処理中にエラーが発生しました: {e}"
            
            email_obj.save()
            return redirect('email_list')
    else:
        form = EmailGenerationForm()
    
    return render(request, 'mail_app/create_email.html', {'form': form})


@login_required
def email_list(request):
    # ユーザー自身の履歴を新しい順に取得
    emails = EmailGeneration.objects.filter(user=request.user).order_by('-created_at')
    search_query = request.GET.get('query', '') # None回避
    
    if search_query:
        emails = emails.filter(
            Q(subject__icontains=search_query) | 
            Q(recipient_name__icontains=search_query) |
            Q(body__icontains=search_query)
        )

    context = {
        'emails': emails, 
        'search_query': search_query
    }

    # ▼▼▼ 非同期検索（Ajax）への対応 ▼▼▼
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # 部分的なHTML（partial）だけを作成してJSONで返す
        html = render_to_string('mail_app/email_list_partial.html', context, request=request)
        return JsonResponse({'html': html})
    
    # 通常のページアクセス時
    return render(request, 'mail_app/email_list.html', context)


@login_required
def email_detail(request, pk):
    email = get_object_or_404(EmailGeneration, pk=pk, user=request.user)
    return render(request, 'mail_app/email_detail.html', {'email': email})


@login_required
def email_edit(request, pk):
    email = get_object_or_404(EmailGeneration, pk=pk, user=request.user)
    if request.method == "POST":
        email.subject = request.POST.get('subject')
        email.body = request.POST.get('body')
        email.save()
        return redirect('email_detail', pk=pk)
    return render(request, 'mail_app/email_edit.html', {'email': email})


@login_required
def email_delete(request, pk):
    email = get_object_or_404(EmailGeneration, pk=pk, user=request.user)
    if request.method == "POST":
        email.delete()
        return redirect('email_list')
    return render(request, 'mail_app/email_delete.html', {'email': email})