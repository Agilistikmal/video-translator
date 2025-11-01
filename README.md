
-----

# 🎥 video-translator

An Open Source Python library initially designed to **translate subtitles/captions from live video streams**, especially those from the **AKB48 Group Live Showroom**.

> **Note:** While originally built for Showroom translations, this library is designed to be **flexible** and can be adapted for translating subtitles from **various video sources**.

-----

## ✨ Features

  * **Live Translation:** Translate incoming subtitles/captions in real-time.
  * **Showroom Integration:** Specific modules/scripts to interface with the Showroom platform's caption system (or similar streaming sites).
  * **Customizable Translators:** Support for various translation APIs (e.g., Google Translate, DeepL, etc.) via a plug-in architecture.
  * **Output Flexibility:** Display translations in a new window, overlay on the video (where supported), or save to a file (e.g., `.srt`).
  * **Caching:** Optional caching of previously translated phrases to reduce API calls and latency.

-----

## 🚀 Installation

### Prerequisites

  * Python 3.8 or higher.
  * An active internet connection (for translation APIs).
  * API key for your chosen translation service (e.g., DeepL, Google Cloud Translation).

### Using pip

```bash
pip install video-translator
```

### From Source

```bash
git clone https://github.com/yourusername/video-translator.git
cd video-translator
pip install -e .
```

-----

## ⚙️ Configuration

A configuration file (`config.ini` or similar) is used to set up API keys, target/source languages, and output preferences.

### Example `config.ini`

```ini
[TRANSLATOR]
service = deepl
api_key = YOUR_DEEPL_API_KEY
source_lang = ja  ; Japanese
target_lang = en  ; English

[SHOWROOM]
# Specific configurations for fetching Showroom captions (details depend on implementation)
# For example: URL pattern, API endpoints, etc.
```

-----

## 💡 Usage

### Basic Real-Time Translation

The core of the library is the `Translator` class and the `LiveCaptionFetcher` (or a similar source-specific class).

```python
from video_translator import Translator
from video_translator.sources.showroom import ShowroomCaptionFetcher
import time

# Initialize the components
translator = Translator(config_file='config.ini')
fetcher = ShowroomCaptionFetcher(room_id="12345")

print("Starting live translation...")

try:
    for original_caption in fetcher.start_listening():
        if original_caption:
            translated_caption = translator.translate(original_caption)
            
            print(f"Original (ja): {original_caption}")
            print(f"Translated (en): **{translated_caption}**\n")
            
except KeyboardInterrupt:
    print("\nTranslation stopped by user.")
finally:
    fetcher.stop_listening()
```

### Running the CLI Tool (If applicable)

For quick usage, you can run the pre-built CLI script:

```bash
video-translator-cli --source showroom --room-id 12345
```

-----

## 🤝 Contributing

Contributions are highly welcome\! Whether it's adding support for a new translation API, improving the caption fetching logic for Showroom, or fixing bugs, feel free to open an issue or submit a pull request.

### To contribute:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

-----

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

-----

## 📞 Contact

Your Name / Your GitHub Username - [@YourTwitterHandle](https://www.google.com/search?q=https://twitter.com/YourTwitterHandle) (Optional)

Project Link: [https://github.com/yourusername/video-translator](https://www.google.com/search?q=https://github.com/yourusername/video-translator)

-----