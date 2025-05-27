def estimate_solar_output(roof_area_m2, panel_efficiency=0.18, avg_sun_hours=5):
    usable_area = roof_area_m2 * 0.75
    panel_area = 1.6
    num_panels = int(usable_area / panel_area)
    system_size_kw = (num_panels * 350) / 1000
    daily_output_kwh = system_size_kw * avg_sun_hours
    annual_output_kwh = daily_output_kwh * 365

    return {
        "num_panels": num_panels,
        "system_size_kw": system_size_kw,
        "daily_output_kwh": daily_output_kwh,
        "annual_output_kwh": annual_output_kwh
    }

def estimate_cost_and_roi(system_size_kw, subsidy=0.3, electricity_rate=8.0):
    cost_per_kw = 50000
    gross_cost = system_size_kw * cost_per_kw
    net_cost = gross_cost * (1 - subsidy)
    annual_savings = system_size_kw * 5 * 365 * electricity_rate
    payback_years = net_cost / annual_savings if annual_savings > 0 else None

    return {
        "gross_cost": gross_cost,
        "net_cost": net_cost,
        "annual_savings": annual_savings,
        "payback_years": round(payback_years, 2) if payback_years else "N/A"
    }

def full_solar_analysis(roof_area_m2):
    output = estimate_solar_output(roof_area_m2)
    cost_roi = estimate_cost_and_roi(output["system_size_kw"])
    return {**output, **cost_roi}
