from django import forms

from .models import Answer


class AnswerForm(forms.ModelForm):
    '''Форма для работы с моделью "Answer".'''

    class Meta:
        model = Answer
        fields = '__all__'
