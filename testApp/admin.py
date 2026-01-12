from django.contrib import admin
from .models import EmailGeneration

# Category はもう使わないので削除しました
admin.site.register(EmailGeneration)