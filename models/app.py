"""
Модуль содержит класс App.
"""

from models.author import Author


class App:
    """
    Класс, представляющий приложение.

    Attributes:
        _name (str): Название приложения.
        _version (str): Версия приложения.
        _author (Author): Автор приложения.
    """

    def __init__(self, name: str, version: str, author: Author) -> None:
        """
        Инициализирует объект App.

        Args:
            name: Название приложения.
            version: Версия приложения.
            author: Автор приложения.

        Raises:
            TypeError: Если аргументы имеют неверный тип.
            ValueError: Если аргументы недопустимы.
        """
        self._name = None
        self._version = None
        self._author = None

        # Используем сеттеры для инициализации с проверками
        self.name = name
        self.version = version
        self.author = author

    @property
    def name(self) -> str:
        """
        Возвращает название приложения.

        Returns:
            Название приложения.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Устанавливает название приложения.

        Args:
            value: Название приложения.

        Raises:
            TypeError: Если value не является строкой.
            ValueError: Если value пустая строка.
        """
        if not isinstance(value, str):
            raise TypeError("Название приложения должно быть строкой")
        if not value.strip():
            raise ValueError("Название приложения не может быть пустым")
        self._name = value.strip()

    @property
    def version(self) -> str:
        """
        Возвращает версию приложения.

        Returns:
            Версия приложения.
        """
        return self._version

    @version.setter
    def version(self, value: str) -> None:
        """
        Устанавливает версию приложения.

        Args:
            value: Версия приложения.

        Raises:
            TypeError: Если value не является строкой.
            ValueError: Если value пустая строка.
        """
        if not isinstance(value, str):
            raise TypeError("Версия должна быть строкой")
        if not value.strip():
            raise ValueError("Версия не может быть пустой")
        self._version = value.strip()

    @property
    def author(self) -> Author:
        """
        Возвращает автора приложения.

        Returns:
            Автор приложения.
        """
        return self._author

    @author.setter
    def author(self, value: Author) -> None:
        """
        Устанавливает автора приложения.

        Args:
            value: Автор приложения.

        Raises:
            TypeError: Если value не является объектом Author.
        """
        if not isinstance(value, Author):
            raise TypeError("Автор должен быть объектом класса Author")
        self._author = value

    def __str__(self) -> str:
        """
        Возвращает строковое представление приложения.

        Returns:
            Строковое представление в формате: "Название (Версия)"
        """
        return f"{self.name} v{self.version}"

    def __repr__(self) -> str:
        """
        Возвращает формальное строковое представление объекта.

        Returns:
            Формальное строковое представление.
        """
        return f"App(name='{self.name}', version='{self.version}', author={repr(self.author)})"
