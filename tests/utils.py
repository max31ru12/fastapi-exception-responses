from typing import Any

import pytest

from fastapi_exception_responses.core import Responses


def prepare_arg_name(arg_name: str):
    return arg_name.replace("_", " ")


def assert_value_type(value: Any):
    responses_class = type("ResponsesClass", (Responses,), {"VALID_ARG_NAME": value})
    with pytest.raises(TypeError):
        responses_class.get_responses()


def assert_response_structure(
    responses: dict,
    code: int | str,
    arg_name: str,
    detail: str,
):
    prepared_name = prepare_arg_name(arg_name)
    prepared_name_lower = prepared_name.lower()

    if isinstance(code, str) and code.isdigit():
        code = int(code)

    examples = responses[code]["content"]["application/json"]["examples"]

    assert code in responses.keys()
    assert prepared_name_lower in examples.keys()
    assert prepared_name == examples[prepared_name_lower]["summary"]
    assert detail == examples[prepared_name_lower]["value"]["detail"]
    assert responses[code]["description"] == f"{code} status code description"


def get_responses(arg_dict: dict):
    return type("MultipleResponses", (Responses,), arg_dict).get_responses()
