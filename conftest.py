import pytest
import os


@pytest.fixture(scope="session")
def browser_type_launch_options():
    return {
        "slow_mo": 0,
        "headless": True
    }


@pytest.fixture(autouse=True)
def create_directories():
    """Create required directories if they don't exist"""
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("reports", exist_ok=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Automatically takes a screenshot when any test fails.
    Attaches it to the HTML report.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            test_name = item.nodeid.replace("/", "_").replace("::", "_")
            screenshot_path = f"screenshots/FAILED_{test_name}.png"
            page.screenshot(path=screenshot_path)

            # This line embeds the screenshot IN the HTML report
            if hasattr(report, "extra"):
                from pytest_html import extras
                report.extra = [extras.image(screenshot_path)]