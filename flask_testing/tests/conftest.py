import pytest
from flask_testing.main.app import create_app, db as _db
from flask_testing.main.models import Parking, Client, Client_Parking


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite://'
    with _app.app_context():
        _db.create_all()
        client_1 = Client(
            id=1,
            name="name",
            surname="surname",
            car_number="Р007ОС",
            credit_card="5555444433332222"
        )
        # Создание второго клиента для теста по заезду на парковку
        client_2 = Client(
            id=2,
            name="new_name",
            surname="new_surname",
            car_number="C009OK",
            credit_card="9876123498761234"
        )
        parking = Parking(
            id=1,
            address="Moscow, pl. Lenina",
            opened=1,
            count_places=10,
            count_available_places=5
        )

        _db.session.add(client_1)
        _db.session.add(client_2)
        _db.session.add(parking)

        client_parking = Client_Parking(
            client_id=1,
            parking_id=1
        )
        _db.session.add(client_parking)

        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    _client = app.test_client()
    yield _client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
