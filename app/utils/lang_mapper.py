def normalize_lang_code(lang: str) -> str:
    if not lang:
        return None
    lang = lang.lower()

    if lang in ["zh", "zh-hans", "zh-cn"]:
        return "zh-cn"
    if lang in ["zh-hant", "zh-tw"]:
        return "zh-tw"

    return lang