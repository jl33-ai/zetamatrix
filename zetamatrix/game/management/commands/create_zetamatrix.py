from django.core.management.base import BaseCommand
from game.models import SolvedAddition, SolvedDivision, SolvedSubtraction, SolvedMultiplication

class Command(BaseCommand):
    help = 'Generates the zetamatrix'

    def handle(self, *args, **options):
        
        for oper in ['+', '-', '*', '/']:
            # use a hash map
            times_dict = {}
            for row in table: 
                time_taken = 3
                if (num1, num2) in times_dict:
                    avg, n = times_dict[(num1, num2)]
                    new_avg, new_n = ((avg*n)+time_taken)/(n+1), n+1
                    times_dict[(num1, num2)] = new_avg, new_n
                else: 
                    times_dict[(num1, num2)] = time_taken, n
        
        
            


        self.stdout.write(self.style.SUCCESS('Successfully generated the zetamatrix'))
