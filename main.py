from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from calculation_functions import calculate_investment, generate_schedule

app = FastAPI()

class InvestmentRequest(BaseModel):
    initial: float = 0
    rate: float 
    years: int
    contribution: float = 0
    frequency: str

@app.post("/calculate")
def calculate(data: InvestmentRequest):

    summary = calculate_investment(
        initial=data.initial,
        annual_rate=data.rate,
        years=data.years,
        contribution=data.contribution,
        frequency=data.frequency
    )

    schedule = generate_schedule(
        initial=data.initial,
        annual_rate=data.rate,
        years=data.years,
        contribution=data.contribution,
        frequency=data.frequency
    )

    return {
        "summary": summary,
        "schedule": schedule
    }

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
    <head>
        <title>ROI Calculator</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <style>
            body {
                margin: 0;
                font-family: Helvetica, sans-serif;
                background: #f9fafb;
                height: 100vh;
                display: flex;
            }

            /* SIDEBAR */
            .sidebar {
                width: 340px;
                background: white;
                padding: 30px;
                border-right: 1px solid #e5e7eb;

                overflow: visible;

                display: flex;
                flex-direction: column;
                gap: 18px;
            }

            .input-group {
                display: flex;
                flex-direction: column;
                gap: 6px;
            }

            label {
                font-size: 13px;
                font-weight: 600;
                color: #111827;
                display: flex;
                align-items: center;
            }

            .helper {
                font-size: 12px;
                color: #6b7280;
                margin-top: -2px;
            }

            input, select {
                padding: 10px;
                border-radius: 8px;
                border: 1px solid #d1d5db;
                width: 100%;
            }

            input:focus, select:focus {
                outline: none;
                border-color: #9ca3af;
            }

            button {
                padding: 12px;
                border-radius: 8px;
                border: none;
                background: #4169df;
                color: white;
                cursor: pointer;
                font-weight: 600;
                margin-top: 10px;
            }

            button:hover {
                background: #87a6ff;
            }

            .tooltip {
                position: relative;
                display: inline-block;
                cursor: help;
                margin-left: 6px;
                font-size: 12px;
                color: #6b7280;
                z-index: 1;
            }

            .tooltip .tooltip-text {
                visibility: hidden;
                opacity: 0;

                width: 240px;
                background: #111827;
                color: #fff;
                text-align: left;
                border-radius: 8px;
                padding: 10px;

                position: absolute;
                z-index: 9999;

                top: auto;

                bottom: 125%;
                left: 50%;
                transform: translateX(-50%);

                font-size: 12px;
                line-height: 1.4;

                transition: opacity 0.15s ease-in-out;

                white-space: normal;
                pointer-events: none;
            }

            .tooltip:hover .tooltip-text {
                visibility: visible;
                opacity: 1;
            }

            /* fallback alignment options */
            .tooltip.right .tooltip-text {
                left: auto;
                right: 0;
                transform: none;
            }

            .tooltip.left .tooltip-text {
                left: 0;
                transform: none;
            }

            /* MAIN */
            .main {
                flex: 1;
                padding: 40px;
                display: flex;
                flex-direction: column;
                gap: 20px;
            }
            .callout {
                background: linear-gradient(135deg, #4169df, #5a7dff);
                color: white;
                padding: 25px;
                border-radius: 14px;
                box-shadow: 0 6px 20px rgba(79, 70, 229, 0.25);
            }

            .callout-label {
                font-size: 14px;
                opacity: 0.9;
                margin-bottom: 8px;
            }

            .callout-value {
                font-size: 38px;
                font-weight: bold;
            }

            .callout-sub {
                margin-top: 6px;
                font-size: 13px;
                opacity: 0.85;
            }

            /* CARDS */
            .cards {
                display: flex;
                gap: 10px;
            }

            .card {
                flex: 1;
                background: white;
                padding: 15px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.05);
                border: 1px solid #eef2f7;
            }

            .card h3 {
                margin: 0;
                font-size: 13px;
                color: #6b7280;
                font-weight: 600;
            }

            .card p {
                font-size: 18px;
                margin: 8px 0 0;
                color: #111827;
                font-weight: 600;
            }

            /* CHART */
            canvas {
                background: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.05);
                border: 1px solid #eef2f7;
            }
        </style>
    </head>

    <body>

        <!-- SIDEBAR -->
        <div class="sidebar">

            <div class="input-group">
                <label>
                    How much are you starting with?
                    <span class="tooltip">ⓘ
                        <span class="tooltip-text">
                            Your initial investment (one-time deposit).
                        </span>
                    </span>
                </label>
                <input id="initial" type="text" inputmode="numeric">
            </div>

            <div class="input-group">
                <label>
                    What is your expected annual return (%)?
                    <span class="tooltip">ⓘ
                        <span class="tooltip-text">
                            Average yearly return assumption (e.g. 7%).
                        </span>
                    </span>
                </label>
                <input id="rate" type="number">
            </div>

            <div class="input-group">
                <label>
                    How many years will you invest?
                    <span class="tooltip">ⓘ
                        <span class="tooltip-text">
                            Number of years you plan to keep your money invested in the account.
                        </span>
                    </span>
                </label>
                <input id="years" type="number">
            </div>

            <div class="input-group">
                <label>
                    How much will contribute each period?
                    <span class="tooltip">ⓘ
                        <span class="tooltip-text">
                            Recurring deposit added each period. This can be $0 if you don't plan to add funds after your initial investment.
                        </span>
                    </span>
                </label>
                <input id="contribution" type="text" inputmode="numeric">
            </div>

            <div class="input-group">
                <label>
                    How often will you contribute?
                    <span class="tooltip">ⓘ
                        <span class="tooltip-text">
                            Select how frequently you intend to add funds to this investment.
                        </span>
                    </span>
                </label>
                <select id="frequency">
                    <option value="monthly">Monthly</option>
                    <option value="annual">Annual</option>
                </select>
            </div>

            <button onclick="calculate()">Calculate</button>
        </div>

        <!-- MAIN -->
        <div class="main">

            <!-- HERO -->
            <div class="callout">
                <div class="callout-label">This investment will be worth:</div>
                <div class="callout-value" id="finalValue">$0</div>
                <div class="callout-sub">Over <span id="yearsLabel">—</span> years</div>
            </div>

            <!-- CARDS -->
            <div class="cards">
                <div class="card">
                    <h3>Total invested capital</h3>
                    <p id="invested">$0</p>
                </div>

                <div class="card">
                    <h3>Total growth</h3>
                    <p id="simple">$0</p>
                </div>
            </div>

            <!-- CHART -->
            <canvas id="chart"></canvas>
        </div>

        <script>
        let chart;
        
        function format(n) {
            return "$" + Number(n).toLocaleString(undefined, {
                maximumFractionDigits: 0
            });
        }

        function parseNumber(id) {
            const value = document.getElementById(id).value;

            if (!value || value.trim() === "") return 0;

            return parseFloat(value.replace(/,/g, "")) || 0;
        }
        
        async function calculate() {
        
            const payload = {
                initial: parseNumber("initial"),
                rate: parseFloat(document.getElementById("rate").value) || 0,
                years: parseInt(document.getElementById("years").value) || 0,
                contribution: parseNumber("contribution"),
                frequency: document.getElementById("frequency").value
            };
        
            const res = await fetch("/calculate", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload)
            });
        
            const data = await res.json();
        
            const finalValue = data.summary.final_value;
            const invested = data.summary.total_contributed;
            const growth = data.summary.interest_earned;
        
            // ===== TOP METRICS =====
            document.getElementById("finalValue").innerText = format(finalValue);
            document.getElementById("invested").innerText = format(invested);
            document.getElementById("simple").innerText = format(growth);
            document.getElementById("yearsLabel").innerText = payload.years;
        
            const labels = data.schedule.map(p => "Year " + p.year);
            const balances = data.schedule.map(p => p.balance);

            const contributions = data.schedule.map(p => {
                const periodsPerYear = payload.frequency === "monthly" ? 12 : 1;
                return payload.initial + (payload.contribution * p.year * periodsPerYear);
            });
        
            if (chart) chart.destroy();
        
            const ctx = document.getElementById("chart");
        
            chart = new Chart(ctx, {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: "Invested Capital",
                            data: contributions,
                            borderColor: "#9ca3af",
                            backgroundColor: "rgba(156,163,175,0.2)",
                            fill: true,
                            tension: 0.35,
                            pointRadius: 0
                        },
                        {
                            label: "Investment Growth",
                            data: balances,
                            borderColor: "#4169df",
                            backgroundColor: "rgba(65,105,223,0.15)",
                            fill: "-1",
                            tension: 0.35,
                            pointRadius: 0
                        }
                    ]
                },
                options: {
                    responsive: true,
                    interaction: {
                        mode: "index",
                        intersect: false
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(ctx) {
                                    return ctx.dataset.label + ": " + format(ctx.raw);
                                }
                            }
                        },
                        legend: {
                            position: "top",
                            labels: {
                                usePointStyle: true,
                                pointStyle: "circle",
                                boxWidth: 8,
                                boxHeight: 8,
                                padding: 15
                            }
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: "Time (Years)"
                            },
                            grid: {
                                display: false
                            }
                        },
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: "Value ($)"
                            },
                            ticks: {
                                callback: v => "$" + v.toLocaleString()
                            },
                            grid: {
                                color: "rgba(0,0,0,0.05)"
                            }
                        }
                    }
                }
            });
        }
        </script>

        <script>
        function formatNumberWithCommas(value) {
            if (!value) return "";

            const number = value.replace(/,/g, "");
            if (isNaN(number)) return "";

            return Number(number).toLocaleString();
        }

        function attachCurrencyFormatter(id) {
            const input = document.getElementById(id);

            input.addEventListener("input", () => {
                let value = input.value;

                if (value === "") return;

                value = value.replace(/,/g, "");

                if (!/^\d+$/.test(value)) return;

                input.value = Number(value).toLocaleString();

                input.setSelectionRange(input.value.length, input.value.length);
            });
        }

        attachCurrencyFormatter("initial");
        attachCurrencyFormatter("contribution");
        </script>

        <script>
        document.querySelectorAll('.tooltip').forEach(tip => {
            tip.addEventListener('mouseenter', () => {
                const text = tip.querySelector('.tooltip-text');

                // reset any previous positioning
                text.style.top = '';
                text.style.bottom = '125%';

                const rect = text.getBoundingClientRect();

                // if tooltip goes off top of screen → flip it
                if (rect.top < 0) {
                    text.style.bottom = 'auto';
                    text.style.top = '125%';
                }
            });
        });
        </script>
        
    </body>
    </html>
    """