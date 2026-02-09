# File: shield_hive/hive_brain.py
import google.generativeai as genai
import os

# Configure your API Key here or in Environment Variables
# If this is empty, the system automatically falls back to "Offline Mode"
GEMINI_API_KEY = "AIzaSyDRtKwdlQU9Jr8RRVlTUk2lIi5Z1I8O0nQ"

def analyze_threat_with_gemini(threat_name, reasons, file_hash):
    """
    Asks Gemini 1.5 Flash to analyze a security event.
    Returns a short, actionable summary.
    """
    if not GEMINI_API_KEY:
        return "AI_OFFLINE: Heuristic Analysis Only."

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            f"Act as a Cyber Security Analyst. Analyze this threat:\n"
            f"Name: {threat_name}\n"
            f"Behaviors: {reasons}\n"
            f"Hash: {file_hash}\n\n"
            f"Provide a 1-sentence assessment of the risk and technical impact. "
            f"Do not be verbose. Focus on what it does."
        )
        
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print(f"⚠️ ORACLE ERROR: {e}")
        return "AI_UNREACHABLE: Fallback to standard DB analysis."