from django.core.management.base import BaseCommand
from game.models import SolvedAddition, SolvedDivision, SolvedSubtraction, SolvedMultiplication
import pandas as pd
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Backfills data into relevant tables'

    def handle(self, *args, **options):
        try:
            data = pd.read_csv('/Users/justinlee/Documents/projport/zetamatrix/zetamatrix/game/management/commands/all_data.csv')
            data = data[10:]
            user = User.objects.get(username='justinlee')

            # Mapping operators to models
            operator_to_model = {
                '+': SolvedAddition,
                '-': SolvedSubtraction,
                '*': SolvedMultiplication,
                '/': SolvedDivision
            }

            for _, question in data.iterrows():
                model = operator_to_model.get(question['operator'])
                if model:
                    model.objects.create(
                        user=user,
                        num1=int(question['num1']),
                        num2=int(question['num2']),
                        time_taken=int(1000*question['timetaken'])
                    )

            self.stdout.write(self.style.SUCCESS('Successfully backfilled data'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "justinlee" does not exist'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
