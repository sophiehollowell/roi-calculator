# ROI Investment Calculator for Nonprofits

A simple web-based investment calculator built with **FastAPI** and a lightweight frontend using **HTML + JavaScript (Chart.js)**.

It helps users understand how their investments can potentially grow over time, and it also highlights how additional funding generated from investment growth can translate into **real-world impact.**

---

## Features

### Investment Modeling
- Calculates investment growth over time from:
  - Initial investment
  - Expected annual rate of return
  - Investment duration
  - Recurring contributions (monthly or annual)
- Displays:
  - Final portfolio value
  - Total invested funds
  - Additional funding generated (investment growth)
  - **Impact Translation (Optional)**
      - Convert investment growth into real-world outcomes
      - User-defined inputs:
          - Impact type (e.g. meals, trees, scholarships)
          - Cost per unit
      - Output:
          - Estimated number of impact units funded by investment growth
          - Example: $5,000 in investment growth → 100 meals funded (at $50/meal)
      - *Fully optional — core investment calculations work independently*
  - **Growth Chart**
      - Interactive growth chart that comares total invested capital and total portfolio value over time

---

## How It Works

The calculator simulates investment growth over time:

1. You start with an initial investment
2. You optionally add recurring contributions
3. Your balance grows based on an assumed annual return
4. The system calculates:
   - Total contributions
   - Growth from compounding
   - Final portfolio value

> Note: The model assumes **annual compounding of returns**.

### Impact Layer (Optional)

If enabled:

1. User defines an impact type and cost per unit
2. The system translates investment growth into:
   - Number of units funded *(growth ÷ cost per unit)*

---

## Tech Stack

### Backend
- FastAPI
- Pydantic

### Frontend
- HTML
- CSS
- Vanilla JavaScript
- Chart.js

---

## Installation

### Clone the Repository
```bash
git clone https://github.com/your-username/roi-calculator.git
cd roi-calculator
```

### Create Virtual Environment
```python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### Install Dependendicies
```pip install -r requirements.txt```

### Run the App
```uvicorn main:app --reload```
Run the above line in Terminal, and then open the link.

### Notes
- Assumes annual compounding of returns
- Assumes that contributions happen at the end of the period
- Impact estimates are user-defined and illustrative, not exact projections
- Designed for:
    - Financial education
    - Nonprofit storytelling

### Future Improvements
- Validation and error handling improvements
  - Issues:
      - Currently, if users hit "Calculate" with an invalid input, the tool will do nothing. There is no message letting them know what the issue is.
      - For the annual return, they should really only be allowed to enter in a number > 1 since the backend assumes a percentage and then converts to a decimal.
  - Fix:
      - Proivde clear error messaging when inputs are invalid or missing (e.g., “Please enter a valid number of years” instead of doing nothing)
      - Enforce input constraints:
          - Annual return > 0
          - Years > 0
          - No negative contributions
- Input experience and formatting
  - Standardize input behavior across fields:
      - Currency fields → support commas (1,000)
      - Numeric fields (years, rate) → clean number inputs without formatting conflicts
  - Remove inconsistent UI elements (e.g., browser up/down arrows on some inputs)
- State persistance
  - Preserve results on page reload
