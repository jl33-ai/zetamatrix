from django.core.management.base import BaseCommand
from django.utils import timezone
from game.models import DailyChallenge
import random

class Command(BaseCommand):
    help = 'Generates the daily challenge'

    def generate_question(self):
        op_list = ['+', '-', '*', '/']
        oper = random.choice(op_list)
        if oper in ['+', '-']:
            num1 = random.randint(2, 100)
            num2 = random.randint(2, 100)
        elif oper == '*':
            num1 = random.randint(2, 12)
            num2 = random.randint(2, 100)
        elif oper == '/':
            num2 = random.randint(2, 12)
            num1 = num2 * random.randint(2, 100)
        return {'num1': num1, 'oper': oper, 'num2': num2}

    def handle(self, *args, **options):
        questions = [self.generate_question() for _ in range(300)]
        DailyChallenge.objects.create(
            date=timezone.now().date(),
            questions=questions
        )

        self.stdout.write(self.style.SUCCESS('Successfully generated the daily challenge'))
