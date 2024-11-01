import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from typing import List

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .models import Client, Parking, Client_Parking

    @app.before_request
    def before_request():
        db.create_all()

    @app.teardown_appcontext
    def shutdown(exception=None):
        db.session.remove()

    @app.route('/clients', methods=['GET'])
    def get_clients():
        clients: List[Client] = db.session.query(Client).all()
        clients_list = [client.to_json() for client in clients]
        return jsonify(clients_list), 200

    @app.route('/clients/<int:client_id>', methods=['GET'])
    def get_client_by_id(client_id: int):
        client: Client = db.session.query(Client).get(client_id)
        return jsonify(client.to_json()), 200

    @app.route('/parkings/<int:parking_id>', methods=['GET'])
    def get_parking_by_id(parking_id: int):
        parking: Parking = db.session.query(Parking).get(parking_id)
        return jsonify(parking.to_json()), 200

    @app.route('/clients', methods=['POST'])
    def create_client():
        name = request.form.get('name', type=str)
        surname = request.form.get('surname', type=str)
        credit_card = request.form.get('credit_card', type=str)
        car_number = request.form.get('car_number', type=str)

        client = Client(
            name=name,
            surname=surname,
            credit_card=credit_card,
            car_number=car_number
        )
        db.session.add(client)
        db.session.commit()
        return '', 201

    @app.route('/parkings', methods=['POST'])
    def create_parking():
        address = request.form.get('address', type=str)
        opened = request.form.get('opened', type=bool)
        count_places = request.form.get('count_places', type=int)
        count_available_places = request.form.get('count_available_places', type=int)

        parking = Parking(
            address=address,
            opened=opened,
            count_places=count_places,
            count_available_places=count_available_places
        )
        db.session.add(parking)
        db.session.commit()
        return '', 201

    @app.route('/client_parkings', methods=['POST'])
    def create_client_parking():
        client_id = request.form.get('client_id', type=int)
        parking_id = request.form.get('parking_id', type=int)
        time_in = datetime.datetime.now()

        parking: Parking = db.session.query(Parking).get(parking_id)

        if not parking.opened:
            return 'Parking is closed', 200

        if parking.count_available_places == 0:
            return 'Parking is full', 200

        client_parking = Client_Parking(
            client_id=client_id,
            parking_id=parking_id,
            time_in=time_in
        )
        parking.count_available_places -= 1
        db.session.add(client_parking)
        db.session.commit()
        return 'Successful parking', 201

    @app.route('/client_parkings', methods=['DELETE'])
    def delete_client_parking():
        client_id = request.form.get('client_id', type=int)
        parking_id = request.form.get('parking_id', type=int)
        time_out = datetime.datetime.now()

        parking: Parking = db.session.query(Parking).get(parking_id)
        client: Client = db.session.query(Client).get(client_id)
        client_parking: Client_Parking = db.session.query(Client_Parking).get(client_id)

        if not client.credit_card:
            return 'Make the payment!', 200

        parking.count_available_places += 1
        client_parking.time_out = time_out

        db.session.delete(client_parking)
        db.session.commit()
        return 'Have a good way!', 201

    return app
