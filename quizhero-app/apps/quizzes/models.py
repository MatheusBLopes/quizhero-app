from django.core.exceptions import ValidationError
from django.db import models



class Quiz(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)

    # def save(self, *args, **kwargs):
    #     if self.pk is None and self.questionalternative_set.count() != 4:
    #         raise ValidationError("A question must have exactly 4 alternatives.")
    #     super().save(*args, **kwargs)


class QuestionAlternative(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)





