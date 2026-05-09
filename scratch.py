import os
import re

css_path = r"c:\Users\pedro\meridiano\src\meridiano\static\css\style.css"

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

css = re.sub(
    r"\.container\s*\{[^}]+\}",
    ".container {\n    max-width: 1400px;\n    width: 95%;\n    margin: 0 auto;\n    padding: 30px 15px;\n    background-color: transparent;\n    border: none;\n    box-shadow: none;\n}",
    css, count=1
)

css = re.sub(
    r"\.header-content\s*\{[^}]+\}",
    ".header-content {\n    max-width: 1400px;\n    margin: 0 auto;\n    display: flex;\n    justify-content: space-between;\n    align-items: center;\n}",
    css, count=1
)

css = re.sub(
    r"/\* --- Article List Styling ---\s*\*/\s*\.article-list\s*\{[^}]+\}",
    "/* --- Article List Styling --- */\n.article-list {\n    list-style-type: none;\n    padding-left: 0;\n    margin-top: 30px;\n    display: grid;\n    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));\n    gap: 30px;\n    align-items: start;\n}",
    css
)

css = re.sub(
    r"\.article-item\s*\{[^}]+\}\s*\.article-item:last-child\s*\{[^}]+\}",
    ".article-item {\n    margin-bottom: 0;\n    padding-bottom: 20px;\n    border-bottom: 1px solid #1A1A1A;\n    display: flex;\n    flex-direction: column;\n    height: 100%;\n}\n.article-item:last-child {\n    border-bottom: 1px solid #1A1A1A;\n}",
    css, count=1
)

css = re.sub(
    r"/\* --- Article List Image Styling ---\s*\*/\s*\.article-item\s*\{[^}]+\}\s*\.article-item:last-child\s*\{[^}]+\}",
    "/* --- Article List Image Styling --- */\n/* overridden for grid */",
    css
)

css = re.sub(
    r"\.article-image-container\s*\{[^}]+\}",
    ".article-image-container {\n    width: 100%;\n    height: 200px;\n    margin-bottom: 15px;\n    border-radius: 0;\n    border: 1px solid #1A1A1A;\n    flex-shrink: 0;\n}",
    css, count=1
)

css = re.sub(
    r"\.filter-sort-form\s*\{[^}]+\}",
    ".filter-sort-form {\n    display: flex;\n    flex-direction: row;\n    flex-wrap: wrap;\n    gap: 20px;\n    margin-bottom: 30px;\n    padding: 20px;\n    background-color: transparent;\n    border-top: 2px solid #1A1A1A;\n    border-bottom: 2px solid #1A1A1A;\n    border-radius: 0;\n    align-items: center;\n}",
    css, count=1
)

css = re.sub(
    r"\.search-filter\s*\{[^}]+\}",
    ".search-filter {\n    display: flex;\n    align-items: center;\n    flex-grow: 1;\n    background-color: transparent;\n    border: 1px solid #1A1A1A;\n    border-radius: 0;\n    padding: 0px 5px 0px 12px;\n    box-shadow: none;\n}",
    css, count=1
)

# Replace profile blocks (Vetor, Matriz, Esfera)
vetor_pattern = r"/\* Vetor Profile[^*]+\*/\s*\.profile-vetor\s*\{[^}]+\}\s*\.profile-vetor\s*\.article-image-container\s*\{[^}]+\}\s*\.profile-vetor\s*\.article-image\s*\{[^}]+\}\s*\.profile-vetor\s*\.article-link-wrapper\s*\{[^}]+\}\s*\.profile-vetor\s*\.article-link\s*\{[^}]+\}\s*\.profile-vetor\s*\.article-text-content\s*\{[^}]+\}\s*\.profile-vetor\s*\.marginalia-ai-summary\s*\{[^}]+\}"

