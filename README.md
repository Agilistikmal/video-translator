
-----

# 🎥 video-translator

An Open Source Python library initially designed to **translate subtitles/captions from video**, especially those from the **AKB48 Group Showroom Live** or **JKT48 IDN Live**.

> **Note:** While originally built for Showroom translations, this library is designed to be **flexible** and can be adapted for translating subtitles from **various video sources**.

-----

## ✨ Features

  * **Generate Subtitles:** Generate original subtitles.
  * **Video Translation:** Translate subtitles into video.
  * **Output Flexibility:** Display translations in a new window, overlay on the video (where supported), or save to a file (e.g., `.srt`).
  * **Caching:** Optional caching of previously translated phrases to reduce API calls and latency.

-----

## 🚀 Installation

### Prerequisites

  * Python 3.8 or higher.
  * An active internet connection (for translation APIs).
  * Deepseek API Key (we use deepseek to translate).

### Using pip

```bash
pip install git+https://github.com/agilistikmal/video-translator.git
```

### From Source

```bash
git clone https://github.com/agilistikmal/video-translator.git
cd video-translator
pip install -e .
```

-----

## 💡 Usage

Soon...

```python
from video_translator import VideoTranslator
```

-----

## 📚 Example

You can see example test case in [test/](https://github.com/Agilistikmal/video-translator/tree/master/tests)

-----

## 🤝 Contributing

Contributions are highly welcome\! Whether it's adding support for a new translation API, or fixing bugs, feel free to open an issue or submit a pull request.

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

## 📞 Author

Agil Ghani Istikmal - [@agilistikmal](https://github.com/agilistikmal)

-----