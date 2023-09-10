from random import randint
import random
from faker import Faker


# def rand_ratio():
#     return randint(840, 900), randint(473, 573)


fake = Faker('pt_BR')
# print(signature(fake.random_number))


# def make_quiz():
#     return {
#         'title': fake.sentence(nb_words=6),
#         'description': fake.sentence(nb_words=12),
#         'preparation_time': fake.random_number(digits=2, fix_len=True),
#         'preparation_time_unit': 'Minutos',
#         'servings': fake.random_number(digits=2, fix_len=True),
#         'servings_unit': 'Porção',
#         'preparation_steps': fake.text(3000),
#         'created_at': fake.date_time(),
#         'author': {
#             'first_name': fake.first_name(),
#             'last_name': fake.last_name(),
#         },
#         'category': {
#             'name': fake.word()
#         },
#         'cover': {
#             'url': 'https://loremflickr.com/%s/%s/food,cook' % rand_ratio(),
#         }
#     }

def make_answer(number):
    return {
        'answer_description': fake.sentence(nb_words=12),
        'right_answer': True if number % 2 == 0 else False
    }

def make_question(number):
    return {
        'numb': number,
        'question_description': fake.sentence(nb_words=12),
        'answers': [make_answer(i) for i in range(4)]
    }


def make_quiz():
    return {
        'id': fake.random_number(digits=2, fix_len=True),
        'title': fake.sentence(nb_words=6),
        'quiz_description': fake.sentence(nb_words=12),
        'questions': [make_question(i + 1) for i in range(10)]

    }


if __name__ == '__main__':
    from pprint import pprint
    pprint(make_quiz())