# 用於驗證使用者輸入資料格式是否正確
import re

class Validator:
    def __init__(self):
        self._errors = []
    
    def required(self, params):
        error_list = [p for p in params if p is None or p == ""]
        if len(error_list) > 0:
            self._errors.append("Missing required fields")
    
    def check_email(self, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self._errors.append("Invalid email format")

    def check_password(self, password):
        # 長度>6、英+符號組成
        if password is None or len(password) < 6 or not any(not char.isalnum() for char in password) or not any(char.isalpha() for char in password):
            self._errors.append("Invalid password format")

    def get_errors(self):
        return self._errors