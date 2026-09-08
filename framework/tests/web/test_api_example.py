"""
API-level example - useful for Bug Quest backend validation and fast test-data setup.
"""
import allure
import pytest

from framework.core.api_client import ApiClient


@allure.feature("API - Smoke")
@pytest.mark.smoke
@pytest.mark.api
def test_get_single_post_returns_expected_shape():
    client = ApiClient()
    response = client.get("/posts/1")
    assert response.status_code == 200
    body = response.json()
    assert set(["userId", "id", "title", "body"]).issubset(body.keys())


@allure.feature("API - Regression")
@pytest.mark.regression
@pytest.mark.api
def test_create_post_returns_201():
    client = ApiClient()
    response = client.post("/posts", json={"title": "foo", "body": "bar", "userId": 1})
    assert response.status_code == 201
    assert response.json()["title"] == "foo"
