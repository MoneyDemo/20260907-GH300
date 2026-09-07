# BMI Calculator

這是一個簡單的 BMI 計算器，能依據體重（磅）與身高（公尺）計算 BMI，
並根據成人健康體位標準進行分類。

## 專案目的

這個專案的目標是讓新手能夠：

- 理解 BMI 的計算方式
- 學習如何利用 pytest 進行單元測試
- 了解「分工明確、可測試」的程式設計方式

## 使用 uv 執行測試

這個專案使用 `uv` 作為 Python 環境管理工具，請依照以下步驟操作：

1. 打開終端機，進入專案資料夾：

   ```bash
   cd C:\Users\tzyu\Downloads\20260907
   ```

2. 執行 pytest：

   ```bash
   uv run pytest
   ```

3. 若你想只執行某一個測試檔案，也可以這樣做：

   ```bash
   uv run pytest tests/test_calculate_bmi.py
   ```

   ```bash
   uv run pytest tests/test_classify_bmi.py
   ```

## 測試內容說明

這個專案只針對兩個函式撰寫單元測試：

- `calculate_bmi()`
- `classify_bmi()`

每個測試案例都被寫成獨立的 function，方便閱讀與維護。

## 重要提醒

- 此專案使用 `uv` 環境，不要直接使用系統預設的 `python` 來執行測試。
- 若你尚未安裝 `uv`，請先安裝它，再依上述步驟執行。
- 所有測試都位於 `tests/` 資料夾中，並依功能分成兩個檔案。

## 常用命令

```bash
uv run pytest
uv run pytest tests/test_calculate_bmi.py
uv run pytest tests/test_classify_bmi.py
```
