from email_validator import validate_email, EmailNotValidError, EmailSyntaxError
from flask import flash


def is_valid_email(email):
    """

    Validate an email address using the email_validator library.

    Args:
        email (str): The email address to be validated.

    Returns:
        bool: True if the email is valid, False otherwise.

    This function attempts to validate an email address using the email_validator library.
    If the email is valid, it returns True. If the email is not valid, it returns False
    and displays a flash message with an error description.

    Note that this function catches specific exceptions (EmailNotValidError and EmailSyntaxError)
    that can be raised during the validation process and provides error messages in the flash message.
    In the event of any other unexpected error, a general error message is displayed.

    """

    try:
        validate_email(email)
        return True

    except (EmailNotValidError, EmailSyntaxError) as e:
        flash(f"email error : {e}")
        return False

    except Exception:
        flash("- an unexpected error occurred -")
