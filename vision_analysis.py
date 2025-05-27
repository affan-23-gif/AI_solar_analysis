import base64
import json
import re # Import the regular expression module
from groq import Groq

def analyze_rooftop_image(image_path: str, groq_api_key: str, model: str = "meta-llama/llama-4-scout-17b-16e-instruct") -> str:
    """
    Analyze rooftop image using Groq's LLaMA 4 Vision model.
    Extracts and returns the pure JSON string output from the model.
    """

    client = Groq(api_key=groq_api_key)

    # Convert image to data URL
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    # Use image/jpeg as a fallback if the actual image type isn't known
    image_url = f"data:image/jpeg;base64,{image_base64}"

    # Prompt message
    prompt_content = (
        "You are a solar rooftop expert. Analyze this image and return only a valid JSON object like:\n"
        "{\n"
        '  "roof_area_m2": number, \n'
        '  "shaded_percent": number, \n'
        '  "estimated_panels": number, \n'
        '  "daily_output_kwh": number, \n'
        '  "annual_output_kwh": number\n'
        "}\n"
        "Do not include any other text, explanations, or markdown formatting (like ```json). Just the raw JSON object."
    )

    prompt = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prompt_content
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": image_url
                }
            }
        ]
    }

    # Call Groq vision model
    completion = client.chat.completions.create(
        model=model,
        messages=[prompt],
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        stream=False
    )

    raw_model_output = completion.choices[0].message.content

    # --- Robust JSON extraction logic ---
    # Attempt to find JSON wrapped in markdown code blocks first
    json_match = re.search(r'```json\s*(\{.*\})\s*```', raw_model_output, re.DOTALL)
    if json_match:
        # If found, return the content of the first capturing group (the JSON itself)
        return json_match.group(1).strip()

    # If not found in markdown, try to find a standalone JSON object
    # This regex looks for a string that starts with '{' and ends with '}'
    # and contains valid JSON characters in between.
    # It's more permissive for cases where the model doesn't use markdown.
    standalone_json_match = re.search(r'(\{.*?\})', raw_model_output, re.DOTALL)
    if standalone_json_match:
        potential_json_string = standalone_json_match.group(1).strip()
        try:
            # Validate if it's actually valid JSON
            json.loads(potential_json_string)
            return potential_json_string
        except json.JSONDecodeError:
            # If it looks like JSON but isn't valid, fall through to the next step
            pass

    # As a last resort, if no clear JSON is found, try to clean and return the whole thing
    # This might still fail in app.py if it's not valid JSON, but it's the best we can do
    # if the model completely deviates from the requested format.
    # Remove common conversational prefixes/suffixes
    cleaned_output = raw_model_output.replace("Here is the analysis:", "").strip()
    cleaned_output = cleaned_output.replace("```json", "").replace("```", "").strip()

    print(f"Warning: Could not find clear JSON in model output. Returning raw/cleaned output for app.py to handle. Raw: {raw_model_output[:200]}...")
    return cleaned_output
