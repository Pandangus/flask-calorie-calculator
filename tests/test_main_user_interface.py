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


def test_manually_enter_calories_is_called_once():
    with patch("src.main_user_interface.manually_enter_calories") as mock_manually_enter_calories, patch(
        "builtins.input", side_effect=["m"]
    ):
        menu()
        assert mock_manually_enter_calories.call_count == 1

    
def test_delete_calories_is_called_once():
    with patch("src.main_user_interface.delete_calories") as mock_delete_calories, patch(
        "builtins.input", side_effect=["d"]
    ):
        menu()
        assert mock_delete_calories.call_count == 1


def test_list_total_calories_is_called_once():
    with patch("src.main_user_interface.list_total_calories") as mock_list_total_calories, patch(
        "builtins.input", side_effect=["l"]
    ):
        menu()
        assert mock_list_total_calories.call_count == 1


def test_portion_calories_is_called_once():
    with patch("src.main_user_interface.portion_calories") as mock_portion_calories, patch(
        "builtins.input", side_effect=["p"]
    ):
        menu()
        assert mock_portion_calories.call_count == 1


def test_load_calories_is_called_once():
    with patch("src.main_user_interface.load_calories") as mock_load_calories, patch(
        "builtins.input", side_effect=["o"]
    ):
        menu()
        assert mock_load_calories.call_count == 1


def test_save_calories_is_called_once():
    with patch("src.main_user_interface.save_calories") as mock_save_calories, patch(
        "builtins.input", side_effect=["s"]
    ):
        menu()
        assert mock_save_calories.call_count == 1