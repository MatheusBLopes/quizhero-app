from django import forms
from django.contrib import admin
from .models import Question, QuestionAlternative, Quiz, QuizFolder, Category


class QuestionAdminForm(forms.ModelForm):
    
    alternative_a = forms.CharField(required=True)
    alternative_b = forms.CharField(required=True)
    alternative_c = forms.CharField(required=True)
    alternative_d = forms.CharField(required=True)
    correct_alternative = forms.ChoiceField(required=True, choices=[('1', 'Alternative A'), ('2', 'Alternative B'), ('3', 'Alternative C'), ('4', 'Alternative D')])

    class Meta:
        model = Question
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(QuestionAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            alternatives = self.instance.questionalternative_set.all()
            self.fields['alternative_a'].initial = alternatives[0].description
            self.fields['alternative_b'].initial = alternatives[1].description
            self.fields['alternative_c'].initial = alternatives[2].description
            self.fields['alternative_d'].initial = alternatives[3].description
            
            correct_alternative = alternatives.filter(is_correct=True).first()
            correct_alternative_index = list(alternatives).index(correct_alternative)
            self.fields['correct_alternative'].initial = str(correct_alternative_index + 1)

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

        existing_alternatives = list(question.questionalternative_set.all())

        for i, alternative in enumerate(alternatives):
            is_correct = i == correct_alternative_index
            if i < len(existing_alternatives):
                # Update existing alternative
                existing_alternative = existing_alternatives[i]
                existing_alternative.description = alternative
                existing_alternative.is_correct = is_correct
                existing_alternative.save()
            else:
                # Create new alternative
                QuestionAlternative.objects.create(question=question, description=alternative, is_correct=is_correct)

        return question

class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = ('description',)


class QuizAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(QuizFolder)
admin.site.register(Category)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
