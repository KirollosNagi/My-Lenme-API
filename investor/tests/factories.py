import factory
from factory.django import DjangoModelFactory
from factory import fuzzy

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from investor.models import Investor


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = fuzzy.FuzzyText(length=10, prefix='user_')
    email = factory.LazyAttribute(lambda user: f"{user.username}@example.com")
    password = factory.LazyFunction(lambda: make_password('password'))


class InvestorFactory(DjangoModelFactory):
    class Meta:
        model = Investor

    user = factory.SubFactory(UserFactory)
    balance = fuzzy.FuzzyDecimal(low=0, high=100000, precision=2)
    on_hold = 0