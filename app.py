import streamlit as st
import json
from vision_analysis import analyze_rooftop_image
from solar_calculator import full_solar_analysis

st.set_page_config(page_title="Solar Rooftop Analyzer", layout="centered")
st.title("☀️ AI-Powered Solar Rooftop Analyzer with Groq")

st.markdown("""
Upload a rooftop satellite image to:
- Estimate usable area
- Calculate solar panel output
- Compute ROI and payback period
""")

groq_api_key = st.text_input("🔑 Enter your Groq API Key", type="password")
image_file = st.file_uploader("📷 Upload Satellite Image", type=["jpg", "jpeg", "png"])

if image_file and groq_api_key:
    with open("temp_image.jpg", "wb") as f:
        f.write(image_file.read())

    st.image("temp_image.jpg", caption="Uploaded Rooftop Image", use_container_width=True)
    st.info("Analyzing rooftop using Groq LLaMA3 Vision model...")

    try:
        ai_response = analyze_rooftop_image("temp_image.jpg", groq_api_key, model="meta-llama/llama-4-scout-17b-16e-instruct")

        st.subheader("📊 AI Model Response")
        st.code(ai_response)

        ai_json = json.loads(ai_response.strip())
        roof_area = ai_json.get("roof_area_m2")

        if roof_area:
            st.success(f"✅ Estimated Usable Roof Area: {roof_area} m²")
            st.markdown(f"🕶️ Shading: {ai_json.get('shaded_percent')}%")
            st.markdown(f"🔢 Estimated Panels: {ai_json.get('estimated_panels')}")
            st.markdown(f"⚡ Daily Output: {ai_json.get('daily_output_kwh')} kWh")
            st.markdown(f"📅 Annual Output: {ai_json.get('annual_output_kwh')} kWh")

            st.subheader("🔧 Solar ROI Estimate")
            analysis = full_solar_analysis(float(roof_area))

            st.json(analysis)

        else:
            raise ValueError("Missing 'roof_area_m2'")

    except json.JSONDecodeError:
        st.warning("❗ Could not parse a valid JSON response. Please enter the roof area manually.")
        manual_area = st.number_input("Enter usable roof area (m²):", min_value=1.0)
        if manual_area:
            analysis = full_solar_analysis(manual_area)
            st.subheader("🔧 Solar ROI Estimate")
            st.json(analysis)
    except Exception as e:
        st.error(f"❌ Error during analysis: {str(e)}")

st.markdown("---")
st.caption("Built with 🧠 Groq Vision + Streamlit")