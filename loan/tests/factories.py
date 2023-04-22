import factory
from factory import fuzzy
from factory.django import DjangoModelFactory
from loan.models import Loan,LoanOffer,LoanRequest
from investor.tests.factories import InvestorFactory
from borrower.tests.factories import BorrowerFactory


class LoanRequestFactory(DjangoModelFactory):
    class Meta:
        model = LoanRequest

    borrower = factory.SubFactory(BorrowerFactory)
    loan_amount = fuzzy.FuzzyDecimal(1000, 10000, precision=2)
    loan_period = fuzzy.FuzzyInteger(1, 12)
    status = 'active'