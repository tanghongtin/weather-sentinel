from services.config_service import load_config


WEEKDAYS = (
    "Thứ Hai",
    "Thứ Ba",
    "Thứ Tư",
    "Thứ Năm",
    "Thứ Sáu",
    "Thứ Bảy",
    "Chủ Nhật",
)


def format_rain_hours(hours, probability_threshold, rainfall_threshold):
    likely_hours = [
        hour
        for hour in hours
        if hour.get("probability") is not None
        and hour["probability"] >= probability_threshold
        and hour.get("rain") is not None
        and hour["rain"] >= rainfall_threshold
    ]
    if not likely_hours:
        return ["  Không có giờ nào đạt ngưỡng"]

    rows = []
    for hour in likely_hours:
        rain = f"{hour['rain']:.1f} mm"
        rows.append(
            f"{hour['time']:%d-%m %H:%M}  | "
            f"{hour['probability']:.0f}% | {rain}"
        )
    return rows


def build_forecast_text(forecast, days):
    config = load_config()
    if not forecast:
        return ""

    daily_forecasts = {}
    for hour in forecast:
        day = hour["time"].date()
        daily_forecasts.setdefault(day, []).append(hour)

    rain_threshold = config["rain_probability_threshold"]
    forecast_days = list(daily_forecasts.items())[:days]
    rainfall_threshold = config["min_rain_mm"]

    lines = ["Lượng mưa theo ngày", ""]
    for day, hours in forecast_days:
        probabilities = [
            hour["probability"]
            for hour in hours
            if hour.get("probability") is not None
        ]
        rainfall = [
            hour["rain"]
            for hour in hours
            if hour.get("rain") is not None
        ]
        probability = max(probabilities) if probabilities else None
        rainfall_total = sum(rainfall) if rainfall else None
        probability_text = "-" if probability is None else f"{probability:.0f}%"
        rainfall_text = "-" if rainfall_total is None else f"{rainfall_total:.1f} mm"

        lines.append(
            f"{WEEKDAYS[day.weekday()]} {day:%d/%m} | "
            f"{probability_text} | {rainfall_text}"
        )

    lines.extend([
        "",
        "",
        "Lượng mưa theo giờ",
        f"(xác suất ≥{rain_threshold}%, lượng mưa ≥{rainfall_threshold} mm)",
        "",
    ])
    all_hours = [hour for _, hours in forecast_days for hour in hours]
    lines.extend(format_rain_hours(all_hours, rain_threshold, rainfall_threshold))

    return "\n".join(lines)


def show_forecast(forecast, days):
    print(build_forecast_text(forecast, days))