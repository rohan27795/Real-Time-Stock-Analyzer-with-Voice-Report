import os
import requests
from dotenv import load_dotenv
from fpdf import FPDF
import unicodedata

# Load environment variables
load_dotenv()
EURI_API_KEY = os.getenv("EURI_API_KEY")

# 🔹 Remove non-latin1 characters for FPDF compatibility
def clean_text_for_pdf(text):
    def replace_non_latin1(c):
        try:
            c.encode('latin-1')
            return c
        except UnicodeEncodeError:
            return ''  # Remove unsupported character
    return ''.join(replace_non_latin1(c) for c in text)

# 🔹 Generate SWOT report from EURI GPT-4.1 Nano
def generate_swot_report(info, sentiment):
    prompt = f"""
    Create a SWOT analysis of the company with this context:
    🔸 Company: {info.get('shortName')}
    🔸 Sector: {info.get('sector')}
    🔸 Market Cap: {info.get('marketCap')}
    🔸 Summary: {info.get('longBusinessSummary')}
    🔸 Real-time Sentiment: {sentiment}

    Format it with clear headings:
    Strengths:
    Weaknesses:
    Opportunities:
    Threats:
    """

    payload = {
        "model": "gpt-4.1-nano",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 700,
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {EURI_API_KEY}",
        "Content-Type": "application/json"
    }

    # Check for API key
    if not EURI_API_KEY:
        return "Error: EURI_API_KEY is not set in the environment. Please check your .env file."

    try:
        response = requests.post(
            "https://api.euron.one/api/v1/euri/alpha/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        response_data = response.json()

        # Safely parse the response (OpenAI-compatible format)
        if 'choices' in response_data and len(response_data['choices']) > 0:
            return response_data['choices'][0]['message']['content']
        
        # Handle alternative formats or errors in JSON
        elif 'error' in response_data:
            error_msg = response_data.get('error', {}).get('message', 'Unknown API error')
            return f"API Error: {error_msg}"
        
        else:
            return "Error: Unexpected response format from LLM API."

    except requests.exceptions.RequestException as e:
        return f"Connection Error: Unable to reach SWOT API. {str(e)}"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"

# 🔹 Save SWOT to PDF safely (without encoding errors)
def save_swot_pdf(swot_text: str, filename="swot_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    clean_text = clean_text_for_pdf(swot_text)

    for line in clean_text.split("\n"):
        pdf.multi_cell(0, 10, line)

    pdf.output(filename)
    return filename