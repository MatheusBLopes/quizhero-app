from django import forms
from django.contrib import admin
from .models import Quiz, Question, QuestionAlternative


class QuestionAdminForm(forms.ModelForm):
    
    alternative_a = forms.CharField(required=True)
    alternative_b = forms.CharField(required=True)
    alternative_c = forms.CharField(required=True)
    alternative_d = forms.CharField(required=True)
    correct_alternative = forms.ChoiceField(required=True, choices=[('1', 'Alternative A'), ('2', 'Alternative B'), ('3', 'Alternative C'), ('4', 'Alternative D')])

    class Meta:
        model = Question
        fields = '__all__'

    def save(self, commit=True):
        question = super().save(commit=False)
        question.save()

        correct_alternative_index = int(self.cleaned_data['correct_alternative']) - 1
        
        alternatives = [
            self.cleaned_data['alternative_a'],
            self.cleaned_data['alternative_b'],
            self.cleaned_data['alternative_c'],
            self.cleaned_data['alternative_d']
        ]

        for i, alternative in enumerate(alternatives):
            is_correct = i == correct_alternative_index
            QuestionAlternative.objects.create(question=question, description=alternative, is_correct=is_correct)

        return question

class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm


admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
