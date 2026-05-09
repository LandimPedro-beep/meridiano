import os
import re

css_path = r"c:\Users\pedro\meridiano\src\meridiano\static\css\style.css"

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Update header styles for a news site look
css = re.sub(
    r"\.header-content\s*\{[^}]+\}",
    ".header-content {\n    max-width: 1400px;\n    margin: 0 auto;\n    display: flex;\n    flex-direction: column;\n    justify-content: center;\n    align-items: center;\n    gap: 20px;\n}",
    css, count=1
)

css = re.sub(
    r"\.main-nav\s*\{[^}]+\}",
    ".main-nav {\n    display: flex;\n    gap: 25px;\n    margin: 0;\n    justify-content: center;\n    border-top: 1px solid #1A1A1A;\n    border-bottom: 1px solid #1A1A1A;\n    width: 100%;\n    padding: 10px 0;\n}",
    css, count=1
)

css = re.sub(
    r"\.logo\s*\{[^}]+\}",
    ".logo {\n    font-family: 'Playfair Display', serif;\n    font-size: 4em;\n    font-weight: 700;\n    color: #1A1A1A;\n    text-decoration: none;\n    text-transform: uppercase;\n    letter-spacing: 4px;\n    line-height: 1;\n    margin-bottom: 10px;\n}",
    css, count=1
)

# Add .brief-list styling
if ".brief-list" not in css:
    css += """\n
/* --- Brief List Styling --- */
.brief-list {
    list-style-type: none;
    padding-left: 0;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}
.brief-item {
    border: 1px solid #1A1A1A;
    padding: 20px;
    background-color: transparent;
    display: flex;
    flex-direction: column;
}
.brief-link {
    font-size: 1.5em;
    font-weight: bold;
    color: #1A1A1A;
    text-decoration: none;
    font-family: 'Playfair Display', serif;
    margin-bottom: 10px;
}
.brief-link:hover {
    color: #2D4B73;
    text-decoration: underline;
}
.brief-meta {
    font-family: 'Special Elite', monospace;
    font-size: 0.8em;
    color: #6c757d;
}
"""

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

print("CSS updated successfully")
