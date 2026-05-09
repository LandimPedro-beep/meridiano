import json
import logging
import re
from datetime import datetime
from urllib.parse import urljoin

import requests
import trafilatura
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger()


SCIENCE_DOMAIN_RULES = [
    ("bioquímica", ["biochem", "biochemistry", "enzym", "metabol", "proteom", "molecular biology"]),
    ("biologia molecular", ["molecular biology", "gene", "genomic", "rna", "dna", "protein"]),
    ("química orgânica", ["organic chemistry", "organometallic", "synthesis", "catalysis", "heterocycle"]),
    ("química inorgânica", ["inorganic chemistry", "coordination", "metal complex", "solid state"]),
    ("química analítica", ["analytical chemistry", "spectrometry", "chromatography", "sensor", "assay"]),
    ("físico-química", ["physical chemistry", "thermodynamics", "kinetics", "electrochem", "spectroscopy"]),
    ("química de materiais", ["materials", "nanoparticle", "polymer", "crystal", "surface"]),
]


# Helper function for date formatting (optional but nice)
def format_datetime(value, format="%Y-%m-%d %H:%M"):
    if value is None:
        return "N/A"
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except ValueError:
            return value  # Return original string if parsing fails
    if isinstance(value, datetime):
        return value.strftime(format)
    return value


def _normalize_whitespace(value):
    if not value:
        return None
    return re.sub(r"\s+", " ", str(value)).strip() or None


def _get_meta_content(soup, *selectors):
    for attrs in selectors:
        tag = soup.find("meta", attrs=attrs)
        if tag and tag.get("content"):
            content = _normalize_whitespace(tag.get("content"))
            if content:
                return content
    return None


def _get_meta_list(soup, *selectors):
    values = []
    for attrs in selectors:
        for tag in soup.find_all("meta", attrs=attrs):
            content = _normalize_whitespace(tag.get("content"))
            if content and content not in values:
                values.append(content)
    return values


def _safe_parse_date(value):
    if not value:
        return None

    candidate = _normalize_whitespace(value)
    if not candidate:
        return None

    candidate = candidate.replace("Z", "+00:00")
    for parser in (datetime.fromisoformat,):
        try:
            return parser(candidate)
        except ValueError:
            pass

    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", candidate)
    if date_match:
        try:
            return datetime.fromisoformat(date_match.group(1))
        except ValueError:
            return None
    return None


def _extract_json_ld_objects(soup):
    objects = []
    for tag in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw_json = tag.string or tag.get_text()
        if not raw_json:
            continue
        try:
            parsed = json.loads(raw_json.strip())
        except Exception:
            continue
        if isinstance(parsed, list):
            objects.extend(parsed)
        else:
            objects.append(parsed)
    return objects


def _extract_authors_from_json_ld(objects):
    authors = []
    for obj in objects:
        if not isinstance(obj, dict):
            continue
        author_value = obj.get("author")
        if isinstance(author_value, list):
            for item in author_value:
                if isinstance(item, dict):
                    name = _normalize_whitespace(item.get("name"))
                    if name and name not in authors:
                        authors.append(name)
                else:
                    name = _normalize_whitespace(item)
                    if name and name not in authors:
                        authors.append(name)
        elif isinstance(author_value, dict):
            name = _normalize_whitespace(author_value.get("name"))
            if name and name not in authors:
                authors.append(name)
        else:
            name = _normalize_whitespace(author_value)
            if name and name not in authors:
                authors.append(name)
    return authors


def _extract_first_json_ld_value(objects, *path_options):
    for obj in objects:
        if not isinstance(obj, dict):
            continue
        for path in path_options:
            current = obj
            found = True
            for key in path:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    found = False
                    break
            if found:
                if isinstance(current, dict):
                    current = current.get("name") or current.get("@type")
                value = _normalize_whitespace(current)
                if value:
                    return value
    return None


def _infer_article_type(article_type, title, abstract, journal_name):
    haystack = " ".join(filter(None, [article_type, title, abstract, journal_name])).lower()
    if not haystack:
        return None, None
    if "review" in haystack:
        return "review", True
    if "perspective" in haystack:
        return "perspective", False
    if "editorial" in haystack:
        return "editorial", False
    if "case report" in haystack:
        return "case_report", False
    if "protocol" in haystack:
        return "protocol", False
    return _normalize_whitespace(article_type), False


