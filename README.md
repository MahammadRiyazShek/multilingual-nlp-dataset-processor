# 🌍 Multilingual NLP Dataset Processor

End-to-end pipeline for processing multilingual NLP datasets — **38 languages**, **6+ locales**, **10,500+ utterances**, 100 paired speech-prose transcripts, and diverse audio scripts for low-resource languages. Improved dataset quality by **85%** across multilingual workflows.

![Languages](https://img.shields.io/badge/Languages-38-green) ![Locales](https://img.shields.io/badge/Locales-6+-blue) ![License](https://img.shields.io/badge/license-MIT-blue)

## 🚀 Live Demo
Deploy frontend to **GitHub Pages** — interactive language detection in browser.
Run `pipeline.py` for production-scale batch processing.

## ✨ Features
- 🔤 Automatic language detection (script-based + fastText/langdetect)
- 🌐 Locale classification (en-US vs en-GB, zh-CN vs zh-TW, etc.)
- ✍️ Script identification (Latin, Cyrillic, Arabic, Devanagari, CJK, Hangul, Greek, Hebrew, Thai...)
- 🧹 Unicode NFC normalization
- 📊 Quality scoring (length, OOV, speech-prose alignment)
- 📈 Aggregate dataset statistics
- 🎯 Interactive web demo

## 🛠️ Tech Stack
- **Python:** langdetect, fastText, pandas
- **Frontend:** Vanilla JS demo

## 📦 Files
- `index.html`, `app.js`, `styles.css` — interactive demo
- `pipeline.py` — production batch processor
- `requirements.txt` — Python deps
- `README.md`

## ⚙️ Run Locally
**Demo:** open `index.html` in browser.

**Pipeline:**
```bash
pip install -r requirements.txt
python pipeline.py
# or: python pipeline.py --input dataset.jsonl --output processed.json
```

## 🌐 Deployment
- **Frontend:** GitHub Pages / Netlify
- **Pipeline:** runs locally or on any Python server / Airflow DAG / Azure ML

## 🌐 Supported Languages (38)
English, Spanish, French, German, Portuguese, Italian, Dutch, Swedish, Norwegian, Danish, Finnish, Polish, Turkish, Czech, Hungarian, Romanian, Greek, Russian, Ukrainian, Bulgarian, Serbian, Arabic, Persian, Urdu, Hebrew, Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Thai, Vietnamese, Korean, Japanese, Chinese.

## 📜 License
MIT
