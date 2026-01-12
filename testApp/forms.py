from django import forms
from .models import EmailGeneration

class EmailGenerationForm(forms.ModelForm):
    class Meta:
        model = EmailGeneration
        # フォームに表示したい項目をすべて書きます
        fields = ['category', 'recipient_name', 'context_notes', 'tone_setting']
        
        # 画面の見た目を整えるための設定（Bootstrapなど）
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'recipient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 株式会社〇〇 山田様'}),
            'context_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '例: 打ち合わせの日程調整をお願いしたい。'}),
            'tone_setting': forms.Select(attrs={'class': 'form-control'}),
        }