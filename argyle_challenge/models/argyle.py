from pydantic import BaseModel
import pycountry


class Client(BaseModel):
    country: str
    payment_verified: bool
    rating: str
    reviews_count: int

    def set_country(self, country: str):
        iso_3166_country = pycountry.countries.search_fuzzy(country)
        self.country = iso_3166_country[0]

    def set_payment_verified(self, status):
        if status is None:
            payment_verified = False
        else:
            payment_verified = True
        self.payment_verified = payment_verified


class Payment(BaseModel):
    type: str
    amount: str
    currency: str

    def set_type_and_amount(self, item:dict):
        amount = item.get('amount').get('amount')
        hourly_budget = item.get('hourlyBudgetText')
        if hourly_budget is None:
            self.type = "fixed price"
            self.amount = amount
        else:
            self.type = "hourly"
            self.amount = hourly_budget



class Job(BaseModel):
    website: str
    url: str
    title: str
    description: str
    date_posted: str
    duration: str
    engagement: str
    experience_level: str
    location_mandatory: bool
    freelancer_location: list[str]
    attributes: list[str]
    service: str
    client: Client
    payment: Payment

    def set_url(self, url_end: str):
        url = f"https://www.upwork.com/jobs/{url_end}"
        self.url = url

    def set_description(self, description: str):
        description = description.replace('\n', '')
        self.description = description

    def set_freelancer_location(self, locations: list[str]):
        for index, country in enumerate(locations):
            locations[index] = pycountry.countries.search_fuzzy(country)[0]
        self.freelancer_location = locations

    def set_attributes(self, attrs: list[dict]):
        for index, attribute in enumerate(attrs):
            attrs[index] = attribute.get('prettyName', None)
        self.attributes = attrs
