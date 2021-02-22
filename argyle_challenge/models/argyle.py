from pydantic import BaseModel


class Client(BaseModel):
    location: str
    paymentVerificationStatus: bool
    rating: str
    reviews: str

    def set_country(self, string, iso_3166_format=False):
        pass


class Payment(BaseModel):
    type: str
    amount: str
    currency: str


class Job(BaseModel):
    website: str
    url: str
    title: str
    description: str
    date_posted: str
    country: str
    duration: str
    engagement: str
    experience_level: str
    prefFreelancerLocationMandatory: bool
    prefFreelancerLocation: list[str]
    attributes: list[str]
    service: str
    client: Client
    payment: Payment
