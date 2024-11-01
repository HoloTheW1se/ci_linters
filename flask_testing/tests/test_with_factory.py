from .factories import ClientFactory, ParkingFactory
from flask_testing.main.models import Client, Parking


def test_create_client(app, db):
    new_client = ClientFactory()
    db.session.commit()
    assert new_client.id is not None
    assert len(db.session.query(Client).all()) == 3


def test_create_parking(client, db):
    new_parking = ParkingFactory()
    db.session.commit()
    assert new_parking.id is not None
    assert len(db.session.query(Parking).all()) == 2
