import re

INJ_PATTERNS = [r"ignore.+previous", r"forget.+instruction", r"override", r"jailbreak", r"system\s*:"]
_INJ = [re.compile(p, re.IGNORECASE) for p in INJ_PATTERNS]

def sanitize(txt):
    if not txt:
        return "", False
    txt = txt.strip()[:400]
    susp = any(p.search(txt) for p in _INJ)
    return txt, susp