from django.test import TestCase
from django.contrib.auth.models import User
from testApp.models import EmailGeneration, Category #

class EmailGenerationModelTest(TestCase):
    def setUp(self):
        """テストデータの準備"""
        # テスト用ユーザーの作成
        self.user = User.objects.create_user(username='testuser', password='password123')
        # テスト用カテゴリの作成
        self.category = Category.objects.create(name='営業', description='新規開拓用')

    def test_email_generation_creation(self):
        """EmailGenerationモデルが正しく保存されるかテスト"""
        # 名前を「山田太郎」にして、モデル側で「様宛」が付くか検証する
        email = EmailGeneration.objects.create(
            user=self.user,
            category=self.category,
            recipient_name='山田太郎', # 「様」を抜いて入力
            context_notes='打ち合わせの依頼です。',
            tone_setting='standard',
            subject='お打ち合わせのお願い',
            body='山田様、お世話になっております...'
        )

        # 1. データベースに保存されているか確認
        self.assertEqual(EmailGeneration.objects.count(), 1)

        # 2. __str__ メソッドの出力を確認
        # models.pyの定義：f"{self.created_at.strftime('%Y-%m-%d')} - {self.recipient_name}様宛"
        expected_str = f"{email.created_at.strftime('%Y-%m-%d')} - 山田太郎様宛"
        self.assertEqual(str(email), expected_str)