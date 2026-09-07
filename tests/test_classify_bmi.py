from app import classify_bmi


# 測試案例：BMI 在 18.5 以下時，應分類為體重過輕。
# Arrange: 設定 BMI 為 18.4。
# Act: 呼叫 classify_bmi() 進行分類。
# Assert: 驗證回傳字串為 "You are underweight."。
def test_classify_bmi_returns_underweight_for_bmi_below_18_5():
    bmi = 18.4

    result = classify_bmi(bmi)

    assert result == "You are underweight."


# 測試案例：BMI 等於 18.5 時，應分類為健康體重。
# Arrange: 設定 BMI 為 18.5。
# Act: 呼叫 classify_bmi() 進行分類。
# Assert: 驗證回傳字串為 "You have a normal weight."。
def test_classify_bmi_returns_normal_for_bmi_exactly_18_5():
    bmi = 18.5

    result = classify_bmi(bmi)

    assert result == "You have a normal weight."


# 測試案例：BMI 在 18.5 到 24 之間時，應分類為健康體重。
# Arrange: 設定 BMI 為 22.0。
# Act: 呼叫 classify_bmi() 進行分類。
# Assert: 驗證回傳字串為 "You have a normal weight."。
def test_classify_bmi_returns_normal_for_bmi_between_18_5_and_24():
    bmi = 22.0

    result = classify_bmi(bmi)

    assert result == "You have a normal weight."


# 測試案例：BMI 等於 24 時，應分類為體重過重。
# Arrange: 設定 BMI 為 24.0。
# Act: 呼叫 classify_bmi() 進行分類。
# Assert: 驗證回傳字串為 "You are overweight."。
def test_classify_bmi_returns_overweight_for_bmi_exactly_24():
    bmi = 24.0

    result = classify_bmi(bmi)

    assert result == "You are overweight."


# 測試案例：BMI 在 24 到 27 之間時，應分類為體重過重。
# Arrange: 設定 BMI 為 25.5。
# Act: 呼叫 classify_bmi() 進行分類。
# Assert: 驗證回傳字串為 "You are overweight."。
def test_classify_bmi_returns_overweight_for_bmi_between_24_and_27():
    bmi = 25.5

    result = classify_bmi(bmi)

    assert result == "You are overweight."


# 測試案例：BMI 等於 27 時，應分類為肥胖。
# Arrange: 設定 BMI 為 27.0。
# Act: 呼叫 classify_bmi() 進行分類。
# Assert: 驗證回傳字串為 "You are obese."。
def test_classify_bmi_returns_obese_for_bmi_exactly_27():
    bmi = 27.0

    result = classify_bmi(bmi)

    assert result == "You are obese."


# 測試案例：BMI 大於 27 時，應分類為肥胖。
# Arrange: 設定 BMI 為 30.0。
# Act: 呼叫 classify_bmi() 進行分類。
# Assert: 驗證回傳字串為 "You are obese."。
def test_classify_bmi_returns_obese_for_bmi_above_27():
    bmi = 30.0

    result = classify_bmi(bmi)

    assert result == "You are obese."
