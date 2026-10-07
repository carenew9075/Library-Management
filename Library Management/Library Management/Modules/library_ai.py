import requests

from Config import config


# ---------------------------------------------------------
# ASK GEMINI
# ---------------------------------------------------------

def ask_gemini(question):

    if not config.GEMINI_API_KEY:
        return "Gemini is not configured. Add an API key in Settings."

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        + config.GEMINI_MODEL
        + ":generateContent"
    )

    headers = {
        "x-goog-api-key": config.GEMINI_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": question}
                ]
            }
        ]
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=20
        )

        if response.status_code != 200:
            return "Gemini could not respond right now. Check the model and API key in Settings."

        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]

    except requests.RequestException:
        return "Gemini is unavailable. Check your internet connection."
    except (KeyError, IndexError, TypeError):
        return "Gemini returned an unexpected response."


# ---------------------------------------------------------
# TEST GEMINI
# ---------------------------------------------------------

def test_gemini():
    answer = ask_gemini("Reply with exactly OK.")
    return answer.strip().upper() == "OK."
