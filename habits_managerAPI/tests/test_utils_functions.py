import pytest
from habits_managerAPI.utils import get_pks_to_delete

def test_getting_pks_to_delete():
    instance_pks = [
        {'id': 1},
        {'id': 2},
        {'id': 3},
        {'id': 4},
    ]
    updated_pk = [
        {'id': 3},
        {'id': 4},
        {'name': 'hello'},
    ]
    response = get_pks_to_delete(instance_pks, updated_pk)
    answer = set((1, 2))
    assert set(response).symmetric_difference(answer) == set()
