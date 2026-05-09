"""
Database operations using SQLModel for the Meridiano application.
This replaces the SQLite-based database.py with modern SQLModel operations.
"""

import json
import logging
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy import case, text
from sqlalchemy.exc import IntegrityError
from sqlmodel import and_, asc, desc, func, or_, select

from . import config_base as config
from .models import (
    Article,
    Brief,
    Collection,
    CollectionArticle,
    FeedScrapeMetric,
    get_session,
)
from .models import init_db as model_init_db

logger = logging.getLogger(__name__)

ARTICLES_PER_PAGE_DEFAULT = 25


def get_db_connection():
    """Returns a new database session (replaces SQLite connection)"""
    return get_session()


def init_db():
    """Initialize the database - create all tables"""

    model_init_db()


def get_unrated_articles(feed_profile: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Gets processed articles that haven't been rated yet."""
    with get_session() as session:
        statement = (
            select(Article)
            .where(
                and_(
                    Article.processed_content.is_not(None),
                    Article.processed_content != "",
                    Article.processed_at.is_not(None),
                    Article.impact_score.is_(None),
                    Article.feed_profile == feed_profile,
                )
            )
            .order_by(desc(Article.processed_at))
            .limit(limit)
        )

        articles = session.exec(statement).all()
        return [_article_to_dict(article) for article in articles]


def update_article_rating(article_id: int, impact_score: int) -> None:
    """Updates an article with its impact score."""
    with get_session() as session:
        statement = select(Article).where(Article.id == article_id)
        article = session.exec(statement).first()
        if article:
            article.impact_score = impact_score
            session.add(article)
            session.commit()


def get_article_by_id(article_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves all data for a specific article by its ID."""
    with get_session() as session:
        statement = select(Article).where(Article.id == article_id)
        article = session.exec(statement).first()
        return _article_to_dict(article) if article else None


def _article_to_dict(article: Article) -> Dict[str, Any]:
    """Convert Article model to dictionary for compatibility with existing code."""
    if not article:
        return None

    return article.model_dump(
        include={
            "id",
            "url",
            "title",
            "published_date",
            "publication_date_verified",
            "publication_year",
            "feed_source",
            "rss_feed_url",
            "editorial_block",
            "fetched_at",
            "scrape_status",
            "metadata_status",
            "metadata_extracted_at",
            "raw_content",
            "abstract",
            "processed_content",
            "embedding",
            "processed_at",
            "llm_stage_version",
            "keyword_labels",
            "keyword_match",
            "keyword_checked_at",
            "doi",
            "journal_name",
            "authors",
            "article_type",
            "citation_count",
            "citation_source",
            "is_review",
            "scientific_domain",
            "subdomain",
            "cluster_id",
            "impact_score",
            "relevance_score",
            "novelty_score",
            "canonical_score",
            "novelty_window_match",
            "matrix_window_match",
            "eligibility_status",
            "eligibility_reason",
            "image_url",
            "feed_profile",
        }
    )


def _brief_to_dict(brief: Brief) -> Dict[str, Any]:
    """Convert Brief model to dictionary for compatibility with existing code."""
    if not brief:
        return None

    return brief.model_dump(
        include={
            "id",
            "generated_at",
            "brief_markdown",
            "contributing_article_ids",
            "feed_profile",
        }
    )


def _build_article_filters(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    feed_profile: Optional[str] = None,
):
    """Helper for building filter conditions for articles."""
    filters = []

    if start_date:
        filters.append(func.date(Article.published_date) >= func.date(start_date))
    if end_date:
        filters.append(func.date(Article.published_date) <= func.date(end_date))
    if feed_profile:
        filters.append(Article.feed_profile == feed_profile)

    return filters


def get_all_articles(
    page: int = 1,
    per_page: int = ARTICLES_PER_PAGE_DEFAULT,
    sort_by: str = "published_date",
    direction: str = "desc",
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    feed_profile: Optional[str] = None,
    search_term: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Fetches articles with filtering, sorting, and full-text search.
    Uses PostgreSQL full-text search when available, falls back to LIKE search.
    """
    with get_session() as session:
        # Start with base query
        statement = select(Article)

        # Apply basic filters
        filters = _build_article_filters(start_date, end_date, feed_profile)
        if filters:
            statement = statement.where(and_(*filters))

        # Apply search if provided
        if search_term:
            if "postgresql" in config.DATABASE_URL.lower():
                # PostgreSQL full-text search
                search_vector = func.to_tsvector(
                    "english",
                    func.coalesce(Article.title, "") + " " + func.coalesce(Article.raw_content, ""),
                )
                # Use SQLAlchemy's match with a plain string and specify the Postgres
                # text search configuration to avoid nesting plainto_tsquery calls.
                statement = statement.where(search_vector.match(search_term, postgresql_regconfig="english"))
            else:
                # Fallback to LIKE search for SQLite
                search_filter = or_(
                    Article.title.ilike(f"%{search_term}%"),
                    Article.raw_content.ilike(f"%{search_term}%"),
                )
                statement = statement.where(search_filter)

        # Apply sorting
        sort_columns = {
            "published_date": Article.published_date,
            "impact_score": Article.impact_score,
            "fetched_at": Article.fetched_at,
        }

        sort_column = sort_columns.get(sort_by, Article.published_date)
        if direction.lower() == "asc":
            statement = statement.order_by(asc(sort_column), desc(Article.id))
        else:
            statement = statement.order_by(desc(sort_column), desc(Article.id))

        # Apply pagination
        offset = (page - 1) * per_page
        statement = statement.offset(offset).limit(per_page)

        articles = session.exec(statement).all()
        return [_article_to_dict(article) for article in articles]


def get_total_article_count(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    feed_profile: Optional[str] = None,
    search_term: Optional[str] = None,
) -> int:
    """Returns total count of articles with optional filtering and search."""
    with get_session() as session:
        # Start with base query
        statement = select(func.count(Article.id))

        # Apply basic filters
        filters = _build_article_filters(start_date, end_date, feed_profile)
        if filters:
            statement = statement.where(and_(*filters))

        # Apply search if provided
        if search_term:
            if "postgresql" in config.DATABASE_URL.lower():
                # PostgreSQL full-text search
                search_vector = func.to_tsvector(
                    "english",
                    func.coalesce(Article.title, "") + " " + func.coalesce(Article.raw_content, ""),
                )
                # Use SQLAlchemy's match with a plain string and specify the Postgres
                # text search configuration to avoid nesting plainto_tsquery calls.
                statement = statement.where(search_vector.match(search_term, postgresql_regconfig="english"))
            else:
                # Fallback to LIKE search
                search_filter = or_(
                    Article.title.ilike(f"%{search_term}%"),
                    Article.raw_content.ilike(f"%{search_term}%"),
                )
                statement = statement.where(search_filter)

        return session.exec(statement).one()


def add_article(
    url: str,
    title: str,
    published_date: datetime,
    feed_source: str,
    raw_content: Optional[str],
    feed_profile: str,
    image_url: Optional[str] = None,
    rss_feed_url: Optional[str] = None,
    publication_date_verified: Optional[datetime] = None,
    publication_year: Optional[int] = None,
    editorial_block: Optional[str] = None,
    scrape_status: Optional[str] = None,
    metadata_status: Optional[str] = None,
    abstract: Optional[str] = None,
    novelty_window_match: Optional[bool] = None,
    matrix_window_match: Optional[bool] = None,
    eligibility_status: Optional[str] = None,
    eligibility_reason: Optional[str] = None,
) -> Optional[int]:
    """Adds a new article with optional image URL."""
    with get_session() as session:
        try:
            # Ensure Postgres sequence is in sync to avoid duplicate primary key errors
            if "postgresql" in config.DATABASE_URL.lower():
                try:
                    # Sync the sequence to the current max(id) so nextval() will produce a fresh value.
                    session.exec(
                        text(
                            "SELECT setval("
                            "pg_get_serial_sequence('articles','id'), "
                            "COALESCE((SELECT MAX(id) FROM articles), 1))"
                        )
                    )
                except Exception as e:
                    # Log warning but continue - this is usually non-critical for new inserts
                    logger.warning(f"PostgreSQL sequence sync warning (non-critical): {e}")
                    # Continue - this is usually fine for new inserts

            article = Article(
                url=url,
                title=title,
                published_date=published_date,
                publication_date_verified=publication_date_verified or published_date,
                publication_year=publication_year if publication_year is not None else (published_date.year if published_date else None),
                feed_source=feed_source,
                rss_feed_url=rss_feed_url,
                editorial_block=editorial_block or feed_profile,
                raw_content=raw_content,
                abstract=abstract,
                image_url=image_url,
                feed_profile=feed_profile,
                fetched_at=datetime.now(),
                scrape_status=scrape_status or ("scraped" if raw_content else "metadata_only"),
                metadata_status=metadata_status or "raw_scrape",
                metadata_extracted_at=datetime.now(),
                novelty_window_match=novelty_window_match,
                matrix_window_match=matrix_window_match,
                eligibility_status=eligibility_status,
                eligibility_reason=eligibility_reason,
            )
            session.add(article)
            session.commit()
            session.refresh(article)  # Get the ID
            print(f"Added article [{feed_profile}]: {title}")
            return article.id
        except IntegrityError:
            session.rollback()
            return None


def get_articles_pending_content_scrape(
    feed_profile: str,
    limit: int = 50,
    require_keyword_match: bool = True,
) -> List[Dict[str, Any]]:
    """Gets eligible articles that still need the expensive full-content scrape."""
    with get_session() as session:
        filters = [
            Article.feed_profile == feed_profile,
            Article.eligibility_status == "eligible",
            or_(Article.raw_content.is_(None), Article.raw_content == ""),
        ]
        if require_keyword_match:
            filters.append(Article.keyword_match.is_(True))

        statement = select(Article).where(and_(*filters)).order_by(desc(Article.published_date), desc(Article.fetched_at)).limit(limit)
        articles = session.exec(statement).all()
        return [_article_to_dict(article) for article in articles]


def update_article_content_scrape(
    article_id: int,
    raw_content: Optional[str],
    image_url: Optional[str] = None,
    abstract: Optional[str] = None,
    scrape_status: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """Stores results from the expensive full-article scrape stage."""
    with get_session() as session:
        statement = select(Article).where(Article.id == article_id)
        article = session.exec(statement).first()
        if article:
            metadata = metadata or {}
            article.raw_content = raw_content
            if image_url:
                article.image_url = image_url
            resolved_abstract = metadata.get("abstract") or abstract
            if resolved_abstract and not article.abstract:
                article.abstract = resolved_abstract
            resolved_title = metadata.get("title")
            if resolved_title and (not article.title or article.title.startswith("Manually Added")):
                article.title = resolved_title
            if metadata.get("doi"):
                article.doi = metadata["doi"]
            if metadata.get("journal_name"):
                article.journal_name = metadata["journal_name"]
            if metadata.get("authors"):
                article.authors = json.dumps(metadata["authors"], ensure_ascii=False)
            if metadata.get("article_type"):
                article.article_type = metadata["article_type"]
            if metadata.get("publication_date_verified"):
                article.publication_date_verified = metadata["publication_date_verified"]
            if metadata.get("publication_year") is not None:
                article.publication_year = metadata["publication_year"]
            if metadata.get("is_review") is not None:
                article.is_review = metadata["is_review"]
            if metadata.get("scientific_domain"):
                article.scientific_domain = metadata["scientific_domain"]
            if metadata.get("subdomain"):
                article.subdomain = metadata["subdomain"]
            if "novelty_window_match" in metadata:
                article.novelty_window_match = metadata.get("novelty_window_match")
            if "matrix_window_match" in metadata:
                article.matrix_window_match = metadata.get("matrix_window_match")
            if metadata.get("eligibility_status"):
                article.eligibility_status = metadata["eligibility_status"]
            if metadata.get("eligibility_reason"):
                article.eligibility_reason = metadata["eligibility_reason"]
            if metadata.get("editorial_block"):
                article.editorial_block = metadata["editorial_block"]
            article.metadata_status = metadata.get("metadata_status") or article.metadata_status or "rss_ingested"
            article.metadata_extracted_at = datetime.now()
            article.scrape_status = scrape_status or ("scraped" if raw_content else "scrape_failed")
            session.add(article)
            session.commit()


def record_feed_scrape_metric(
    scrape_run_id: str,
    feed_profile: str,
    rss_feed_url: str,
    feed_source: Optional[str],
    detected_count: int,
    duplicate_count: int,
    scrape_success_count: int,
    scrape_failed_count: int,
) -> int:
    """Persists scrape-stage metrics for one RSS feed in one scrape run."""
    with get_session() as session:
        metric = FeedScrapeMetric(
            scrape_run_id=scrape_run_id,
            feed_profile=feed_profile,
            rss_feed_url=rss_feed_url,
            feed_source=feed_source,
            detected_count=detected_count,
            duplicate_count=duplicate_count,
            scrape_success_count=scrape_success_count,
            scrape_failed_count=scrape_failed_count,
            recorded_at=datetime.now(),
        )
        session.add(metric)
        session.commit()
        session.refresh(metric)
        return metric.id


def get_latest_feed_feedback_summary(feed_profile: str) -> List[Dict[str, Any]]:
    """Returns per-feed confidence metrics from the latest scrape run plus current article state."""
    with get_session() as session:
        latest_run_id = session.exec(
            select(FeedScrapeMetric.scrape_run_id)
            .where(FeedScrapeMetric.feed_profile == feed_profile)
            .order_by(desc(FeedScrapeMetric.recorded_at))
            .limit(1)
        ).first()

        latest_metrics = {}
        if latest_run_id:
            metric_rows = session.exec(
                select(FeedScrapeMetric).where(
                    and_(
                        FeedScrapeMetric.feed_profile == feed_profile,
                        FeedScrapeMetric.scrape_run_id == latest_run_id,
                    )
                )
            ).all()
            latest_metrics = {
                row.rss_feed_url: {
                    "scrape_run_id": row.scrape_run_id,
                    "last_scrape_at": row.recorded_at,
                    "detected_count": row.detected_count,
                    "duplicate_count": row.duplicate_count,
                    "scrape_success_count": row.scrape_success_count,
                    "scrape_failed_count": row.scrape_failed_count,
                    "feed_source": row.feed_source,
                }
                for row in metric_rows
            }

        article_rows = session.exec(
            select(
                Article.rss_feed_url,
                func.max(Article.feed_source),
                func.count(Article.id),
                func.sum(case((Article.processed_at.is_not(None), 1), else_=0)),
                func.sum(case((Article.keyword_match.is_(True), 1), else_=0)),
                func.sum(case((Article.keyword_match.is_(False), 1), else_=0)),
            )
            .where(Article.feed_profile == feed_profile)
            .group_by(Article.rss_feed_url)
        ).all()

        summary_by_feed = {}
        for rss_feed_url, feed_source, stored_count, processed_count, approved_count, rejected_count in article_rows:
            if not rss_feed_url:
                continue
            summary_by_feed[rss_feed_url] = {
                "feed_profile": feed_profile,
                "rss_feed_url": rss_feed_url,
                "feed_source": feed_source,
                "scrape_run_id": None,
                "last_scrape_at": None,
                "detected_count": 0,
                "duplicate_count": 0,
                "scrape_success_count": 0,
                "scrape_failed_count": 0,
                "stored_count": stored_count or 0,
                "processed_count": processed_count or 0,
                "keyword_accepted_count": approved_count or 0,
                "keyword_rejected_count": rejected_count or 0,
            }

        for rss_feed_url, metric in latest_metrics.items():
            row = summary_by_feed.setdefault(
                rss_feed_url,
                {
                    "feed_profile": feed_profile,
                    "rss_feed_url": rss_feed_url,
                    "feed_source": metric.get("feed_source"),
                    "scrape_run_id": None,
                    "last_scrape_at": None,
                    "detected_count": 0,
                    "duplicate_count": 0,
                    "scrape_success_count": 0,
                    "scrape_failed_count": 0,
                    "stored_count": 0,
                    "processed_count": 0,
                    "keyword_accepted_count": 0,
                    "keyword_rejected_count": 0,
                },
            )
            row.update(metric)
            if not row.get("feed_source"):
                row["feed_source"] = metric.get("feed_source")

        return sorted(summary_by_feed.values(), key=lambda item: item["rss_feed_url"])


def get_unprocessed_articles(feed_profile: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Gets keyword-approved articles that haven't been processed yet."""
    with get_session() as session:
        statement = (
            select(Article)
            .where(
                and_(
                    Article.processed_at.is_(None),
                    or_(
                        and_(Article.raw_content.is_not(None), Article.raw_content != ""),
                        and_(Article.abstract.is_not(None), Article.abstract != ""),
                    ),
                    Article.keyword_match.is_(True),
                    Article.feed_profile == feed_profile,
                )
            )
            .order_by(desc(Article.fetched_at))
            .limit(limit)
        )

        articles = session.exec(statement).all()
        return [_article_to_dict(article) for article in articles]


def get_articles_for_keyword_filter(feed_profile: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Gets articles that still need keyword labeling/filtering."""
    with get_session() as session:
        statement = (
            select(Article)
            .where(
                and_(
                    Article.keyword_checked_at.is_(None),
                    Article.eligibility_status == "eligible",
                    Article.title.is_not(None),
                    Article.title != "",
                    Article.feed_profile == feed_profile,
                )
            )
            .order_by(desc(Article.published_date), desc(Article.fetched_at))
            .limit(limit)
        )

        articles = session.exec(statement).all()
        return [_article_to_dict(article) for article in articles]


def update_article_keyword_filter(article_id: int, labels: List[str], matched: bool) -> None:
    """Stores keyword labels and the filter decision for an article."""
    with get_session() as session:
        statement = select(Article).where(Article.id == article_id)
        article = session.exec(statement).first()
        if article:
            article.keyword_labels = json.dumps(labels, ensure_ascii=False)
            article.keyword_match = matched
            article.keyword_checked_at = datetime.now()
            session.add(article)
            session.commit()


def update_article_processing(article_id: int, processed_content: str, embedding: Optional[List[float]]) -> None:
    """Updates an article with its summary, embedding, and processed timestamp."""
    with get_session() as session:
        statement = select(Article).where(Article.id == article_id)
        article = session.exec(statement).first()
        if article:
            article.processed_content = processed_content
            article.embedding = json.dumps(embedding) if embedding else None
            article.processed_at = datetime.now()
            article.llm_stage_version = article.llm_stage_version or "v1"
            session.add(article)
            session.commit()


def get_articles_for_briefing(lookback_hours: int, feed_profile: str) -> List[Dict[str, Any]]:
    """Gets recently processed articles for a specific feed profile."""
    cutoff_time = datetime.now() - timedelta(hours=lookback_hours)

    with get_session() as session:
        statement = (
            select(Article)
            .where(
                and_(
                    Article.processed_at >= cutoff_time,
                    Article.embedding.is_not(None),
                    Article.feed_profile == feed_profile,
                )
            )
            .order_by(desc(Article.processed_at))
        )

        articles = session.exec(statement).all()
        return [_article_to_dict(article) for article in articles]


def save_brief(brief_markdown: str, contributing_article_ids: List[int], feed_profile: str) -> int:
    """Saves the generated brief including its feed profile."""
    with get_session() as session:
        ids_json = json.dumps(contributing_article_ids)
        brief = Brief(
            brief_markdown=brief_markdown,
            contributing_article_ids=ids_json,
            feed_profile=feed_profile,
            generated_at=datetime.now(),
        )

        # Guarantee unique and sequential id
        if "postgresql" in config.DATABASE_URL.lower():
            try:
                session.exec(
                    text(
                        "SELECT setval("
                        "pg_get_serial_sequence('briefs','id'), "
                        "COALESCE((SELECT MAX(id) FROM briefs), 1))"
                    )
                )
            except Exception:
                pass

        session.add(brief)
        session.commit()
        session.refresh(brief)  # Get the ID
        print(f"Saved brief [{feed_profile}] with ID: {brief.id}")
        return brief.id


def get_all_briefs_metadata(
    feed_profile: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Retrieves ID, timestamp, and profile for briefs, newest first, optionally filtered."""
    with get_session() as session:
        statement = select(Brief)

        if feed_profile:
            statement = statement.where(Brief.feed_profile == feed_profile)

        statement = statement.order_by(desc(Brief.generated_at))
        briefs = session.exec(statement).all()

        return [_brief_to_dict(brief) for brief in briefs]


def get_brief_by_id(brief_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves a specific brief's content and timestamp by its ID."""
    with get_session() as session:
        statement = select(Brief).where(Brief.id == brief_id)
        brief = session.exec(statement).first()
        return _brief_to_dict(brief) if brief else None


def get_distinct_feed_profiles(table: str = "articles") -> List[str]:
    """Gets a list of distinct feed_profile values from a table."""
    if table not in ["articles", "briefs"]:
        raise ValueError("Invalid table name for distinct profiles.")

    with get_session() as session:
        if table == "articles":
            statement = select(Article.feed_profile).distinct().order_by(Article.feed_profile)
            result = session.exec(statement).all()
        else:  # table == 'briefs'
            statement = select(Brief.feed_profile).distinct().order_by(Brief.feed_profile)
            result = session.exec(statement).all()

        return list(result)


# -------------------------
# Collections helpers
# -------------------------
def create_collection(name: str) -> int:
    """Create a new collection and return its ID."""
    with get_session() as session:
        coll = Collection(name=name, created_at=datetime.now(), archived=False)
        session.add(coll)
        session.commit()
        session.refresh(coll)
        return coll.id


def get_collections(archived: bool = False) -> List[Dict[str, Any]]:
    """Return available collections (id, name, created_at), filtered by archived status."""
    with get_session() as session:
        stmt = select(Collection).where(Collection.archived == archived).order_by(asc(Collection.name))
        cols = session.exec(stmt).all()
        return [{"id": c.id, "name": c.name, "created_at": c.created_at, "archived": c.archived} for c in cols]


def get_collection_by_id(collection_id: int) -> Optional[Dict[str, Any]]:
    """Return collection metadata by id."""
    with get_session() as session:
        stmt = select(Collection).where(Collection.id == collection_id)
        coll = session.exec(stmt).first()
        if not coll:
            return None
        return {"id": coll.id, "name": coll.name, "created_at": coll.created_at, "archived": coll.archived}


def toggle_collection_archive_status(collection_id: int) -> Optional[bool]:
    """
    Toggles the archived status of a collection.
    Returns the new archived status, or None if collection not found.
    """
    with get_session() as session:
        coll = session.get(Collection, collection_id)
        if not coll:
            return None

        coll.archived = not coll.archived
        session.add(coll)
        session.commit()
        session.refresh(coll)
        return coll.archived


def delete_collection(collection_id: int) -> None:
    """Deletes a collection and all its article associations."""
    with get_session() as session:
        # First, delete associations
        stmt_assoc = select(CollectionArticle).where(CollectionArticle.collection_id == collection_id)
        assocs = session.exec(stmt_assoc).all()
        for assoc in assocs:
            session.delete(assoc)

        # Then, delete the collection itself
        coll = session.get(Collection, collection_id)
        if coll:
            session.delete(coll)

        session.commit()


def add_article_to_collection(collection_id: int, article_id: int) -> None:
    """Associate an article with a collection (idempotent)."""
    with get_session() as session:
        # Check existence first
        exists_stmt = select(CollectionArticle).where(
            and_(CollectionArticle.collection_id == collection_id, CollectionArticle.article_id == article_id)
        )
        existing = session.exec(exists_stmt).first()
        if existing:
            return

        assoc = CollectionArticle(collection_id=collection_id, article_id=article_id)
        session.add(assoc)
        session.commit()


def remove_article_from_collection(collection_id: int, article_id: int) -> None:
    """Remove association between an article and a collection."""
    with get_session() as session:
        stmt = select(CollectionArticle).where(
            and_(CollectionArticle.collection_id == collection_id, CollectionArticle.article_id == article_id)
        )
        assoc = session.exec(stmt).first()
        if assoc:
            session.delete(assoc)
            session.commit()


def get_articles_for_collection(collection_id: int) -> List[Dict[str, Any]]:
    """Return article dicts for all articles in a collection ordered by fetched_at desc."""
    with get_session() as session:
        stmt = (
            select(Article)
            .join(CollectionArticle, Article.id == CollectionArticle.article_id)
            .where(CollectionArticle.collection_id == collection_id)
            .order_by(desc(Article.fetched_at))
        )
        articles = session.exec(stmt).all()
        return [_article_to_dict(article) for article in articles]


def get_article_count_for_collection(collection_id: int) -> int:
    """Return the count of articles in a specific collection using a count query."""
    with get_session() as session:
        stmt = select(func.count(CollectionArticle.article_id)).where(CollectionArticle.collection_id == collection_id)
        return session.exec(stmt).one()
