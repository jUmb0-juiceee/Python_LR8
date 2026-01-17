"""
Модуль для работы с API курсов валют Центробанка.
Содержит функцию get_currencies для получения текущих курсов.
"""

import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List


def create_logger() -> logging.Logger:
    """
    Создаёт логгер, записывающий всё в файл.

    Returns:
        Настроенный логгер.
    """
    logger_obj = logging.getLogger("file_logger")
    logger_obj.setLevel(logging.INFO)

    if logger_obj.handlers:
        return logger_obj

    handler = logging.FileHandler("app.log", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger_obj.addHandler(handler)
    return logger_obj


def reading_log(log: logging.Logger) -> None:
    """
    Выводит содержимое лог-файла.

    Args:
        log: логгер, внутри которого хранятся все записи.
    """
    with open("app.log", "r", encoding="utf-8") as f:
        content = f.read()
        print(content)


file_log = create_logger()


def logger(func=None, *, handle=None):
    """
    Декоратор для логирования вызовов функций.

    Args:
        func: декорируемая функция
        handle: обработчик логов

    Returns:
        Декорированная функция.
    """
    import functools

    if func is None:
        return lambda f: logger(f, handle=handle)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        if handle is not None:
            try:
                if hasattr(handle, "info"):
                    handle.info(f"Старт {func.__name__}, args={args}")
                else:
                    handle.write(f"INFO: Старт {func.__name__}, args={args}\n")
                result = func(*args, **kwargs)
                if hasattr(handle, "info"):
                    handle.info(f"Завершение {func.__name__}, результат={result}")
                else:
                    handle.write(f"INFO: Завершение {func.__name__}, результат={result}\n")
                return result
            except Exception as e:
                if hasattr(handle, "error"):
                    handle.error(f"{type(e).__name__}: {e}")
                else:
                    handle.write(f"ERROR: {type(e).__name__}: {e}\n")
                raise
        else:
            return func(*args, **kwargs)
    return inner


@logger(handle=file_log)
def get_currencies(
    currency_codes: List[str],
    url: str = 'https://www.cbr-xml-daily.ru/daily_json.js',
    handle=file_log
) -> Dict[str, float]:
    """
    Получает курсы валют от API Центробанка.

    Args:
        currency_codes: список кодов валют для получения курсов
        url: URL API Центробанка
        handle: логгер для записи событий

    Returns:
        Словарь, где ключи - коды валют, значения - курсы к рублю.

    Raises:
        TypeError: если курс валюты не числовой
        KeyError: если валюта не найдена в данных API
        ValueError: если получен некорректный JSON
        requests.exceptions.RequestException: при ошибках сети
    """
    handle.info(f'Начало работы функции get_currencies. Аргументы: currency_codes = {currency_codes}')
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        currencies = {}

        if "Valute" in data:
            for code in currency_codes:
                if code in data["Valute"]:
                    if not isinstance(data["Valute"][code]["Value"], (int, float)):
                        handle.error(f"Курс {code} не числовой")
                        reading_log(handle)
                        raise TypeError(f"Курс валюты '{code}' имеет неверный тип")
                    else:
                        currencies[code] = data["Valute"][code]["Value"]
                else:
                    handle.error(f"Валюты '{code}' нет в данных API")
                    reading_log(handle)
                    raise KeyError(f"Валюта '{code}' не найдена")

        else:
            handle.error("Ключ 'Valute' отсутствует в данных API")
            reading_log(handle)
            raise KeyError("Нет ключа 'Valute' в данных API")
        handle.info(f'Успешное завершение работы функции get_currencies. Результат: currencies = {currencies}')
        return currencies

    except ValueError as e:
        handle.error(f"Некорректный JSON: {e}")
        reading_log(handle)
        raise

    except requests.exceptions.ConnectionError as e:
        handle.error(f"Ошибка сети, API недоступен: {e}")
        reading_log(handle)
        raise

    except requests.exceptions.RequestException as e:
        handle.error(f"Ошибка при запросе API: {e}")
        reading_log(handle)
        raise

    except Exception as e:
        handle.error(f"Упали с исключением: {e}")
        reading_log(handle)
        raise


@logger(handle=file_log)
def get_currency_history(currency_code: str, days: int = 90) -> Dict[str, float]:
    """
    Получает исторические данные по валюте за указанное количество дней.

    Args:
        currency_code: Код валюты (например, 'USD')
        days: Количество дней истории (по умолчанию 90 дней ≈ 3 месяца)

    Returns:
        Словарь с датами в формате 'YYYY-MM-DD' и значениями курсов
    """
    file_log.info(f'Получение истории для {currency_code} за {days} дней')

    history = {}
    try:
        # Для демонстрации создадим тестовые данные
        # В реальном приложении здесь был бы запрос к API
        base_value = 90.0
        for day in range(days):
            date = (datetime.now() - timedelta(days=day)).strftime('%Y-%m-%d')
            # Имитация изменения курса
            import random
            change = random.uniform(-2, 2)
            history[date] = round(base_value + change * (day / 30), 4)

        file_log.info(f'Сгенерировано {len(history)} записей истории для {currency_code}')
        return history

    except Exception as e:
        file_log.error(f"Ошибка при получении истории для {currency_code}: {e}")
        raise


# Функция для тестирования (можно удалить в финальной версии)
def test_get_currencies() -> None:
    """
    Тестирует функцию get_currencies.
    """
    print("Тестирование функции get_currencies...")
    try:
        currency_list = ['USD', 'EUR', 'GBP']
        currency_data = get_currencies(currency_list)
        print(f"Полученные курсы: {currency_data}")
        print("Тест пройден успешно!")
    except Exception as e:
        print(f"Ошибка при тестировании: {e}")


if __name__ == '__main__':
    # Очищаем логгер для чистого теста
    open("app.log", "w", encoding="utf-8").close()
    test_get_currencies()