from django.db import models
from django.contrib.auth.models import User

class EmailGeneration(models.Model):
    # ▼ カテゴリの選択肢
    CATEGORY_CHOICES = [
        ('business', 'ビジネス全般'),
        ('apology', 'お詫び・謝罪'),
        ('thank_you', 'お礼・感謝'),
        ('request', '依頼・お願い'),
        ('notice', '通知・お知らせ'),
        ('greeting', '挨拶（季節・転勤など）'),
    ]

    # ▼ トーン（雰囲気）の選択肢
    TONE_CHOICES = [
        ('standard', '標準（失礼なく一般的）'),
        ('polite', 'とても丁寧（目上の人へ）'),
        ('friendly', '親しみやすく（柔らかめ）'),
        ('concise', '簡潔に（急ぎ・チャット）'),
        ('apologetic', 'お詫びの気持ちで'),
    ]

    # ▼ ユーザーとの紐づけ
    # null=True, blank=True にすることで、既存データがあってもエラー回避できます
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # ▼ 入力項目
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='business',
        verbose_name='カテゴリ'
    )

    recipient_name = models.CharField(
        max_length=100,
        verbose_name='相手の名前・役職'
    )

    context_notes = models.TextField(
        verbose_name='伝えたい要件・状況'
    )

    tone_setting = models.CharField(
        max_length=50,
        choices=TONE_CHOICES,
        default='standard',
        verbose_name='トーン設定'
    )

    # ▼ 生成結果の保存用（検索機能の対象フィールド）
    subject = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField(blank=True, null=True)

    # ▼ 編集済みフラグ（AI生成後に手動修正したか？）
    is_edited = models.BooleanField(default=False)

    # ▼ 作成日時
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # 管理画面などで表示される名前
        date_str = self.created_at.strftime('%Y-%m-%d')
        return f"{self.recipient_name}様へのメール ({date_str})"