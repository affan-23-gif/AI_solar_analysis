def rooftop_analysis_prompt():
    """
    Returns a structured JSON-only prompt for solar rooftop analysis.
    """
    return (
        "You are a solar rooftop assessment expert. Analyze the uploaded rooftop image and respond ONLY with this valid JSON:\n"
        "{\n"
        '  "roof_area_m2": number,\n'
        '  "shaded_percent": number,\n'
        '  "estimated_panels": number,\n'
        '  "daily_output_kwh": number,\n'
        '  "annual_output_kwh": number\n'
        "}\n"
        "Do not include text, explanation, or commentary — JSON only."
    )
