"""
Основной модуль клиент-серверного приложения Currency Tracker.
Реализует HTTP сервер с маршрутизацией и MVC архитектурой.
"""

import http.server
import socketserver
import urllib.parse
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from jinja2 import Environment, PackageLoader, select_autoescape

# Импорт моделей
from models import Author, App, User, Currency, UserCurrency
# Импорт функции для получения курсов валют
from utils.currencies_api import get_currencies


class CurrencyTrackerHandler(http.server.BaseHTTPRequestHandler):
    """
    Обработчик HTTP запросов для приложения Currency Tracker.

    Реализует маршрутизацию и обработку всех запросов приложения.
    """

    # Общие данные приложения (заглушки для демонстрации)
    _users: List[User] = [
        User(1, "Иван Иванов"),
        User(2, "Мария Петрова"),
        User(3, "Алексей Сидоров"),
        User(4, "Елена Кузнецова")
    ]

    _currencies: List[Currency] = [
        Currency(1, 840, "USD", "Доллар США", 90.50, 1),
        Currency(2, 978, "EUR", "Евро", 98.75, 1),
        Currency(3, 826, "GBP", "Фунт стерлингов", 115.20, 1),
        Currency(4, 392, "JPY", "Японская йена", 0.60, 100),
        Currency(5, 756, "CHF", "Швейцарский франк", 102.30, 1),
        Currency(6, 156, "CNY", "Китайский юань", 12.50, 1)
    ]

    _user_currencies: List[UserCurrency] = [
        UserCurrency(1, 1, 1),  # Иван → USD
        UserCurrency(2, 1, 2),  # Иван → EUR
        UserCurrency(3, 2, 2),  # Мария → EUR
        UserCurrency(4, 2, 3),  # Мария → GBP
        UserCurrency(5, 3, 4),  # Алексей → JPY
        UserCurrency(6, 4, 1),  # Елена → USD
        UserCurrency(7, 4, 2),  # Елена → EUR
        UserCurrency(8, 4, 5),  # Елена → CHF
    ]

    # Инициализация Jinja2 Environment (один раз при старте)
    env = Environment(
        loader=PackageLoader("myapp"),
        autoescape=select_autoescape()
    )

    def _render_template(self, template_name: str, context: Dict) -> bytes:
        """
        Рендерит Jinja2 шаблон с переданным контекстом.

        Args:
            template_name: Имя шаблона (без пути)
            context: Словарь с данными для шаблона

        Returns:
            Отрендеренный HTML в виде bytes
        """
        template = self.env.get_template(template_name)
        html_content = template.render(**context)
        return html_content.encode('utf-8')

    def _send_response(self, content: bytes, content_type: str = "text/html; charset=utf-8") -> None:
        """
        Отправляет HTTP ответ клиенту.

        Args:
            content: Содержимое ответа
            content_type: MIME-тип контента
        """
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _send_error(self, message: str, code: int = 404) -> None:
        """
        Отправляет страницу с ошибкой.

        Args:
            message: Сообщение об ошибке
            code: HTTP код ошибки
        """
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        error_html = f"""
        <html>
        <head><title>Ошибка {code}</title></head>
        <body>
            <h1>Ошибка {code}</h1>
            <p>{message}</p>
            <p><a href="/">Вернуться на главную</a></p>
        </body>
        </html>
        """
        self.wfile.write(error_html.encode('utf-8'))

    def _get_query_params(self) -> Dict[str, List[str]]:
        """
        Извлекает параметры запроса из URL.

        Returns:
            Словарь с параметрами запроса
        """
        query_string = urllib.parse.urlparse(self.path).query
        return urllib.parse.parse_qs(query_string)

    def _handle_static_file(self) -> None:
        """
        Обрабатывает запросы к статическим файлам.
        """
        try:
            # Убираем /static/ из пути
            file_path = self.path[8:]

            # Безопасность: запрещаем доступ к файлам вне папки static
            if '..' in file_path or file_path.startswith('/'):
                self._send_error("Доступ запрещен", 403)
                return

            full_path = f"static/{file_path}"

            # Проверяем существование файла
            if not os.path.exists(full_path):
                self._send_error("Файл не найден", 404)
                return

            # Определяем MIME-тип по расширению
            if full_path.endswith('.css'):
                mime_type = 'text/css'
            elif full_path.endswith('.js'):
                mime_type = 'application/javascript'
            elif full_path.endswith('.png'):
                mime_type = 'image/png'
            elif full_path.endswith('.jpg') or full_path.endswith('.jpeg'):
                mime_type = 'image/jpeg'
            elif full_path.endswith('.gif'):
                mime_type = 'image/gif'
            elif full_path.endswith('.ico'):
                mime_type = 'image/x-icon'
            elif full_path.endswith('.svg'):
                mime_type = 'image/svg+xml'
            else:
                mime_type = 'application/octet-stream'

            with open(full_path, 'rb') as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

        except Exception as e:
            self._send_error(f"Ошибка при чтении файла: {str(e)}", 500)

    def do_GET(self) -> None:
        """
        Обрабатывает GET запросы.

        Реализует маршрутизацию по self.path:
        - / : главная страница
        - /users : список пользователей
        - /user?id=... : информация о пользователе
        - /currencies : список валют
        - /author : информация об авторе
        - /static/... : статические файлы
        """
        path = urllib.parse.urlparse(self.path).path

        try:
            # Обработка статических файлов
            if path.startswith('/static/'):
                self._handle_static_file()
                return

            # Основная маршрутизация
            if path == "/":
                self._handle_index()
            elif path == "/users":
                self._handle_users()
            elif path == "/user":
                self._handle_user_detail()
            elif path == "/currencies":
                self._handle_currencies()
            elif path == "/author":
                self._handle_author()
            else:
                self._send_error("Страница не найдена", 404)

        except Exception as e:
            self._send_error(f"Внутренняя ошибка сервера: {str(e)}", 500)

    def _handle_index(self) -> None:
        """
        Обрабатывает запрос к главной странице.
        """
        # Создаем объекты для главной страницы
        author = Author("Синельников Никита", "P3122")
        app = App("Currency Tracker", "1.0.0", author)

        context = {
            "app_name": app.name,
            "app_version": app.version,
            "author_name": app.author.name,
            "author_group": app.author.group,
            "request_path": "/"
        }

        html_content = self._render_template("index.html", context)
        self._send_response(html_content)

    def _handle_users(self) -> None:
        """
        Обрабатывает запрос к списку пользователей.
        """
        # Добавляем информацию о количестве подписок для каждого пользователя
        users_with_subscriptions = []
        for user in self._users:
            subscription_count = sum(1 for uc in self._user_currencies if uc.user_id == user.id)
            users_with_subscriptions.append({
                "id": user.id,
                "name": user.name,
                "subscriptions_count": subscription_count
            })

        context = {
            "users": users_with_subscriptions,
            "request_path": "/users"
        }

        html_content = self._render_template("users.html", context)
        self._send_response(html_content)

    def _handle_user_detail(self) -> None:
        """
        Обрабатывает запрос к информации о конкретном пользователе.
        """
        params = self._get_query_params()
        user_id = params.get("id", [None])[0]

        if not user_id:
            self._send_error("Не указан ID пользователя")
            return

        try:
            user_id = int(user_id)
            user = next((u for u in self._users if u.id == user_id), None)

            if not user:
                self._send_error(f"Пользователь с ID {user_id} не найден")
                return

            # Находим валюты, на которые подписан пользователь
            currency_ids = [uc.currency_id for uc in self._user_currencies if uc.user_id == user_id]
            subscriptions = [c for c in self._currencies if c.id in currency_ids]

            # Добавляем вычисляемое поле для курса за единицу
            for currency in subscriptions:
                currency.value_per_unit = currency.get_value_per_unit()

            context = {
                "user": user,
                "subscriptions": subscriptions,
                "currencies_count": len(self._currencies),
                "request_path": "/users"
            }

            # Используем новый шаблон для детальной информации
            html_content = self._render_template("user_detail.html", context)
            self._send_response(html_content)

        except ValueError:
            self._send_error("Некорректный ID пользователя")
        except Exception as e:
            self._send_error(f"Ошибка при обработке запроса: {str(e)}")

    def _handle_currencies(self) -> None:
        """
        Обрабатывает запрос к списку валют.
        Пытается получить актуальные курсы через API.
        """
        try:
            # Пытаемся получить актуальные курсы через API
            currency_codes = [c.char_code for c in self._currencies]
            api_currencies = get_currencies(currency_codes)

            # Обновляем курсы в наших объектах Currency
            currencies_with_api_data = []
            for currency in self._currencies:
                if currency.char_code in api_currencies:
                    # Сохраняем старое значение для отображения изменения
                    old_value = currency.value
                    # Обновляем значение
                    currency.value = api_currencies[currency.char_code]
                    # Вычисляем изменение
                    change = currency.value - old_value if old_value else 0

                    currencies_with_api_data.append({
                        "id": currency.id,
                        "num_code": currency.num_code,
                        "char_code": currency.char_code,
                        "name": currency.name,
                        "value": currency.value,
                        "nominal": currency.nominal,
                        "value_per_unit": currency.get_value_per_unit(),
                        "change": change
                    })
                else:
                    # Если курс не получен из API, используем старый
                    currencies_with_api_data.append({
                        "id": currency.id,
                        "num_code": currency.num_code,
                        "char_code": currency.char_code,
                        "name": currency.name,
                        "value": currency.value,
                        "nominal": currency.nominal,
                        "value_per_unit": currency.get_value_per_unit(),
                        "change": 0
                    })

            context = {
                "currencies": currencies_with_api_data,
                "update_time": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                "request_path": "/currencies"
            }

            html_content = self._render_template("currencies.html", context)
            self._send_response(html_content)

        except Exception as e:
            # Если API не доступно, показываем статические данные
            print(f"Ошибка при получении курсов из API: {e}")

            currencies_with_data = []
            for currency in self._currencies:
                currencies_with_data.append({
                    "id": currency.id,
                    "num_code": currency.num_code,
                    "char_code": currency.char_code,
                    "name": currency.name,
                    "value": currency.value,
                    "nominal": currency.nominal,
                    "value_per_unit": currency.get_value_per_unit(),
                    "change": 0
                })

            context = {
                "currencies": currencies_with_data,
                "update_time": datetime.now().strftime("%d.%m.%Y %H:%M:%S") + " (статические данные)",
                "request_path": "/currencies"
            }

            html_content = self._render_template("currencies.html", context)
            self._send_response(html_content)

    def _handle_author(self) -> None:
        """
        Обрабатывает запрос к информации об авторе.
        """
        context = {
            "request_path": "/author"
        }

        html_content = self._render_template("author.html", context)
        self._send_response(html_content)

    def log_message(self, format: str, *args) -> None:
        """
        Переопределяем логирование для отключения стандартных логов.
        """
        # Можно раскомментировать для отладки
        # print(f"{self.address_string()} - {format % args}")
        pass


def run_server(port: int = 8000) -> None:
    """
    Запускает HTTP сервер на указанном порту.

    Args:
        port: Порт для запуска сервера
    """
    handler = CurrencyTrackerHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Сервер запущен на http://localhost:{port}")
        print("Доступные маршруты:")
        print("  /           - Главная страница")
        print("  /users      - Список пользователей")
        print("  /user?id=   - Информация о пользователе")
        print("  /currencies - Курсы валют")
        print("  /author     - Информация об авторе")
        print("  /static/    - Статические файлы (CSS, изображения)")
        print("\nНажмите Ctrl+C для остановки сервера")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nСервер остановлен")


if __name__ == "__main__":
    run_server(8000)