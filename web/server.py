"""Flask 後端：GET / 顯示 BMI 噗噗星球網頁，POST /api/bmi 執行計算與分類。
計算邏輯直接重用根目錄 app.py 的 calculate_bmi/classify_bmi，做為唯一計算來源。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import calculate_bmi, classify_bmi  # noqa: E402  # 需先調整 sys.path 才能匯入

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# app.py 的 classify_bmi() 回傳完整英文句子，這裡對應成前端要用的分類鍵與中文標籤。
CATEGORY_MAP = {
    "You are underweight.": ("under", "過輕"),
    "You have a normal weight.": ("normal", "正常"),
    "You are overweight.": ("over", "過重"),
    "You are obese.": ("obese", "肥胖"),
}


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/bmi")
def bmi():
    payload = request.get_json(silent=True) or {}
    try:
        weight = float(payload["weight"])
        height = float(payload["height"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "請提供有效的體重（磅）與身高（公尺）"}), 400

    if height <= 0:
        return jsonify({"error": "身高必須大於 0"}), 400

    bmi_value = calculate_bmi(weight, height)
    category_key, label = CATEGORY_MAP[classify_bmi(bmi_value)]
    return jsonify({"bmi": round(bmi_value, 2), "category": category_key, "label": label})


if __name__ == "__main__":
    app.run(debug=True)
