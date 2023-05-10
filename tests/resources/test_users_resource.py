import json

from nuBox.ext.database import User as UserModel

BASE_URL = '/api/v1'


def test_should_return_a_list_of_users(client):
    response = client.get(f"{BASE_URL}/users/")
    assert response.status_code == 200


def test_find_user(client, user):
    response = client.get(f"{BASE_URL}/user/{user.id}")
    data = json.loads(response.data.decode())

    created = data.pop('createdAt')
    updated = data.pop('updatedAt')

    data.pop('deletedAt')
    data.pop('deleted')

    expected = {
        'id': 1,
        'username': 'my_user'
    }

    user_founded = UserModel.query.filter_by(id=user.id).first()

    assert user_founded is not None
    assert data == expected
    assert created
    assert updated
