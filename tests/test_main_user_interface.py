from unittest.mock import patch
from src.main_user_interface import menu


def test_ensures_internal_methods_are_each_called_once():
    with patch("src.main_user_interface.enter_calories") as mock_enter_calories, patch(
        "builtins.input", side_effect = ["e", "x", "x", "y"]
    ):
        menu()
    
        assert mock_enter_calories.call_count == 1
