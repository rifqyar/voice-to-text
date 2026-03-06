from deep_translator import GoogleTranslator
from app.utils.lang_mapper import normalize_lang_code

def safe_translate(text: str, src_lang: str, dest_lang: str):
    try:
        if not text.strip():
            return ""

        src_lang_norm = normalize_lang_code(src_lang)
        dest_lang_norm = normalize_lang_code(dest_lang)

        # deep-translator otomatis handle 'auto' detect
        translator = GoogleTranslator(source=src_lang_norm or 'auto', target=dest_lang_norm)
        translated = translator.translate(text)

        print(f"🌐 Translate ({src_lang_norm or 'auto'}→{dest_lang_norm}): {translated}")
        return translated

    except Exception as e:
        print(f"⚠️ Translate failed ({src_lang}→{dest_lang}): {e}")
        return text