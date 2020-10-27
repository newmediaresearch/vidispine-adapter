import pytest

from vidispine.base import EntityBase


def test_init(test_client):
    base = EntityBase(test_client)

    assert base.client == test_client
    assert base.entity is ''


@pytest.mark.parametrize('endpoint,matrix_params,expected_result', [
    ('', None, 'entity'),

    ('endpoint', None, 'entity/endpoint'),
    ('endpoint/eggs', None, 'entity/endpoint/eggs'),
    ('endpoint/eggs/123', None, 'entity/endpoint/eggs/123'),

    ('', {'number': 100, 'first': 1}, 'entity;number=100;first=1'),
    (
        'endpoint',
        {'number': 100, 'first': 1},
        'entity/endpoint;number=100;first=1'
    ), (
        'endpoint/eggs',
        {'number': 100, 'first': 1},
        'entity/endpoint/eggs;number=100;first=1'
    ), (
        'endpoint/eggs/123',
        {'number': 100, 'first': 1},
        'entity/endpoint/eggs/123;number=100;first=1'
    ),
])
def test_build_url(test_client, endpoint, matrix_params, expected_result):
    base = EntityBase(test_client)
    base.entity = 'entity'

    result = base._build_url(endpoint, matrix_params)

    assert result == expected_result


def test_build_url_no_entity(test_client):
    base = EntityBase(test_client)

    with pytest.raises(NotImplementedError) as err:
        base._build_url()

    err.match('Do not use Base class directly')
