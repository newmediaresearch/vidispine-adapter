import pytest

from vidispine.utils import create_matrix_params_query


@pytest.mark.parametrize('matrix_params', [
    {'test1': 1, 'test2': 'foo', 'test3': 'bar'}, {'test': 'foo bar pizza'},
    {'test': ''}, {'': 'test'}, {}, None, {123: 456}
])
def test_create_matrix_params_query(matrix_params):
    result = create_matrix_params_query(matrix_params)

    if matrix_params:
        assert isinstance(result, str)
        assert result.count(';') == len(matrix_params)
        assert ' ' not in result
    else:
        assert result == matrix_params
