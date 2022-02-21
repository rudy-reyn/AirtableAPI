# 02/12/22
# datatypes.py
import io
from datetime import time

class AirtableBaseNumber:
    """Maps Python numeric types to numeric Airtable fields

    Autonumber: int
    Count:      int
    Currency:   float
    Number:     int | float
    Percent:    float, n >= 0
    Rating:     int, 0 < n <= 10
    """
    def __init__(self, num, format: type, allow_negative: bool=True):
        self.format = format
        if format not in (int, float):
            raise TypeError(f"""Numeric format must be either an integer or float.
            Got: '{type(format)}'""")
        self.allow_negative = allow_negative
        self.number = num

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, num: int | float):
        if self.format(num) != num:
            raise TypeError("Invalid value format.")
        if not self.allow_negative and num < 0:
            raise ValueError("Negative number provided but not is allowed.")
        self._number = self.format(num)

class Autonumber:
    pass

class Count(AirtableBaseNumber):
    def __init__(self, num):
        super().__init__(num, int, allow_negative=False)

class Currency(AirtableBaseNumber):
    def __init__(self, num, symbol="$", **kwargs):
        super().__init__(num, float, allow_negative=allow_negative)
        if not isinstance(symbol, str):
            raise TypeError("'symbol' must be a string")
        self.symbol = symbol

    def __str__(self):
        return f"{self.symbol}{self.number}"

class Number(AirtableBaseNumber):
    pass

class Percent(AirtableBaseNumber):
    def __repr__(self):
        return f"{self.number}"

    def __str__(self):
        return f"{self.number:%}"

class Duration:
    duration_formats = "h:mm", "h:mm:ss", "h:mm:ss.s", "h:mm:ss.ss", "h:mm:ss.sss"

    def __init__(self, duration: int | float, duration_format: str="h:mm"):
        raise NotImplementedError("Full support does not yet exist")
        if duration_format not in self.duration_formats:
            raise ValueError(f"Invalid duration_format, must be one of:\n{self.duration_formats}")
        self.duration_format: str = duration_format
        self.duration: int | float = duration

    def __repr__(self):
        # TODO
        hours, remainder = divmod(self.duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        match self.duration_format:
            case "h:mm":
                return f"{hours}:{minutes}"
            case _:
                precision = len(self.duration_format.partition(".")[-1])
                print(precision)
                return f"{hours}:{minutes}:{seconds}"

class Rating:
    """Airtable ratings are integers between 1 and another integer between 1 and 10."""
    def __init__(self, rating: int, limit: int=5):
        self.limit = limit
        self.rating = rating

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, lim: int):
        if not isinstance(lim, int):
            raise TypeError("'limit' must be an integer between 1 and 10.")
        if not 0 < lim <= 10:
            raise ValueError("'limit' must be an integer between 1 and 10.")
        self._limit: int = lim

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, rating: int):
        if not isinstance(rating, int):
            raise TypeError("'rating' must be an integer between 1 and {self.limit}.")
        if not 1 <= rating <= self.limit:
            raise ValueError(f"'rating' must be an integer between 1 and {self.limit}, got: '{rating}'")
        self._rating = rating

    def __repr__(self):
        return f"{self.rating}"

class Attachment:
    """Maps Python file objects to Airtable Attachment fields."""
    def __init__(self):
        return
