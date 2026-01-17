"""
Модуль содержит класс UserCurrency для связи пользователей и валют.
"""


class UserCurrency:
    """
    Класс, представляющий связь пользователя с валютой (подписку).

    Attributes:
        _id (int): Уникальный идентификатор связи.
        _user_id (int): Идентификатор пользователя.
        _currency_id (int): Идентификатор валюты.
    """

    def __init__(self, link_id: int, user_id: int, currency_id: int) -> None:
        """
        Инициализирует объект UserCurrency.

        Args:
            link_id: Уникальный идентификатор связи.
            user_id: Идентификатор пользователя.
            currency_id: Идентификатор валюты.

        Raises:
            TypeError: Если аргументы имеют неверный тип.
            ValueError: Если аргументы недопустимы.
        """
        self._id = None
        self._user_id = None
        self._currency_id = None

        # Используем сеттеры для инициализации с проверками
        self.id = link_id
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def id(self) -> int:
        """
        Возвращает идентификатор связи.

        Returns:
            Идентификатор связи.
        """
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        """
        Устанавливает идентификатор связи.

        Args:
            value: Идентификатор связи.

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
    def user_id(self) -> int:
        """
        Возвращает идентификатор пользователя.

        Returns:
            Идентификатор пользователя.
        """
        return self._user_id

    @user_id.setter
    def user_id(self, value: int) -> None:
        """
        Устанавливает идентификатор пользователя.

        Args:
            value: Идентификатор пользователя.

        Raises:
            TypeError: Если value не является целым числом.
            ValueError: Если value отрицательный или нулевой.
        """
        if not isinstance(value, int):
            raise TypeError("ID пользователя должен быть целым числом")
        if value <= 0:
            raise ValueError("ID пользователя должен быть положительным числом")
        self._user_id = value

    @property
    def currency_id(self) -> int:
        """
        Возвращает идентификатор валюты.

        Returns:
            Идентификатор валюты.
        """
        return self._currency_id

    @currency_id.setter
    def currency_id(self, value: int) -> None:
        """
        Устанавливает идентификатор валюты.

        Args:
            value: Идентификатор валюты.

        Raises:
            TypeError: Если value не является целым числом.
            ValueError: Если value отрицательный или нулевой.
        """
        if not isinstance(value, int):
            raise TypeError("ID валюты должен быть целым числом")
        if value <= 0:
            raise ValueError("ID валюты должен быть положительным числом")
        self._currency_id = value

    def __str__(self) -> str:
        """
        Возвращает строковое представление связи.

        Returns:
            Строковое представление в формате: "Связь #: UserID → CurrencyID"
        """
        return f"Связь #{self.id}: User {self.user_id} → Currency {self.currency_id}"

    def __repr__(self) -> str:
        """
        Возвращает формальное строковое представление объекта.

        Returns:
            Формальное строковое представление.
        """
        return f"UserCurrency(id={self.id}, user_id={self.user_id}, currency_id={self.currency_id})"