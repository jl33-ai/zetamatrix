from django.core.management.base import BaseCommand
from game.models import GameSession
import pandas as pd
from django.contrib.auth.models import User
import random
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Backfills data into relevant tables'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username='justinlee')
            model = GameSession
            for _ in range(100):  # Set the number of instances you want to create
                # Create a GameSession instance with a random score and the default start_time
                session = GameSession.objects.create(
                    user=user,
                    score=random.randint(40, 60),  # Random score between 40 and 60
                    length=120,
                    is_dailychallenge=False
                )

                # Generate a random timedelta, e.g., up to 30 days back
                random_days_back = timedelta(days=random.randint(0, 30))

                # Generate a random time offset within a day (up to 24 hours back)
                random_time_offset = timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))

                # Calculate the random start_time
                random_start_time = timezone.now() - random_days_back - random_time_offset

                # Override the auto_now_add start_time with the random_start_time
                session.start_time = random_start_time

                # Save the instance again to update the start_time
                session.save()
        

            self.stdout.write(self.style.SUCCESS('Successfully added synthetic data'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "justinlee" does not exist'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
