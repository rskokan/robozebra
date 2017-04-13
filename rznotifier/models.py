from django.db import models


class Loan(models.Model):
    notified = models.BooleanField(default=False)
    loan_id = models.IntegerField(db_index=True)
    date_published = models.DateTimeField(null=True)
    main_income_type = models.CharField(max_length=30, null=True)
    region = models.SmallIntegerField(null=True)
    story = models.TextField(null=True)
    questions_count = models.SmallIntegerField(null=True)
    purpose = models.SmallIntegerField(null=True)
    covered = models.BooleanField(default=False)
    topped = models.NullBooleanField()
    deadline = models.DateTimeField(null=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=4, null=True)
    name = models.CharField(max_length=200, null=True)
    term_in_months = models.SmallIntegerField(null=True)
    #    investment_rate = models.FloatField() # 1.0 is fully invested
    user_id = models.IntegerField(null=True)
    rating = models.CharField(max_length=5, db_index=True)
    nick_name = models.CharField(max_length=30)
    investments_count = models.SmallIntegerField(null=True)
    remaining_investment = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    published = models.BooleanField(default=False)

    def __str__(self):
        return '[{}] {:.0f} Kc | {:.2f}% | {} mesicu | {} | https://app.zonky.cz/#/marketplace/detail/{}/'.format(
            self.get_rating_for_ui(), self.amount, self.interest_rate * 100, self.term_in_months,
            self.name, self.loan_id)

    def update_values(self, new_values):
        self.date_published = new_values['datePublished']
        self.main_income_type = new_values['mainIncomeType']
        self.region = new_values['region']
        self.story = new_values['story']
        self.questions_count = new_values['questionsCount']
        self.purpose = new_values['purpose']
        self.covered = new_values['covered']
        self.topped = new_values['topped']
        self.deadline = new_values['deadline']
        self.interest_rate = new_values['interestRate']
        self.name = new_values['name']
        self.term_in_months = new_values['termInMonths']
        self.user_id = new_values['userId']
        self.rating = new_values['rating']
        self.nick_name = new_values['nickName']
        self.investments_count = new_values['investmentsCount']
        self.remaining_investment = new_values['remainingInvestment']
        self.amount = new_values['amount']
        self.published = new_values['published']

    def get_rating_for_ui(self):
        """
        Mapping of API-UI Zonky ratings:
        AAAAA - A**, 3.99%
        AAAA - A*, 4.99%
        AAA - A++, 5.99%
        AA - A+, 8.49%
        A - A, 10.99%
        B - B, 13.49%
        C - C, 15.49%
        D - D, 19.99%
        """
        res = None
        if self.rating == 'AAAAA':
            res = 'A**'
        elif self.rating == 'AAAA':
            res = 'A*'
        elif self.rating == 'AAA':
            res = 'A++'
        elif self.rating == 'AA':
            res = 'A+'
        elif self.rating == 'A':
            res = 'A'
        elif self.rating == 'B':
            res = 'B'
        elif self.rating == 'C':
            res = 'C'
        elif self.rating == 'D':
            res = 'D'
        else:
            res = 'UNKNOWN'

        return res

    def get_notif_channel(self):
        return '#zonky-{}'.format(self.rating)
