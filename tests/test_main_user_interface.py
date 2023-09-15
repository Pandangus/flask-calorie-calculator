from unittest.mock import patch
from src.main_user_interface import menu


def test_exit_is_called_once():
    with patch("src.main_user_interface.exit") as mock_exit, patch(
        "builtins.input", side_effect=["x"]
    ):
        menu()
        assert mock_exit.call_count == 1


def test_enter_calories_is_called_once():
    with patch("src.main_user_interface.enter_calories") as mock_enter_calories, patch(
        "builtins.input", side_effect=["e"]
    ):
        menu()
        assert mock_enter_calories.call_count == 1
