import requests

urls = [
    "https://api.euron.one/api/v1/euri/alpha/chat/completions",
    "https://api.euron.one/api/v1/euri/chat/completions",
    "https://api.euron.one/api/v1/chat/completions",
    "https://api.euron.one/v1/chat/completions",
    "https://api.euron.one/euri/v1/chat/completions",
    "https://api.euron.one/alpha/v1/chat/completions",
    "https://api.euron.one/api/v1/euri/gpt-4.1-nano/chat/completions",
    "https://api.euron.one/api/v1/euri/v1/chat/completions",
    "https://euri.euron.one/api/v1/chat/completions",
    "https://api.euron.one/v1/completions"
]

print("Probing URLs for Euron AI API...")
for url in urls:
    try:
        # Use HEAD or GET/POST with no data to check existence
        # 401/403 means the endpoint exists but needs auth. 404 means it doesn't.
        response = requests.post(url, timeout=5)
        print(f"{url} -> {response.status_code}")
    except Exception as e:
        print(f"{url} -> Error: {e}")
