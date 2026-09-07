import pytest

from app import calculate_bmi


# 測試案例：當體重為 0 公斤時，BMI 應為 0。
# Arrange: 設定體重為 0，身高為 1.7 公尺。
# Act: 呼叫 calculate_bmi() 進行計算。
# Assert: 驗證結果等於 0.0。
def test_calculate_bmi_for_zero_weight_returns_zero():
    weight_pounds = 0
    height_meters = 1.7

    result = calculate_bmi(weight_pounds, height_meters)

    assert result == 0.0


# 測試案例：標準情境下，BMI 應符合公式計算結果。
# Arrange: 設定體重為 154 磅，身高為 1.7 公尺。
# Act: 呼叫 calculate_bmi() 進行計算。
# Assert: 驗證結果約等於 24.17。
def test_calculate_bmi_for_standard_case_matches_expected_value():
    weight_pounds = 154
    height_meters = 1.7

    result = calculate_bmi(weight_pounds, height_meters)

    assert result == pytest.approx(24.17, rel=1e-3)


# 測試案例：當體重與身高都取最小正數時，BMI 應由轉換公式正確計算。
# Arrange: 設定體重為 1 磅，身高為 1 公尺。
# Act: 呼叫 calculate_bmi() 進行計算。
# Assert: 驗證結果約等於 0.453592。
def test_calculate_bmi_for_minimum_positive_height_and_weight():
    weight_pounds = 1
    height_meters = 1

    result = calculate_bmi(weight_pounds, height_meters)

    assert result == pytest.approx(0.453592, rel=1e-6)


# 測試案例：當體重較重且身高中等時，BMI 應隨著體重增加而變大。
# Arrange: 設定體重為 220 磅，身高為 1.6 公尺。
# Act: 呼叫 calculate_bmi() 進行計算。
# Assert: 驗證結果約等於 38.98。
def test_calculate_bmi_for_large_weight_returns_large_bmi():
    weight_pounds = 220
    height_meters = 1.6

    result = calculate_bmi(weight_pounds, height_meters)

    assert result == pytest.approx(38.98, rel=1e-3)


# 測試案例：若身高為 0，BMI 計算必須拋出 ZeroDivisionError。
# Arrange: 設定體重為 70 磅，身高為 0 公尺。
# Act: 呼叫 calculate_bmi() 進行計算。
# Assert: 驗證會拋出 ZeroDivisionError。
def test_calculate_bmi_raises_zero_division_error_when_height_is_zero():
    weight_pounds = 70
    height_meters = 0

    with pytest.raises(ZeroDivisionError):
        calculate_bmi(weight_pounds, height_meters)
