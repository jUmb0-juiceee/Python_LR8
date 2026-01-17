"""
Модуль содержит класс Currency для представления валюты.
"""


class Currency:
    """
    Класс, представляющий валюту.

    Attributes:
        _id (int): Уникальный идентификатор валюты.
        _num_code (int): Цифровой код валюты.
        _char_code (str): Символьный код валюты.
        _name (str): Название валюты.
        _value (float): Курс валюты к рублю.
        _nominal (int): Номинал (за сколько единиц указан курс).
    """

    def __init__(
            self,
            currency_id: int,
            num_code: int,
            char_code: str,
            name: str,
            value: float,
            nominal: int
    ) -> None:
        """
        Инициализирует объект Currency.

        Args:
            currency_id: Уникальный идентификатор валюты.
            num_code: Цифровой код валюты.
            char_code: Символьный код валюты.
            name: Название валюты.
            value: Курс валюты к рублю.
            nominal: Номинал валюты.

        Raises:
            TypeError: Если аргументы имеют неверный тип.
            ValueError: Если аргументы недопустимы.
        """
        self._id = None
        self._num_code = None
        self._char_code = None
        self._name = None
        self._value = None
        self._nominal = None

        # Используем сеттеры для инициализации с проверками
        self.id = currency_id
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal

    @property
    def id(self) -> int:
        """
        Возвращает идентификатор валюты.

        Returns:
            Идентификатор валюты.
        """
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        """
        Устанавливает идентификатор валюты.

        Args:
            value: Идентификатор валюты.

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
    def num_code(self) -> int:
        """
        Возвращает цифровой код валюты.

        Returns:
            Цифровой код валюты.
        """
        return self._num_code

    @num_code.setter
    def num_code(self, value: int) -> None:
        """
        Устанавливает цифровой код валюты.

        Args:
            value: Цифровой код валюты.

        Raises:
            TypeError: Если value не является целым числом.
            ValueError: Если value отрицательный или нулевой.
        """
        if not isinstance(value, int):
            raise TypeError("Цифровой код должен быть целым числом")
        if value <= 0:
            raise ValueError("Цифровой код должен быть положительным числом")
        self._num_code = value

    @property
    def char_code(self) -> str:
        """
        Возвращает символьный код валюты.

        Returns:
            Символьный код валюты.
        """
        return self._char_code

    @char_code.setter
    def char_code(self, value: str) -> None:
        """
        Устанавливает символьный код валюты.

        Args:
            value: Символьный код валюты.

        Raises:
            TypeError: Если value не является строкой.
            ValueError: Если value пустая или имеет неверную длину.
        """
        if not isinstance(value, str):
            raise TypeError("Символьный код должен быть строкой")
        if not value.strip():
            raise ValueError("Символьный код не может быть пустым")
        if len(value.strip()) != 3:
            raise ValueError("Символьный код должен состоять из 3 символов")
        self._char_code = value.strip().upper()

    @property
    def name(self) -> str:
        """
        Возвращает название валюты.

        Returns:
            Название валюты.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Устанавливает название валюты.

        Args:
            value: Название валюты.

        Raises:
            TypeError: Если value не является строкой.
            ValueError: Если value пустая строка.
        """
        if not isinstance(value, str):
            raise TypeError("Название должно быть строкой")
        if not value.strip():
            raise ValueError("Название не может быть пустым")
        self._name = value.strip()

    @property
    def value(self) -> float:
        """
        Возвращает курс валюты.

        Returns:
            Курс валюты к рублю.
        """
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        """
        Устанавливает курс валюты.

        Args:
            value: Курс валюты к рублю.

        Raises:
            TypeError: Если value не является числом.
            ValueError: Если value отрицательный или нулевой.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Курс должен быть числом")
        if value <= 0:
            raise ValueError("Курс должен быть положительным числом")
        self._value = float(value)

    @property
    def nominal(self) -> int:
        """
        Возвращает номинал валюты.

        Returns:
            Номинал валюты.
        """
        return self._nominal

    @nominal.setter
    def nominal(self, value: int) -> None:
        """
        Устанавливает номинал валюты.

        Args:
            value: Номинал валюты.

        Raises:
            TypeError: Если value не является целым числом.
            ValueError: Если value отрицательный или нулевой.
        """
        if not isinstance(value, int):
            raise TypeError("Номинал должен быть целым числом")
        if value <= 0:
            raise ValueError("Номинал должен быть положительным числом")
        self._nominal = value

    def get_value_per_unit(self) -> float:
        """
        Рассчитывает курс за одну единицу валюты.

        Returns:
            Курс за одну единицу валюты.
        """
        return self.value / self.nominal

    def __str__(self) -> str:
        """
        Возвращает строковое представление валюты.

        Returns:
            Строковое представление в формате: "Название (Код)"
        """
        return f"{self.name} ({self.char_code})"

    def __repr__(self) -> str:
        """
        Возвращает формальное строковое представление объекта.

        Returns:
            Формальное строковое представление.
        """
        return (f"Currency(id={self.id}, num_code={self.num_code}, "
                f"char_code='{self.char_code}', name='{self.name}', "
                f"value={self.value}, nominal={self.nominal})")