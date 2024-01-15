import time

from fastapi.testclient import TestClient

from module_api import app, process_sql_condition, Session, session, Base

client = TestClient(app)

#
def test_status_code():
    """
    Тут проверяю рабочая ли ссылка на api
    :return:
    """
    data = [
        {"audience1": '',
         "audience2": ''}
    ]

    response = client.post("/getPercent", json=data)
    assert response.status_code == 200


def test_api_work():

    """
    Тут проверяю правильность вычислений
    :return:
    """
    data = [
        {"audience1": 'data.age BETWEEN 18 AND 35',
         "audience2": 'data.sex = 1 AND data.age >= 18'}
    ]

    response = client.post("/getPercent", json=data)
    assert response.json() == {'percent': '1.96%'}


