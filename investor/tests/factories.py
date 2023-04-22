import factory
from factory.django import DjangoModelFactory
from factory import fuzzy
from investor.models import Investor
from core.tests.factories import UserFactory


class InvestorFactory(DjangoModelFactory):
    class Meta:
        model = Investor

    user = factory.SubFactory(UserFactory)
    balance = fuzzy.FuzzyDecimal(low=0, high=100000, precision=2)
    on_hold = 0