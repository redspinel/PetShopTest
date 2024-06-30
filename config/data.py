class user_data:
    id: int = None
    username: str = None
    firstName: str = None
    lastName: str = None
    email: str = None
    password: str = None
    phone: str = None
    userStatus: int = None

user_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "username": {"type": "string"},
        "firstName": {"type": "string"},
        "lastName": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"},
        "phone": {"type": "string"},
        "userStatus": {"type": "integer"}
    },
    "required": ["id", "username", "firstName", "lastName", "email", "password", "phone", "userStatus"]
}

response_create_user_schema = {
    "type": "object",
    "properties": {
        "code": {"type": "integer"},
        "type": {"type": "string"},
        "message": {"type": "string"}
    },
    "required": ["code", "type", "message"]
}

expected_delete_user_response = {
    "code": 200,
    "type": "unknown",
    "message": "username_placeholder"
}

expected_login_success_response = {
    "code": 200,
    "type": "unknown",
    "message": "logged in user session:"
}

expected_login_error_response = {
    "code": 400,
    "type": "unknown",
    "message": "Invalid username/password supplied"
}

expected_logout_success_response = {
    "code": 200,
    "type": "unknown",
    "message": "ok"
}


expected_nonexistent_user_response = {
    "code": 1,
    "type": "error",
    "message": "User not found"
}

