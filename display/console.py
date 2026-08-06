from datetime import datetime, timedelta
from services.config_service import load_config


MODEL_NAMES = {
    "ecmwf_ifs": "ECMWF",
    "dwd_icon_seamless": "ICON",
    "ncep_gfs_seamless": "GFS",
    "bom_access_global": "ACCESS",
}


def format_datetime(dt: datetime):
    return dt.strftime("%d/%m %H:%M")


def build_forecast_text(forecasts, days):
    config = load_config()
    if not forecasts:
        return ""

    lines = []

    models = list(forecasts.keys())
    base = forecasts[models[0]]

    end_time = base[0]["time"] + timedelta(days=days)
    max_hours = min(len(f) for f in forecasts.values())

    for i in range(max_hours):

        hour = base[i]

        if hour["time"] >= end_time:
            break

        agree = 0

        for model in models:
            rain = forecasts[model][i].get("rain")

            if rain is not None and rain >= config["min_rain_mm"]:
                agree += 1

        if agree == 0:
            continue

        lines.append(f"🕒 {format_datetime(hour['time'])}")
        lines.append("")

        for model in models:

            data = forecasts[model][i]

            name = MODEL_NAMES.get(model, model.upper())

            rain = data.get("rain")
            prob = data.get("probability")
            low_cloud = data.get("cloud_low")
            mid_cloud = data.get("cloud_mid")
            cape = data.get("cape")

            rain_text = "-" if rain is None else f"{rain:.1f}mm"
            prob_text = "-" if prob is None else f"{prob}%"
            low_cloud_text = "-" if low_cloud is None else f"{int(low_cloud)}%"
            mid_cloud_text = "-" if mid_cloud is None else f"{int(mid_cloud)}%"
            cape_text = "-" if cape is None else f"{int(cape)}"

            lines.append(
                f"{name:<6} "
                f"{prob_text:<4} "
                f"{rain_text:<6} "
                f"{low_cloud_text:<4} "
                f"{mid_cloud_text} "
                #f"{cape_text:<5}"
            )

        lines.append("")

        lines.append(f"✅ Đồng thuận: {agree}/{len(models)}")
        lines.append("─" * 20)
        lines.append("")

    return "\n".join(lines)


def show_forecast(forecasts, days):
    print(build_forecast_text(forecasts, days))