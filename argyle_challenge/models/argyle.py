from pydantic import BaseModel
from typing import Optional
import pycountry
import re


class Client(BaseModel):
    country: Optional[str]
    payment_verified: Optional[bool]
    rating: Optional[str]
    reviews_count: Optional[int]

    def set_country(self, country: str):
        print('set_country', country)
        iso_3166_country = pycountry.countries.search_fuzzy(country)
        self.country = iso_3166_country[0].alpha_2

    def set_payment_verified(self, status):
        if status is None:
            payment_verified = False
        else:
            payment_verified = True
        self.payment_verified = payment_verified


class Payment(BaseModel):
    type: Optional[str]
    amount: Optional[str]
    currency: Optional[str]

    def set_type_and_amount(self, item: dict):
        amount = item.get('amount').get('amount')
        hourly_budget = item.get('hourlyBudgetText')
        if hourly_budget is None:
            self.type = "fixed price"
            self.amount = str(amount)
        else:
            self.type = "hourly"
            self.amount = hourly_budget


class Job(BaseModel):
    website: Optional[str]
    url: Optional[str]
    title: Optional[str]
    description: Optional[str]
    date_posted: Optional[str]
    duration: Optional[str]
    engagement: Optional[str]
    experience_level: Optional[str]
    location_mandatory: Optional[bool]
    freelancer_location: Optional[list[str]]
    attributes: Optional[list[str]]
    service: Optional[str]
    client: Optional[Client]
    payment: Optional[Payment]

    def set_url(self, url_end: str):
        url = f"https://www.upwork.com/jobs/{url_end}"
        self.url = url

    def set_description(self, description: str):
        description = description.replace('\n', '')
        description = re.sub(r'\s+', ' ', description)
        self.description = description

    def set_freelancer_location(self, locations: list[str]):
        for index, country in enumerate(locations):
            locations[index] = pycountry.countries.search_fuzzy(country)[0].alpha_2
        self.freelancer_location = locations

    def set_attributes(self, attrs: list[dict]):
        for index, attribute in enumerate(attrs):
            attrs[index] = attribute.get('prettyName', None)
        self.attributes = attrs
