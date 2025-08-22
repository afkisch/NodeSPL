import re

def pytest_runtest_logreport(report):
    if report.longrepr:
        report_text = str(report.longrepr)
        report.longrepr = mask_secrets(report_text)

def mask_secrets(text: str) -> str:
    # Replace any X-API-KEY value with ***
    pattern = r"(x-api-key['\"]?:\s*)['\"]?.*?['\"]?([,}])"
    return re.sub(pattern, r"\1***\2", text, flags=re.IGNORECASE)