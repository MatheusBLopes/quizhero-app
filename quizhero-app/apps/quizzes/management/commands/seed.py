from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker
from apps.quizzes.models import Question, QuestionAlternative, Quiz


class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def __init__(self):
        super().__init__()
        self.fake = Faker()
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Clear the database before seeding',
        )
    
        parser.add_argument(
            '--num_quizzes',
            type=int,
            default=10,
            help='Specify the number of quizzes to create',
        )

    def create_quiz(self, user):
        title = self.fake.sentence(nb_words=3)
        description = self.fake.text(max_nb_chars=200)
        quiz = Quiz.objects.create(name=title, description=description, user=user)
        return quiz

    def create_question(self, quiz):
        text = self.fake.text(max_nb_chars=200)
        question = Question.objects.create(description=text, quiz=quiz)
        correct_choice = QuestionAlternative.objects.create(description=self.fake.word(), question=question, is_correct=True)
        for i in range(3):
            QuestionAlternative.objects.create(description=self.fake.word(), question=question, is_correct=False)
        return question


    def create_question_set(self, quiz):
        for i in range(5):
            question = self.create_question(quiz)

    def create_quiz_set(self, num_quizzes):
        master_user = User.objects.get(username='master')
        for i in range(num_quizzes):
            quiz = self.create_quiz(master_user)
            quiz.author = master_user
            quiz.save()
            self.create_question_set(quiz)

    def handle(self, *args, **options):
        if options['clean']:
            QuestionAlternative.objects.all().delete()
            Question.objects.all().delete()
            Quiz.objects.all().delete()


        num_quizzes = options['num_quizzes']
        self.create_quiz_set(num_quizzes)

        self.stdout.write(self.style.SUCCESS('Data seeded successfully'))