import re

PHONE_KEEP_DIGITS = re.compile(r"\D+")

STATE_NAME = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
    "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota",
    "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island",
    "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin",
    "WY": "Wyoming", "DC": "District of Columbia"
}

def _replace_america(text: str) -> str:
    if not text:
        return text
    return re.sub(r"\b(amerika serikat)\b", "United States", text, flags=re.IGNORECASE)


def normalize_row(row: dict) -> dict:
    r = dict(row)
    #keep digits and drop leading US '1'
    ph = (r.get("recipient_phone_number") or "").strip()
    digits = PHONE_KEEP_DIGITS.sub("", ph)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    r["recipient_phone_number"] = digits or None

    #website domain
    url = (r.get("website") or "").strip().lower()
    if url:
        url = re.sub(r"^https?://(www\.)?", "", url)
        url = url.split("/")[0]
    r["website"] = url or None

    #replace amerika serikat with united states
    for key in ("recipient_line_address", "geo_location"):
        if key in r and r.get(key):
            r[key] = _replace_america(r.get(key).strip())


    for k in ("recipient_company", "recipient_email", "city","state", "country"):
        if r.get(k):
            r[k] = r[k].strip()
            if k == "state":
                if r[k].upper() in STATE_NAME:
                    r[k] = STATE_NAME[r[k].upper()]
            elif k == "country" and r[k].lower() == "amerika serikat":
                r[k] = "USA"

    return r
