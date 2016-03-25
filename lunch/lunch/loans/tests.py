# lunch/loans/test.py
from django.test import TestCase
from .models import Loan, Functionteam, Cocodri, Pegadri
from django.contrib.auth.models import User
from datetime import datetime
from django.test import Client

class LoanViewTests(TestCase):

    def setUp(self):
        user = User.objects.create_user('test_user', 'test_user@gmail.com', '0000')
        Functionteam.objects.create(name='ATS')
        Cocodri.objects.create(name='test', email='test@apple.com', owner=user)
        Pegadri.objects.create(name='test', email='test@pegatroncorp.com', owner=user)

        function_team = Functionteam.objects.get(name='ATS')
        cocodri = Cocodri.objects.get(name='test')
        pegadri = Pegadri.objects.get(name='test')

        Loan.objects.create(
            owner=user, function_team=function_team, cocodri=cocodri,
            pegadri=pegadri,purpose='測試開單', disassemble=True,
            pega_dri_mail_group=[pegadri], created_at=datetime.now()
        )

        # login user and check login
        self.client = Client()
        login = self.client.login(username='test_user', password='0000')
        self.assertEqual(login, True)

    def tearDown(self):
        User.objects.all().delete()
        Functionteam.objects.all().delete()
        Pegadri.objects.all().delete()
        Cocodri.objects.all().delete()
        Loan.objects.all().delete()

    def test_list_view(self):
        r = self.client.get('/loan/')
        self.assertContains(
            r, '<a class="navbar-brand" href="/">PTD Alpha</a>', html=True,
        )
        self.assertContains(
            r, '<a href="/loan/1/">#1 ATS(test_user)</a>', html=True,
        )