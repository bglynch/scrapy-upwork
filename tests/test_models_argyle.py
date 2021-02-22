import unittest
from argyle_challenge.models.argyle import Job, Client, Payment


class MyTestCase(unittest.TestCase):
    # sample payment data
    hourly_payment_data = {'amount': {'currencyCode': 'USD', 'amount': 0}, 'hourlyBudgetText': '$15.00-$30.00'}
    fixed_payment_data = {'amount': {'currencyCode': 'USD', 'amount': 500}, 'hourlyBudgetText': None}
    attributes_data = [
        {'freeText': None, 'skillType': 3, 'highlighted': False, 'prettyName': 'Microsoft Excel'},
        {'freeText': None, 'skillType': 3, 'highlighted': False, 'prettyName': 'SQL'},
        {'freeText': None, 'skillType': 3, 'highlighted': False, 'prettyName': 'MySQL'},
        {'freeText': None, 'skillType': 3, 'highlighted': False, 'prettyName': 'Database Management'},
        {'freeText': None, 'skillType': 3, 'highlighted': False, 'prettyName': 'Data Mining'}
    ]

    def test_payment_class(self):
        hourly_payment = Payment()
        hourly_payment.set_type_and_amount(self.hourly_payment_data)
        self.assertEqual(hourly_payment.amount, '$15.00-$30.00')
        self.assertEqual(hourly_payment.type, 'hourly')

        fixed_payment = Payment()
        fixed_payment.set_type_and_amount(self.fixed_payment_data)
        self.assertEqual(fixed_payment.amount, '500')
        self.assertEqual(fixed_payment.type, 'fixed price')

    def test_client_class(self):
        client = Client()
        client.set_country('United States')
        client.set_payment_verified(None)
        self.assertEqual(client.country, 'US')
        self.assertEqual(client.payment_verified, False)

        client.set_payment_verified(1)
        self.assertEqual(client.payment_verified, True)

    def test_job_class(self):
        job = Job()
        job.set_url('some-url')
        self.assertEqual(job.url, 'https://www.upwork.com/jobs/some-url')

        job.set_description('some test\n\n    description\n')
        self.assertEqual(job.description, 'some test description')

        job.set_freelancer_location(['Ireland', 'United States'])
        self.assertEqual(job.freelancer_location, ['IE', 'US'])

        job.set_attributes(self.attributes_data)
        self.assertEqual(job.attributes, ['Microsoft Excel', 'SQL', 'MySQL', 'Database Management', 'Data Mining'])


if __name__ == '__main__':
    unittest.main()
