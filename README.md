# 📄 tghtml
Simple tool for parse common HTML to Telegram HTML

## 🚀 Start
To start install package from pypi:
```sh
pip install tghtml
```

or install from sources:
```sh
python setup.py install
```

## 🔩 Usage
```python
from tghtml import TgHTML

TgHTML("<p>Ban</p>").parsed  # output "ban"
```
