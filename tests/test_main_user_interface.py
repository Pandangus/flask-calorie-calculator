from unittest.mock import patch
from src.main_user_interface import menu


def test_enter_calories_is_called_once():
    with patch("src.main_user_interface.enter_calories") as mock_enter_calories, patch(
        "builtins.input", side_effect = ["e", "x", "y"]
    ):
        menu()
        assert mock_enter_calories.call_count == 1
