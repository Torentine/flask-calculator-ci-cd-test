import unittest
from app import app
from urllib.parse import quote

class FlaskAppTests(unittest.TestCase):
    
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.client.testing = True

    def test_home_page(self):
        """Тест главной страницы"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertIn('Привет, мир!', response_text)

    def test_user_page(self):
        """Тест страницы пользователя"""
        response = self.client.get('/user/testuser')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertIn('Hello, testuser', response_text)

    def test_post_page(self):
        """Тест страницы поста"""
        response = self.client.get('/post/123')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertIn('Это пост под номером: 123', response_text)

    def test_login_get(self):
        """Тест GET запроса для логина"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertIn('form method="post"', response_text)

    def test_login_post(self):
        """Тест POST запроса для логина"""
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertIn('Попытка входа: testuser', response_text)

    def test_calc_add(self):
        """Тест сложения в калькуляторе"""
        # Используем query_string вместо параметров в URL
        response = self.client.get('/calc', query_string={'a': 5, 'b': 3, 'operation': '+'})
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertEqual(response_text, "Результат: 8")

    def test_calc_sub(self):
        """Тест вычитания в калькуляторе"""
        response = self.client.get('/calc', query_string={'a': 10, 'b': 4, 'operation': '-'})
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertEqual(response_text, "Результат: 6")

    def test_calc_mul(self):
        """Тест умножения в калькуляторе"""
        response = self.client.get('/calc', query_string={'a': 3, 'b': 7, 'operation': '*'})
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertEqual(response_text, "Результат: 21")

    def test_calc_div(self):
        """Тест деления в калькуляторе"""
        response = self.client.get('/calc', query_string={'a': 15, 'b': 3, 'operation': '/'})
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertEqual(response_text, "Результат: 5")

    def test_calc_div_by_zero(self):
        """Тест деления на ноль"""
        response = self.client.get('/calc', query_string={'a': 5, 'b': 0, 'operation': '/'})
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertEqual(response_text, "Ошибка: деление на ноль")

    def test_calc_invalid_operation(self):
        """Тест неверной операции"""
        response = self.client.get('/calc', query_string={'a': 5, 'b': 3, 'operation': 'invalid'})
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertEqual(response_text, "Неверная операция")

    def test_calc_invalid_number(self):
        """Тест неверного формата числа"""
        response = self.client.get('/calc', query_string={'a': 'abc', 'b': 3, 'operation': '+'})
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertEqual(response_text, "Ошибка: неверный формат числа")

    def test_calc_default_values(self):
        """Тест калькулятора с значениями по умолчанию"""
        response = self.client.get('/calc')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertEqual(response_text, "Результат: 0")

    def test_calc_empty_params(self):
        """Тест калькулятора с пустыми параметрами"""
        response = self.client.get('/calc', query_string={'a': '', 'b': '', 'operation': '+'})
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertEqual(response_text, "Результат: 0")

    def test_calc_negative_numbers(self):
        """Тест калькулятора с отрицательными числами"""
        response = self.client.get('/calc', query_string={'a': -5, 'b': 3, 'operation': '+'})
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertEqual(response_text, "Результат: -2")

    def test_calc_float_numbers(self):
        """Тест калькулятора с дробными числами"""
        response = self.client.get('/calc', query_string={'a': 2.5, 'b': 1.5, 'operation': '+'})
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertEqual(response_text, "Результат: 4")

    def test_calc_float_division(self):
        """Тест деления с дробным результатом"""
        response = self.client.get('/calc', query_string={'a': 5, 'b': 2, 'operation': '/'})
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertEqual(response_text, "Результат: 2.5")

if __name__ == '__main__':
    unittest.main()