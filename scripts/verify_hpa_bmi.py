"""
Playwright 腳本：驗證 BMI console 程式與衛福部國健署官方 BMI 計算機的結果是否一致。

執行方式（務必使用 uv 環境執行）：
    uv run python scripts/verify_hpa_bmi.py

這支腳本會：
1. 針對四個體位分類（過輕、正常、過重、肥胖）各設計一個測試案例。
2. 使用 app.py 裡的 calculate_bmi() / classify_bmi() 計算本地結果。
3. 用 Playwright 開啟官方 BMI 計算機網頁，自動填入身高、體重、年齡並送出表單，
   取得官方網站計算出的 BMI 值與體位分類。
4. 印出兩邊結果的比對報告。
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

# 讓腳本可以在 scripts/ 目錄下執行時，仍能匯入位於專案根目錄的 app.py。
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import calculate_bmi, classify_bmi  # noqa: E402

HPA_URL = "https://www.hpa.gov.tw/Obesity/BmiCalculate.aspx"

# 每個體位分類各設計一個測試案例：(分類標籤, 體重公斤, 身高公分)。
# 官方網站以公斤/公分為輸入單位，因此直接使用公制數值，並在計算本地 BMI 時
# 轉換為 app.py 所需的磅與公尺。
TEST_CASES = [
    ("過輕 (underweight)", 50, 170),
    ("正常 (normal)", 65, 170),
    ("過重 (overweight)", 72, 170),
    ("肥胖 (obese)", 85, 170),
]

# 官方網站的年齡欄位是必填項目，選擇成人年齡以確保套用「成人健康體位標準」。
ADULT_AGE = "30"


def calculate_local_result(weight_kg, height_cm):
    """使用 app.py 的邏輯計算 BMI 與體位分類，回傳 (bmi, category)。"""
    weight_pounds = weight_kg / 0.453592
    height_meters = height_cm / 100
    bmi = calculate_bmi(weight_pounds, height_meters)
    category = classify_bmi(bmi)
    return bmi, category


def fetch_hpa_result(page, weight_kg, height_cm):
    """操作官方 BMI 計算機網頁，回傳 (bmi_text, category_text)。"""
    page.goto(HPA_URL)
    page.get_by_role("combobox", name="您的年齡：").select_option(ADULT_AGE)
    page.get_by_role("textbox", name="您的身高：").fill(str(height_cm))
    page.get_by_role("textbox", name="您的體重：").fill(str(weight_kg))
    page.get_by_role("button", name="送出").click()

    bmi_text = page.locator("text=BMI值：").inner_text()
    category_text = page.locator("text=「").first.inner_text()
    return bmi_text, category_text


def main():
    results = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()

        for label, weight_kg, height_cm in TEST_CASES:
            local_bmi, local_category = calculate_local_result(weight_kg, height_cm)
            hpa_bmi_text, hpa_category_text = fetch_hpa_result(page, weight_kg, height_cm)

            results.append(
                {
                    "label": label,
                    "weight_kg": weight_kg,
                    "height_cm": height_cm,
                    "local_bmi": local_bmi,
                    "local_category": local_category,
                    "hpa_bmi_text": hpa_bmi_text,
                    "hpa_category_text": hpa_category_text,
                }
            )

        browser.close()

    print(f"{'案例':<20}{'體重(kg)':<10}{'身高(cm)':<10}{'本地BMI':<10}{'官方BMI':<12}{'本地分類':<25}官方分類")
    for r in results:
        print(
            f"{r['label']:<20}{r['weight_kg']:<10}{r['height_cm']:<10}"
            f"{r['local_bmi']:<10.2f}{r['hpa_bmi_text']:<12}"
            f"{r['local_category']:<25}{r['hpa_category_text']}"
        )


if __name__ == "__main__":
    main()