def _infer_scientific_domain(title, abstract, journal_name, url):
    haystack = " ".join(filter(None, [title, abstract, journal_name, url])).lower()
    if not haystack:
        return None, None

    for domain, keywords in SCIENCE_DOMAIN_RULES:
        if any(keyword in haystack for keyword in keywords):
            return "química", domain
    if "chem" in haystack or "quím" in haystack:
        return "química", None
    if "biology" in haystack or "biolog" in haystack:
        return "biologia", None
    return None, None


def extract_scientific_metadata(url, html_content, soup=None):
    """Extracts lightweight scientific metadata from article HTML."""
    soup = soup or BeautifulSoup(html_content, "lxml")
    json_ld_objects = _extract_json_ld_objects(soup)

    title = _normalize_whitespace(
        _get_meta_content(soup, {"property": "og:title"}, {"name": "dc.Title"}, {"name": "citation_title"})
    )
    if not title and soup.title and soup.title.string:
        title = _normalize_whitespace(soup.title.string)

    doi = _normalize_whitespace(
        _get_meta_content(
            soup,
            {"name": "citation_doi"},
            {"name": "dc.Identifier"},
            {"name": "prism.doi"},
            {"property": "article:doi"},
        )
    )
    if doi and doi.lower().startswith("doi:"):
        doi = doi[4:].strip()
    if not doi:
        doi_match = re.search(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", html_content, flags=re.IGNORECASE)
        if doi_match:
            doi = doi_match.group(0)

    journal_name = _normalize_whitespace(
        _get_meta_content(
            soup,
            {"name": "citation_journal_title"},
            {"name": "prism.publicationName"},
            {"name": "dc.Source"},
            {"property": "og:site_name"},
        )
    ) or _extract_first_json_ld_value(json_ld_objects, ("isPartOf", "name"), ("publisher", "name"))

    abstract = clean_html_to_text(
        _get_meta_content(
            soup,
            {"name": "citation_abstract"},
            {"name": "description"},
            {"property": "og:description"},
            {"name": "dc.Description"},
        )
    ) or _extract_first_json_ld_value(json_ld_objects, ("description",))

    authors = _get_meta_list(soup, {"name": "citation_author"}, {"name": "dc.Creator"}, {"name": "author"})
    if not authors:
        authors = _extract_authors_from_json_ld(json_ld_objects)

    raw_article_type = _normalize_whitespace(
        _get_meta_content(
            soup,
            {"name": "citation_article_type"},
            {"name": "dc.Type"},
        )
    ) or _extract_first_json_ld_value(json_ld_objects, ("@type",))

    publication_date_verified = (
        _safe_parse_date(
            _get_meta_content(
                soup,
                {"name": "citation_publication_date"},
                {"name": "citation_online_date"},
                {"name": "dc.Date"},
                {"name": "prism.publicationDate"},
                {"property": "article:published_time"},
                {"property": "og:published_time"},
            )
        )
        or _safe_parse_date(_extract_first_json_ld_value(json_ld_objects, ("datePublished",)))
    )
    publication_year = publication_date_verified.year if publication_date_verified else None

    article_type, is_review = _infer_article_type(raw_article_type, title, abstract, journal_name)
    scientific_domain, subdomain = _infer_scientific_domain(title, abstract, journal_name, url)

    non_empty_fields = sum(
        1
        for value in [title, doi, journal_name, abstract, authors, article_type, publication_date_verified, scientific_domain]
        if value
    )
    metadata_status = "publisher_metadata_extracted" if non_empty_fields >= 3 else "publisher_metadata_partial"

    return {
        "title": title,
        "doi": doi,
        "journal_name": journal_name,
        "authors": authors,
        "abstract": abstract,
        "article_type": article_type,
        "publication_date_verified": publication_date_verified,
        "publication_year": publication_year,
        "is_review": is_review,
        "scientific_domain": scientific_domain,
        "subdomain": subdomain,
        "metadata_status": metadata_status,
    }


def fetch_article_content_and_og_image(url):
    """
    Fetches HTML, extracts main content using Trafilatura,
    and extracts the og:image URL using BeautifulSoup.

    Returns:
        dict: {'content': str|None, 'og_image': str|None, 'metadata': dict}
    """
    content = None
    og_image = None
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
            "referer": "https://www.google.com",
        }
        response = requests.get(url, headers=headers, timeout=20)  # Increased timeout slightly
        response.raise_for_status()
        html_content = response.text

        # 1. Extract text content
        content = trafilatura.extract(html_content, include_comments=False, include_tables=False)

        # 2. Extract og:image and scientific metadata
        soup = BeautifulSoup(html_content, "lxml")  # Use lxml or html.parser
        og_image_tag = soup.find("meta", property="og:image")
        if og_image_tag and og_image_tag.get("content"):
            og_image = og_image_tag["content"]
            # Optionally resolve relative URLs - less common for og:image but possible
            og_image = urljoin(url, og_image)

        metadata = extract_scientific_metadata(url, html_content, soup=soup)

        return {"content": content, "og_image": og_image, "metadata": metadata}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return {"content": None, "og_image": None, "metadata": {}}
    except Exception as e:
        # Catch potential BeautifulSoup errors or others
        print(f"Error processing content/og:image from {url}: {e}")
        # Still return content if it was extracted before the error
        return {"content": content, "og_image": None, "metadata": {}}


