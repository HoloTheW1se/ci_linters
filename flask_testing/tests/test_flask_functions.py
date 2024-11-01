import pytest
import json


@pytest.mark.parametrize("route", ["clients", "clients/1"])
def test_get_routes(client, route):
    """Тестирование получения статус кода 200 от всех GET-запросов"""
    response = client.get(route)
    assert response.status_code == 200


def test_create_client(client):
    """Тестирование создания клиента"""
    client_data = {"name": 'Alex', "surname": 'Vershinin', "car_number": 'B008AD', "credit_card": '1234123412341234'}
    response = client.post('/clients', data=client_data)
    assert response.status_code == 201


def test_create_parking(client):
    """Тестирование создания парковки"""
    parking_data = {"address": 'Oryol, st. Lermontova, 35', "opened": 1, "count_places": 10,
                    "count_available_places": 5}
    response = client.post('/parkings', data=parking_data)
    assert response.status_code == 201


@pytest.mark.parking
def test_create_client_parking(client):
    """Тестирование заезда на парковку"""
    client_parking_data = {"client_id": 2, "parking_id": 1}
    parking_data = client.get(f"/parkings/{client_parking_data['parking_id']}").json
    count_available_places_before_post = parking_data['count_available_places']

    assert parking_data['opened'] is True
    assert parking_data['count_available_places'] > 0

    response = client.post("/client_parkings", data=client_parking_data)
    parking_data = client.get(f"/parkings/{client_parking_data['parking_id']}").json
    count_available_places_after_post = parking_data['count_available_places']

    assert count_available_places_before_post > count_available_places_after_post
    assert response.status_code == 201


@pytest.mark.parking
def test_delete_client_parking(client):
    """Тестирование выезда с парковки"""
    client_parking_data = {'client_id': 1, 'parking_id': 1}
    # Получение данных о клиенте и парковке
    client_data = client.get(f"/clients/{str(client_parking_data['client_id'])}").json
    parking_data = client.get(f"/parkings/{str(client_parking_data['parking_id'])}").json

    count_available_places_before_post = parking_data['count_available_places']

    response = client.delete('/client_parkings', data=client_parking_data)

    parking_data = client.get(f"/parkings/{client_parking_data['parking_id']}").json
    count_available_places_after_post = parking_data['count_available_places']

    assert count_available_places_before_post < count_available_places_after_post
    assert client_data['credit_card']
    assert response.status_code == 201
