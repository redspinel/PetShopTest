from pages.base_page import BasePage

class UserPage(BasePage):
    def create_user(self, user_data):
        return self.post("/user", data=user_data)

    def get_user(self, username):
        return self.get(f"/user/{username}")

    def update_user(self, username, user_data):
        return self.put(f"/user/{username}", data=user_data)

    def delete_user(self, username):
        return self.delete(f"/user/{username}")

    def login_user(self, username, password):
        params = {"username": username, "password": password}
        return self.get("/user/login", params=params)

    def logout_user(self):
        return self.get("/user/logout")

    def recover_password(self, email):
        return self.post("/user/recover-password", data={"email": email})

    def get_all_users(self):
        return self.get("/users")

    def create_users_with_array(self, users_data):
        return self.post("/user/createWithArray", data=users_data)

    def create_users_with_list(self, users_data):
        return self.post("/user/createWithList", data=users_data)