def clean_html_to_text(value):
    """Best-effort conversion of small HTML snippets from RSS fields to plain text."""
    if not value:
        return None
    text = BeautifulSoup(value, "lxml").get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


def scrape_single_article_details(article_url):
    """
    Fetches and extracts details (title, raw_content, image_url) for a single article URL.

    Args:
        article_url (str): The URL of the article to scrape.

    Returns:
        dict: {'title': str|None, 'raw_content': str|None, 'image_url': str|None, 'error': str|None}
              'error' key will be present if fetching/processing failed.
    """
    print(f"Attempting to scrape single article: {article_url}")
    fetched_title = None
    raw_content = None
    final_image_url = None
    error_message = None

    try:
        # Use the existing fetch_article_content_and_og_image helper
        fetch_result = fetch_article_content_and_og_image(article_url)  # This already logs its own errors

        raw_content = fetch_result["content"]
        og_image_url = fetch_result["og_image"]

        if not raw_content:
            # fetch_article_content_and_og_image might have already logged, but good to have a specific error here
            error_message = "Failed to extract main content from the article."
            logger.warning(f"{error_message} URL: {article_url}")
            # Even if content fails, we might still get a title or image from OG tags if fetch worked partially
            # So, continue to try and extract title if possible.

        # --- Attempt to get a title from the page if not from RSS ---
        # We need to re-fetch or use the already fetched HTML if available from fetch_article_content_and_og_image
        # Let's assume fetch_article_content_and_og_image doesn't return the full soup object.
        # If it did, we could reuse it. For now, we might need a minimal re-fetch or a helper modification.
        # Simplification: If trafilatura got content, it often implies page was fetched.
        # We could parse the title from the raw_content's source HTML (if fetch_... stored it)
        # or do another small HEAD request or parse from a snippet.
        # For now, we'll use a placeholder if the feed didn't provide it.
        # A more robust solution would be to enhance fetch_article_content_and_og_image
        # to also return the <title> tag content.

        if raw_content:  # If we got content, try to get title from HTML
            try:
                # Need to parse the HTML again if not already available from previous fetch
                headers = {"User-Agent": "Mozilla/5.0 ..."}  # Your headers
                response = requests.get(article_url, headers=headers, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "lxml")
                title_tag = soup.find("title")
                if title_tag and title_tag.string:
                    fetched_title = title_tag.string.strip()
                # Fallback to OG title if HTML title is poor/missing
                if not fetched_title:
                    og_title_tag = soup.find("meta", property="og:title")
                    if og_title_tag and og_title_tag.get("content"):
                        fetched_title = og_title_tag["content"].strip()
            except Exception as title_e:
                logger.warning(f"Could not extract title for {article_url}: {title_e}")
                # Continue without title if it fails

        final_image_url = og_image_url  # For a single manual add, OG image is the primary target
        metadata = fetch_result.get("metadata") or {}
        if not fetched_title:
            fetched_title = metadata.get("title")

        if not raw_content and not fetched_title and not final_image_url:
            # If absolutely nothing was fetched, it's a more significant error
            error_message = "Failed to fetch any content, title, or image from the URL."

    except Exception as e:
        error_message = f"General error scraping single article {article_url}: {e}"
        logger.error(error_message, exc_info=True)

    return {
        "title": fetched_title,
        "raw_content": raw_content,
        "image_url": final_image_url,
        "metadata": metadata if "metadata" in locals() else {},
        "error": error_message,
    }
