import pytest

@pytest.fixture(scope="session")
def browser_type_launch_options():
    return {
        "slo_mo": 1000
    }