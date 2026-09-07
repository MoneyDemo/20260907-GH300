import pytest

from web.server import app


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    return app.test_client()


# 測試案例：造訪首頁時，應回傳 200 並包含網站標題關鍵字。
# Arrange: 準備測試用的 Flask client。
# Act: 呼叫 GET /。
# Assert: 驗證回傳 200，且頁面內容包含「BMI 噗噗星球」。
def test_index_route_returns_200_with_expected_title(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "BMI 噗噗星球".encode("utf-8") in response.data
