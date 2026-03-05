from pydantic import BaseModel
from typing import List, Dict


class ForecastItem(BaseModel):
    datetime: str
    predicted_energy_kWh: float
    predicted_cost: float


class PredictionResponse(BaseModel):
    message: str

    raw_file: str
    processed_file: str
    report_file: str

    total_rows: int
    total_anomalies: int
    estimated_total_cost: float

    next_24_hours_forecast: List[ForecastItem]

    estimated_next_month_usage_kWh: float
    estimated_next_month_cost: float