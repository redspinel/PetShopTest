from faker import Faker
import random
import string
from config.data import user_data

fake = Faker('ru_RU')

def generate_id():
    return random.randint(1, 100)

def generate_username():
    return fake.user_name()

def generate_firstname():
    return fake.first_name()

def generate_lastname():
    return fake.last_name()

def generate_email():
    return fake.safe_email()

def generate_password():
    return fake.password()

def generate_phone():
    return "+7922964" + ''.join(random.choices(string.digits, k=4))

def generate_userstatus():
    return random.randint(0, 100)

def generate_user_data():
    user = user_data()
    user.id = generate_id()
    user.username = generate_username()
    user.firstName = generate_firstname()
    user.lastName = generate_lastname()
    user.email = generate_email()
    user.password = generate_password()
    user.phone = generate_phone()
    user.userStatus = generate_userstatus()
    return user