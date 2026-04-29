from typing import Dict, List


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
    frequency: str
) -> Dict:

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

    interest = balance - total_contributed
    roi = (interest / total_contributed * 100) if total_contributed > 0 else 0

    return {
        "final_value": round(balance, 2),
        "total_contributed": round(total_contributed, 2),
        "interest_earned": round(interest, 2),
        "roi_percent": round(roi, 2)
    }

def generate_schedule(
    initial: float,
    annual_rate: float,
    years: int,
    contribution: float,
    frequency: str
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
        "balance": round(balance, 2)
    })

    for period in range(1, total_periods + 1):
        balance += contribution

        balance *= (1 + rate_per_period)

        if period % periods_per_year == 0:
            year = period // periods_per_year

            schedule.append({
                "year": year,
                "balance": round(balance, 2)
            })

    return schedule