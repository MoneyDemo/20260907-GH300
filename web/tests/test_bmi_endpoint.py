import pytest

from web.server import app


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    return app.test_client()


# 測試案例：提供有效的體重與身高時，應回傳正確的 BMI 與分類。
# Arrange: 準備 154 磅、1.70 公尺的請求內容。
# Act: 呼叫 POST /api/bmi。
# Assert: 驗證回傳 200，且 BMI 與分類與 console 版計算結果一致。
def test_bmi_endpoint_returns_correct_result_for_valid_input(client):
    payload = {"weight": 154, "height": 1.70}

    response = client.post("/api/bmi", json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert data["bmi"] == pytest.approx(24.17, rel=1e-3)
    assert data["category"] == "over"
    assert data["label"] == "過重"


# 測試案例：BMI 略低於 18.5 時，應分類為過輕。
# Arrange: 選擇會產生 18.4 左右 BMI 的體重與身高。
# Act: 呼叫 POST /api/bmi。
# Assert: 驗證分類為 under。
def test_bmi_endpoint_classifies_underweight_below_threshold(client):
    payload = {"weight": 90, "height": 1.70}

    response = client.post("/api/bmi", json=payload)

    data = response.get_json()
    assert response.status_code == 200
    assert data["category"] == "under"


# 測試案例：BMI 等於 24（正常/過重邊界）時，應分類為過重。
# Arrange: 選擇會產生剛好 24.0（含極小誤差修正）BMI 的體重與身高。
# Act: 呼叫 POST /api/bmi。
# Assert: 驗證分類為 over（與 app.py 的 classify_bmi 邊界一致）。
def test_bmi_endpoint_classifies_boundary_bmi_24_as_overweight(client):
    height = 1.70
    # 磅轉公斤再除以身高平方會有浮點誤差，加極小 epsilon 避免落在邊界下方。
    weight_lb = (24.0 + 1e-6) * (height ** 2) / 0.453592
    payload = {"weight": weight_lb, "height": height}

    response = client.post("/api/bmi", json=payload)

    data = response.get_json()
    assert response.status_code == 200
    assert data["category"] == "over"


# 測試案例：BMI 等於 27（過重/肥胖邊界）時，應分類為肥胖。
# Arrange: 選擇會產生剛好 27.0（含極小誤差修正）BMI 的體重與身高。
# Act: 呼叫 POST /api/bmi。
# Assert: 驗證分類為 obese（與 app.py 的 classify_bmi 邊界一致）。
def test_bmi_endpoint_classifies_boundary_bmi_27_as_obese(client):
    height = 1.70
    weight_lb = (27.0 + 1e-6) * (height ** 2) / 0.453592
    payload = {"weight": weight_lb, "height": height}

    response = client.post("/api/bmi", json=payload)

    data = response.get_json()
    assert response.status_code == 200
    assert data["category"] == "obese"


# 測試案例：身高為 0 時，應回傳 400 錯誤，而不是讓伺服器拋出例外。
# Arrange: 準備身高為 0 的請求內容。
# Act: 呼叫 POST /api/bmi。
# Assert: 驗證回傳 400 並附帶錯誤訊息。
def test_bmi_endpoint_returns_400_when_height_is_zero(client):
    payload = {"weight": 154, "height": 0}

    response = client.post("/api/bmi", json=payload)

    assert response.status_code == 400
    assert "error" in response.get_json()


# 測試案例：缺少必要欄位時，應回傳 400 錯誤。
# Arrange: 準備只有體重、缺少身高的請求內容。
# Act: 呼叫 POST /api/bmi。
# Assert: 驗證回傳 400 並附帶錯誤訊息。
def test_bmi_endpoint_returns_400_when_height_field_missing(client):
    payload = {"weight": 154}

    response = client.post("/api/bmi", json=payload)

    assert response.status_code == 400
    assert "error" in response.get_json()


# 測試案例：欄位型別不是數字時，應回傳 400 錯誤。
# Arrange: 準備體重為非數字字串的請求內容。
# Act: 呼叫 POST /api/bmi。
# Assert: 驗證回傳 400 並附帶錯誤訊息。
def test_bmi_endpoint_returns_400_when_weight_is_not_a_number(client):
    payload = {"weight": "not-a-number", "height": 1.70}

    response = client.post("/api/bmi", json=payload)

    assert response.status_code == 400
    assert "error" in response.get_json()
