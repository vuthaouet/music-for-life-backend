from Model.models import *
import re

PATTERN = dict()
PATTERN['email'] = re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$")


def validate_email(email):
    if not PATTERN['email'].match(email):
        return False, 'Email contain invalid characters'
    return True,


def validate_new_email(email):
    v = validate_email(email)
    if not v[0]:
        return v
    if UserDetails.find_by_email(email):
        return False, 'Email already existed'
    return True,


def validate_existed_email(email):
    v = validate_email(email)
    if not v[0]:
        return v
    user_details = UserDetails.find_by_email(email)
    if not user_details:
        return False, 'Email does not exist'
    return True, user_details


def validate_new_user(username):
    if UserDetails.find_by_user_name(username):
        return False, 'User name already existed'
    return True,

def validate_book_id(book_id):
    # book_id = html.escape(book_id)
    book_details = BookDetails.find_by_id(book_id)
    if not book_details:
        return False, 'Book does not exist'
    return True, book_details

def refactor_name(last_name, first_name):
    last_name = last_name.strip()
    first_name = first_name.strip()
    full_name = (last_name + " " + first_name).split()
    full_name = [ x.capitalize() for x in full_name]
    full_name = " ".join(full_name)
    return full_name