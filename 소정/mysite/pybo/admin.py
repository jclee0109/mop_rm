from django.contrib import admin
from .models import Question

# ---------------------------------- [edit] ---------------------------------- #
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Question, QuestionAdmin)
# ---------------------------------------------------------------------------- #