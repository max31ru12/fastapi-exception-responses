from typing import Callable, Any

from src.fastapi_responses.core import Responses



# ARGNAME.replace("_", " ")

# {154: {
#   'description': ARGNAME,
#   'content': {
#       'application/json': {
#           'examples': {
#               ARGNAME in lowercase: {
#                   'summary': ARGNAME uppercase, 'value': {
#                       'detail': DETAIL
#                       }
#                   }
#               }
#           }
#       }
#    }
# }

from tests.utils import assert_value_type, assert_response_structure


def test_single_response(responses_args: Callable):
    arg_name, code, detail = responses_args()

    single_responses_class = type("SingleResponses", (Responses,), {arg_name: (code, detail)})
    responses = single_responses_class.get_responses()

    assert_response_structure(responses, code, arg_name, detail)


def test_multiple_responses(responses_args: Callable):
    argname1, code1, detail1 = responses_args()
    argname2, code2, detail2 = responses_args()

    multiple_responses_class = type("MultipleResponses", (Responses,), {
        argname1: (code1, detail1),
        argname2: (code2, detail2),
    })

    responses = multiple_responses_class.get_responses()

    assert_response_structure(responses, code1, argname1, detail1)
    assert_response_structure(responses, code2, argname2, detail2)


def test_multiple_detail(responses_args):
    argname1, code1, detail1 = responses_args()
    argname2, _, detail2 = responses_args()

    multiple_responses_class = type("MultipleResponses", (Responses,), {
        argname1: (code1, detail1),
        argname2: (code1, detail2),
    })

    responses = multiple_responses_class.get_responses()

    print(responses)

    assert_response_structure(responses, code1, argname1, detail1)




def test_invalid_attr_name(responses_args):
    argname, code, detail = responses_args()

    argname1 = f"__{argname}__"
    argname2 = f"_{argname}"
    argname3 = f"__{argname}"

    responses_class = type("ResponsesClass", (Responses,), {
        argname1: (code, detail),
        argname2: (code, detail),
        argname3: (code, detail),
    })

    assert responses_class.get_responses() == {}


def test_callable_attr(responses_args):
    argname, code, _ = responses_args()

    def mock_func():
        pass

    responses_class = type("ResponsesClass", (Responses,), {argname: mock_func})

    assert responses_class.get_responses() == {}


def test_invalid_code_type(faker):
    assert_value_type(faker.pystr())
    assert_value_type(faker.pyint())
    assert_value_type(faker.pybool())
    assert_value_type(faker.pydict())
    assert_value_type(faker.pyset())
    assert_value_type(faker.pyfloat())
    assert_value_type(faker.pyobject())
    assert_value_type(faker.pylist(nb_elements=2))





