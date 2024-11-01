import factory

from flask_testing.main.app import db
from flask_testing.main.models import Client, Parking


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker("first_name")  # type: ignore
    surname = factory.Faker("last_name")  # type: ignore
    credit_card = factory.Faker("text")  # type: ignore
    car_number = factory.Faker("text")  # type: ignore


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker("address")  # type: ignore
    opened = factory.Faker("boolean")  # type: ignore
    count_places = factory.Faker("random_int")  # type: ignore
    count_available_places = factory.LazyAttribute(lambda o: o.count_places - 1)  # type: ignore # noqa
