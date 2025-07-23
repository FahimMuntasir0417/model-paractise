from django.core.management.base import BaseCommand
from event.models import Category, Event, Participant
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Populate fake data into the database.'

    def handle(self, *args, **kwargs):
        # Create Categories
        categories = []
        for name in ['Tech', 'Music', 'Art', 'Business', 'Education']:
            cat, _ = Category.objects.get_or_create(name=name, defaults={'description': fake.text()})
            categories.append(cat)

        # Create Events
        events = []
        for _ in range(10):
            event = Event.objects.create(
                name=fake.sentence(nb_words=3),
                description=fake.text(),
                date=fake.future_date(end_date='+30d'),
                time=fake.time_object(),
                location=fake.city(),
                category=random.choice(categories)
            )
            events.append(event)

        # Create Participants
        for _ in range(20):
            participant = Participant.objects.create(
                name=fake.name(),
                email=fake.unique.email()
            )
            participant.events.set(random.sample(events, k=random.randint(1, 3)))

        self.stdout.write(self.style.SUCCESS("✅ Fake data populated successfully."))
