import factory
from datetime import date, time
from announcement.models import Announcement


class AnnouncementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Announcement

    title = factory.Faker("sentence", nb_words=6)
    message = factory.Faker("paragraph")
    schedule_date = factory.LazyFunction(date.today)  # Defaults to today
    schedule_time = factory.LazyFunction(
        lambda: time(9, 0))
    receiver_group = factory.Iterator(
        [choice[0] for choice in Announcement.RECEIVER_GROUP])
