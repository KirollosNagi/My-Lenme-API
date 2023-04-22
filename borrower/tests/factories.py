import factory
from factory.django import DjangoModelFactory
from factory import fuzzy
from core.tests.factories import UserFactory
from borrower.models import Borrower




class BorrowerFactory(DjangoModelFactory):
    class Meta:
        model = Borrower

    user = factory.SubFactory(UserFactory)
    balance = fuzzy.FuzzyDecimal(low=0, high=100000, precision=2)