vetor_replacement = """/* Vetor Profile (Manchete principal) */
.profile-vetor {
    grid-column: 1 / -1;
    display: flex;
    flex-direction: row;
    gap: 30px;
    border-bottom: 3px double #1A1A1A;
    padding-bottom: 20px;
    margin-bottom: 0;
}
.profile-vetor .article-image-container {
    width: 50%;
    height: auto;
    max-height: 400px;
    margin-bottom: 0;
    border-radius: 0;
    border: 1px solid #1A1A1A;
    flex-shrink: 0;
}
.profile-vetor .article-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 0;
}
.profile-vetor .article-link-wrapper {
    text-align: left;
    margin-bottom: 15px;
    column-span: all;
}
.profile-vetor .article-link {
    font-size: 2.5em;
    line-height: 1.1;
}
.profile-vetor .article-text-content {
    width: 50%;
    column-count: 2;
    column-gap: 20px;
    column-rule: 1px solid #D1D1D1;
    text-align: justify;
}
.profile-vetor .marginalia-ai-summary {
    float: none;
    width: 100%;
    column-span: all;
    border-left: none;
    border-top: 1px dashed #1A1A1A;
    margin-left: 0;
    transform: none;
    margin-top: 15px;
}"""
css = re.sub(vetor_pattern, vetor_replacement, css)


matriz_esfera_pattern = r"/\* Matriz Profile[^*]+\*/\s*\.profile-matriz\s*\{[^}]+\}\s*\.profile-matriz\s*\.article-link\s*\{[^}]+\}\s*\.profile-matriz\s*\.article-meta\s*\{[^}]+\}\s*\.profile-matriz\s*\.marginalia-ai-summary\s*\{[^}]+\}\s*/\* Horizonte / Esfera Profile[^*]+\*/\s*\.profile-horizonte,\s*\.profile-esfera\s*\{[^}]+\}\s*\.profile-horizonte\s*\.article-image-container,\s*\.profile-esfera\s*\.article-image-container\s*\{[^}]+\}\s*\.profile-horizonte\s*\.article-text-content,\s*\.profile-esfera\s*\.article-text-content\s*\{[^}]+\}"

matriz_esfera_replacement = """/* Matriz Profile (Ficha catalográfica) */
.profile-matriz {
    display: flex;
    flex-direction: column;
    border: 2px solid #1A1A1A;
    padding: 20px;
    background-color: transparent;
    box-shadow: 4px 4px 0px rgba(26, 26, 26, 0.2);
    margin-bottom: 0;
    align-items: flex-start;
}
.profile-matriz .article-link {
    font-family: 'Special Elite', monospace;
    text-transform: uppercase;
    font-size: 1.2em;
    letter-spacing: 1px;
}
.profile-matriz .article-meta {
    font-family: 'Special Elite', monospace;
    display: inline-block;
    border: 1px solid #1A1A1A;
    padding: 3px 8px;
    margin-top: 10px;
    background-color: transparent;
}
.profile-matriz .marginalia-ai-summary {
    float: none;
    width: 100%;
    border-left: none;
    border-top: 2px solid #1A1A1A;
    margin-top: 15px;
    margin-left: 0;
    transform: none;
    padding-left: 0;
}

/* Horizonte / Esfera Profile (Panorama denso) */
.profile-horizonte, .profile-esfera {
    display: flex;
    flex-direction: column;
    border-top: 2px solid #1A1A1A;
    border-bottom: 2px solid #1A1A1A;
    padding: 15px 0;
    margin-bottom: 0; 
}
.profile-horizonte .article-image-container, .profile-esfera .article-image-container {
    width: 100%;
    height: 150px;
    border-radius: 0;
    border: 1px solid #1A1A1A;
    margin-bottom: 10px;
}
.profile-horizonte .article-text-content, .profile-esfera .article-text-content {
    font-size: 1em;
    text-align: justify;
}"""
css = re.sub(matriz_esfera_pattern, matriz_esfera_replacement, css)

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

print("CSS updated successfully")
