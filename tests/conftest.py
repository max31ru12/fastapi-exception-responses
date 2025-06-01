from http import HTTPStatus
from typing import Callable

import pytest
from faker import Faker


@pytest.fixture(scope="session")
def faker():
    fake = Faker()
    yield fake


@pytest.fixture(scope="function")
def responses_args(faker: Faker) -> Callable:
    http_status_codes = [status.value for status in HTTPStatus]

    def _generate() -> tuple[str, int, str]:
        argname = "".join(faker.random_letters(10)).upper()
        code = faker.random_element(elements=http_status_codes)
        detail = faker.pystr(min_chars=10, max_chars=20)
        return argname, code, detail

    return _generate
