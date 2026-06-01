"""
Multilingual NLP Dataset Processor — Production Pipeline
Processes 10,500+ utterances across 38 languages and 6+ locales.
Handles paired speech-prose transcripts and low-resource language audio scripts.
"""
import json, csv, re, unicodedata
from pathlib import Path
from collections import Counter
from typing import List, Dict, Optional

try:
    from langdetect import detect, detect_langs, DetectorFactory
    DetectorFactory.seed = 42
    HAS_LANGDETECT = True
except ImportError:
    HAS_LANGDETECT = False

SUPPORTED = {
    'en','es','fr','de','pt','it','nl','sv','no','da','fi','pl','tr','cs','hu','ro',
    'el','ru','uk','bg','sr','ar','fa','ur','he','hi','bn','ta','te','mr','gu','kn',
    'ml','th','vi','ko','ja','zh'
}
LOCALES = {
    'en': ['en-US','en-GB','en-IN','en-AU','en-CA'],
    'es': ['es-ES','es-MX','es-AR','es-CO'],
    'fr': ['fr-FR','fr-CA','fr-BE'],
    'pt': ['pt-BR','pt-PT'],
    'zh': ['zh-CN','zh-TW','zh-HK'],
    'ar': ['ar-SA','ar-EG','ar-AE'],
}

def normalize(text: str) -> str:
    """Unicode NFC normalization + whitespace cleanup."""
    text = unicodedata.normalize('NFC', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def detect_script(text: str) -> str:
    for ch in text:
        c = ord(ch)
        if 0x4E00 <= c <= 0x9FFF: return 'CJK'
        if 0x3040 <= c <= 0x309F: return 'Hiragana'
        if 0xAC00 <= c <= 0xD7AF: return 'Hangul'
        if 0x0600 <= c <= 0x06FF: return 'Arabic'
        if 0x0900 <= c <= 0x097F: return 'Devanagari'
        if 0x0400 <= c <= 0x04FF: return 'Cyrillic'
        if 0x0370 <= c <= 0x03FF: return 'Greek'
        if 0x0590 <= c <= 0x05FF: return 'Hebrew'
        if 0x0E00 <= c <= 0x0E7F: return 'Thai'
    return 'Latin'

def detect_language(text: str) -> str:
    if HAS_LANGDETECT and text.strip():
        try:
            return detect(text)
        except Exception:
            return 'unknown'
    return 'unknown'

def classify_locale(lang: str, text: str) -> str:
    """Heuristic locale classification from regional vocabulary cues."""
    cues = {
        'en-GB': r'\b(colour|favourite|whilst|lorry|petrol)\b',
        'en-US': r'\b(color|favorite|truck|gas|sidewalk)\b',
        'es-MX': r'\b(órale|chido|güey)\b',
        'es-ES': r'\b(vale|tío|guay)\b',
        'pt-BR': r'\b(você|cara|legal)\b',
        'pt-PT': r'\b(tu|fixe|miúdo)\b',
        'zh-TW': r'[繁體]',
        'zh-CN': r'[简]',
    }
    for locale, rx in cues.items():
        if locale.startswith(lang) and re.search(rx, text, re.I):
            return locale
    return LOCALES.get(lang, [f'{lang}-XX'])[0] if lang in LOCALES else f'{lang}-XX'

def quality_score(utterance: str, transcript: Optional[str] = None) -> Dict:
    """Compute dataset quality metrics."""
    chars = len(utterance)
    words = len(utterance.split())
    score = 100
    if chars < 5:   score -= 30
    if chars > 500: score -= 10
    if words < 2:   score -= 20
    if transcript:
        ratio = len(transcript) / max(chars, 1)
        if not (0.5 <= ratio <= 2.0): score -= 15
    return {'chars': chars, 'words': words, 'quality_score': max(score, 0)}

def process_utterance(text: str, transcript: Optional[str] = None) -> Dict:
    """Full pipeline for a single utterance."""
    norm = normalize(text)
    lang = detect_language(norm)
    script = detect_script(norm)
    locale = classify_locale(lang, norm)
    quality = quality_score(norm, transcript)
    return {
        'text': norm,
        'language': lang,
        'language_supported': lang in SUPPORTED,
        'script': script,
        'locale': locale,
        'transcript': transcript,
        **quality,
    }

def process_dataset(input_path: str, output_path: str):
    """Batch process JSONL/CSV dataset."""
    inp = Path(input_path)
    rows = []
    if inp.suffix == '.jsonl':
        with open(inp) as f:
            for line in f:
                rec = json.loads(line)
                rows.append(process_utterance(rec.get('text',''), rec.get('transcript')))
    elif inp.suffix == '.csv':
        with open(inp) as f:
            for rec in csv.DictReader(f):
                rows.append(process_utterance(rec.get('text',''), rec.get('transcript')))

    # Aggregate stats
    lang_counts = Counter(r['language'] for r in rows)
    avg_quality = sum(r['quality_score'] for r in rows) / max(len(rows),1)
    stats = {
        'total_utterances': len(rows),
        'languages': dict(lang_counts.most_common()),
        'unique_languages': len(lang_counts),
        'avg_quality_score': round(avg_quality, 2),
        'supported_ratio': sum(1 for r in rows if r['language_supported']) / max(len(rows),1),
    }
    with open(output_path, 'w') as f:
        json.dump({'stats': stats, 'records': rows}, f, ensure_ascii=False, indent=2)
    print(f"✅ Processed {len(rows)} utterances. Stats: {stats}")
    return stats

if __name__ == '__main__':
    # Demo: process inline samples
    samples = [
        "Hello, how are you today?",
        "Bonjour, comment allez-vous?",
        "你好,今天怎么样?",
        "नमस्ते, आप कैसे हैं?",
        "مرحبا، كيف حالك؟",
    ]
    for s in samples:
        print(json.dumps(process_utterance(s), ensure_ascii=False, indent=2))
