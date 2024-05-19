import random

from faker import (
    Faker,
)
from pycountry import (
    countries,
)

__all__ = (
    "fake",
)


class Fake(Faker):

    def username(self) -> str:
        username = self.name()
        separator = random.choice([""])
        username = username.replace(" ", separator)
        return username

    def telegram_id(self) -> int:
        return random.randint(1, 2 ** 24 - 1)

    def bool(self) -> bool:
        return random.choice([True, False])

    def language_code(self):
        country = random.choice(list(countries))
        return country.alpha_2.lower()


fake = Fake()
