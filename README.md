# 📄 tghtml
Parser to telegram html

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
from tghtml import tghtml

tghtml("<p>Ban</p>")  # output "ban\n"
```

## 🔨 Dependencies
### 🍲 [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
Beautiful Soup is a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.

### 🌳 [lxml](https://pypi.org/project/lxml/)
lxml is a Pythonic, mature binding for the libxml2 and libxslt libraries. It provides safe and convenient access to these libraries using the ElementTree API.
