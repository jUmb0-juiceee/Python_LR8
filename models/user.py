"""
Модуль содержит класс User для представления пользователя приложения.
"""


class User:
    """
    Класс, представляющий пользователя приложения.

    Attributes:
        _id (int): Уникальный идентификатор пользователя.
        _name (str): Имя пользователя.
    """

    def __init__(self, user_id: int, name: str) -> None:
        """
        Инициализирует объект User.

        Args:
            user_id: Уникальный идентификатор пользователя.
            name: Имя пользователя.

        Raises:
            TypeError: Если аргументы имеют неверный тип.
            ValueError: Если аргументы недопустимы.
        """
        self._id = None
        self._name = None

        # Используем сеттеры для инициализации с проверками
        self.id = user_id
        self.name = name

    @property
    def id(self) -> int:
        """
        Возвращает идентификатор пользователя.

        Returns:
            Идентификатор пользователя.
        """
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        """
        Устанавливает идентификатор пользователя.

        Args:
            value: Идентификатор пользователя.

        Raises:
            TypeError: Если value не является целым числом.
            ValueError: Если value отрицательный или нулевой.
        """
        if not isinstance(value, int):
            raise TypeError("ID должен быть целым числом")
        if value <= 0:
            raise ValueError("ID должен быть положительным числом")
        self._id = value

    @property
    def name(self) -> str:
        """
        Возвращает имя пользователя.

        Returns:
            Имя пользователя.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Устанавливает имя пользователя.

        Args:
            value: Имя пользователя.

        Raises:
            TypeError: Если value не является строкой.
            ValueError: Если value пустая строка.
        """
        if not isinstance(value, str):
            raise TypeError("Имя должно быть строкой")
        if not value.strip():
            raise ValueError("Имя не может быть пустым")
        self._name = value.strip()

    def __str__(self) -> str:
        """
        Возвращает строковое представление пользователя.

        Returns:
            Строковое представление в формате: "Имя (ID: #)"
        """
        return f"{self.name} (ID: {self.id})"

    def __repr__(self) -> str:
        """
        Возвращает формальное строковое представление объекта.

        Returns:
            Формальное строковое представление.
        """
        return f"User(id={self.id}, name='{self.name}')"