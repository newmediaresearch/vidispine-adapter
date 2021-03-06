import pytest

from vidispine.utils import create_matrix_params_string


@pytest.mark.parametrize('matrix_params,expected_output', [
    (
        {'test1': 1, 'test2': 'foo', 'test3': 'bar'},
        ';test1=1;test2=foo;test3=bar'
    ),
    ({'test': 'foo bar pizza'}, ';test=foo%20bar%20pizza'),
    ({'test': ''}, ';test='),
    ({'': 'test'}, ';=test'),
    ({123: 456}, ';123=456')
])
def test_create_matrix_params_string(matrix_params, expected_output):
    result = create_matrix_params_string(matrix_params)

    assert result == expected_output


def test_create_matrix_params_string_empty_params():
    result = create_matrix_params_string({})

    assert result == ''
