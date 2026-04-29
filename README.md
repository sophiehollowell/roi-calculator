# ROI Investment Calculator

A simple web-based investment calculator built with **FastAPI** and a lightweight frontend using **HTML + JavaScript (Chart.js)**.

It helps users understand how their investments grow over time based on:
- Initial investment
- Regular contributions
- Expected annual return
- Investment duration

---

## Features

- Calculates investment growth over time
- Interactive chart visualization (Chart.js)
- Supports monthly or annual contributions
- Shows:
  - Final portfolio value
  - Total contributions
  - Interest earned
  - Return on investment (ROI)

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

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- Pydantic

### Frontend
- HTML
- CSS
- Vanilla JavaScript
- Chart.js

---

## 📦 Installation

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
