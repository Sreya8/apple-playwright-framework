import pytest

@pytest.fixture(scope="session")
def browser_type_launch_options():
    return {
        # "slow_mo": 1000,
        "headless": False
    }