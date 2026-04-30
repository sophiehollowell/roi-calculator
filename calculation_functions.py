from typing import Dict, List, Optional


FREQUENCY_MAP = {
    "annual": 1,
    "monthly": 12
}

# Convert percentage input into decimal
def normalize_rate(rate: float):
    return rate / 100


def calculate_investment(
    initial: float,
    annual_rate: float,
    years: int,
    contribution: float,
    frequency: str,
    annual_withdrawal: float = 0
):

    annual_rate = normalize_rate(annual_rate)

    balance = initial
    total_contributed = initial

    for year in range(1, years + 1):

        if frequency == "monthly":
            yearly_contribution = contribution * 12
        else:
            yearly_contribution = contribution

        balance += yearly_contribution
        total_contributed += yearly_contribution

        balance *= (1 + annual_rate)

        if annual_withdrawal:
            balance -= annual_withdrawal

            if balance < 0:
                balance = 0

    interest = balance - total_contributed
    roi = (interest / total_contributed * 100) if total_contributed > 0 else 0
    total_withdrawn = annual_withdrawal * years

    return {
        "final_value": round(balance, 2),
        "total_contributed": round(total_contributed, 2),
        "interest_earned": round(interest, 2),
        "roi_percent": round(roi, 2),
        "total_withdrawn": round(total_withdrawn, 2)
    }

def generate_schedule(
    initial: float,
    annual_rate: float,
    years: int,
    contribution: float,
    frequency: str,
    annual_withdrawal: float = 0
):
    annual_rate = normalize_rate(annual_rate)

    FREQUENCY_MAP = {
        "monthly": 12,
        "annual": 1
    }

    periods_per_year = FREQUENCY_MAP[frequency]
    rate_per_period = annual_rate / periods_per_year
    total_periods = years * periods_per_year

    balance = initial
    schedule = []

    schedule.append({
        "year": 0,
        "balance": round(balance, 2),
        "withdrawn": 0
    })

    for period in range(1, total_periods + 1):
        balance += contribution

        balance *= (1 + rate_per_period)

        if period % periods_per_year == 0:
            year = period // periods_per_year

            withdrawn = annual_withdrawal if annual_withdrawal else 0
            balance -= withdrawn

            if balance < 0:
                withdrawn += balance
                balance = 0

            schedule.append({
                "year": year,
                "balance": round(balance, 2),
                "withdrawn": round(withdrawn, 2)
            })

    return schedule

def translate_impact(
        growth: float, 
        impact_type: Optional[str],
        impact_cost: Optional[float]
):
    if not impact_type or not impact_cost or impact_cost <= 0:
        return None
    
    units = int(growth // impact_cost)

    return {
        "units": units,
        "type": impact_type,
        "cost": impact_cost
    }
