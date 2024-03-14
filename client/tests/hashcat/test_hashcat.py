import pytest
from unittest.mock import Mock
from hashcat import Hashcat


@pytest.mark.parametrize(
    "property_name, test_value",
    [
        ("attack_mode", 3),
        ("backend_devices", [1, 2, 3]),
        ("benchmark", True),
        ("hash", "example_hash"),
        ("hash_mode", 100),
    ],
)
def test_hashcat_properties(property_name, test_value):
    mock_cat_instance = Mock()
    hashcat = Hashcat(mock_cat_instance)

    setattr(hashcat, property_name, test_value)
    setattr(mock_cat_instance, property_name, test_value)

    assert getattr(mock_cat_instance, property_name) == test_value

    assert getattr(hashcat, property_name) == test_value
