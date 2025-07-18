from energy_manager.helpers import getDate


def test_date():
    assert getDate().year == 2025
