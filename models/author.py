"""
Модуль содержит класс Author для представления автора приложения.
"""


class Author:
    """
    Класс, представляющий автора приложения.

    Attributes:
        _name (str): Имя автора.
        _group (str): Учебная группа автора.
    """

    def __init__(self, name: str, group: str) -> None:
        """
        Инициализирует объект Author.

        Args:
            name: Имя автора.
            group: Учебная группа автора.

        Raises:
            TypeError: Если name или group не являются строками.
            ValueError: Если name или group пустые.
        """
        self._name = None
        self._group = None

        # Используем сеттеры для инициализации с проверками
        self.name = name
        self.group = group

    @property
    def name(self) -> str:
        """
        Возвращает имя автора.

        Returns:
            Имя автора.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Устанавливает имя автора.

        Args:
            value: Имя автора.

        Raises:
            TypeError: Если value не является строкой.
            ValueError: Если value пустая строка.
        """
        if not isinstance(value, str):
            raise TypeError("Имя должно быть строкой")
        if not value.strip():
            raise ValueError("Имя не может быть пустым")
        self._name = value.strip()

    @property
    def group(self) -> str:
        """
        Возвращает учебную группу автора.

        Returns:
            Учебная группа автора.
        """
        return self._group

    @group.setter
    def group(self, value: str) -> None:
        """
        Устанавливает учебную группу автора.

        Args:
            value: Учебная группа автора.

        Raises:
            TypeError: Если value не является строкой.
            ValueError: Если value пустая строка.
        """
        if not isinstance(value, str):
            raise TypeError("Группа должна быть строкой")
        if not value.strip():
            raise ValueError("Группа не может быть пустой")
        self._group = value.strip()

    def __str__(self) -> str:
        """
        Возвращает строковое представление автора.

        Returns:
            Строковое представление в формате: "Имя (Группа)"
        """
        return f"{self.name} ({self.group})"

    def __repr__(self) -> str:
        """
        Возвращает формальное строковое представление объекта.

        Returns:
            Формальное строковое представление.
        """
        return f"Author(name='{self.name}', group='{self.group}')"