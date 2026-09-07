# BMI 計算器：依照成人健康體位標準，將體重與身高轉換為 BMI，
# 並判斷目前體位分類。這份程式以單一檔案維持簡潔結構，
# 方便後續進行單元測試與維護。

# BMI 分類門檻：依衛生福利部國民健康署成人健康體位標準定義。
UNDERWEIGHT_THRESHOLD = 18.5
NORMAL_WEIGHT_THRESHOLD = 24.0
OVERWEIGHT_THRESHOLD = 27.0

# 1 磅約等於 0.453592 公斤，用於將英制重量轉換為公制。
POUNDS_TO_KILOGRAMS = 0.453592


def calculate_bmi(weight_pounds, height_meters):
    """將英制體重轉換為公斤，並計算 BMI。"""
    weight_kg = weight_pounds * POUNDS_TO_KILOGRAMS
    return weight_kg / (height_meters ** 2)


def classify_bmi(bmi):
    """根據 BMI 值回傳對應的體位分類說明。"""
    if bmi < UNDERWEIGHT_THRESHOLD:
        return "You are underweight."
    if bmi < NORMAL_WEIGHT_THRESHOLD:
        return "You have a normal weight."
    if bmi < OVERWEIGHT_THRESHOLD:
        return "You are overweight."
    return "You are obese."


def bmi_calculator():
    """從使用者讀取體重與身高，計算 BMI 並顯示結果。"""
    weight = float(input("Enter your weight in pounds: "))
    height = float(input("Enter your height in meters: "))

    bmi = calculate_bmi(weight, height)
    category = classify_bmi(bmi)

    print(f"Your BMI is: {bmi:.2f}")
    print(category)


# 程式進入點：只有在直接執行此檔案時才會啟動主流程。
if __name__ == "__main__":
    bmi_calculator()