"""
Data-driven regression example: one test definition, multiple inputs from JSON.
This is the pattern to reuse for login/search/form-validation style scenarios tomorrow.
"""
import allure
import pytest

from framework.core.utils import load_json_data
from framework.pages.playwright_dev_home_page import PlaywrightDevHomePage

search_cases = load_json_data("search_terms.json")


@allure.feature("Web - Regression")
@pytest.mark.regression
@pytest.mark.web
@pytest.mark.parametrize("case", search_cases, ids=[c["search_term"] for c in search_cases])
def test_search_term_data_driven(page, case):
    home = PlaywrightDevHomePage(page).open()
    home.search(case["search_term"])
    result_text = home.first_result_text()
    assert case["expect_contains"].lower() in result_text.lower(), (
        f"Expected '{case['expect_contains']}' in first result, got '{result_text}'"
    )
