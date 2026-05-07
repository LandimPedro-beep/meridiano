"""
SQLModel database models for Meridiano application.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, text

from . import config_base as config


class Article(SQLModel, table=True):
    """Article model representing news articles in the database."""

    # Old SQLite schema for reference
    """
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT, /* id is alias for rowid */
        url TEXT UNIQUE NOT NULL,
        title TEXT,
        published_date DATETIME,
        feed_source TEXT,
        fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        raw_content TEXT,
        processed_content TEXT,
        embedding TEXT,
        processed_at DATETIME,
        cluster_id INTEGER,
        impact_score INTEGER,
        image_url TEXT,
        feed_profile TEXT NOT NULL DEFAULT 'default'
    );
    CREATE INDEX IF NOT EXISTS idx_articles_url ON articles (url);
    CREATE INDEX IF NOT EXISTS idx_articles_processed_at ON articles (processed_at);
    CREATE INDEX IF NOT EXISTS idx_articles_published_date ON articles (published_date);
    """

    __tablename__ = "articles"

    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(unique=True, index=True)
    title: Optional[str] = None
    published_date: Optional[datetime] = None
    publication_date_verified: Optional[datetime] = Field(default=None, index=True)
    publication_year: Optional[int] = Field(default=None, index=True)
    feed_source: Optional[str] = None
    rss_feed_url: Optional[str] = Field(default=None, index=True)
    editorial_block: Optional[str] = Field(default=None, index=True)
    fetched_at: datetime = Field(default_factory=datetime.now)
    scrape_status: Optional[str] = Field(default=None, index=True)
    metadata_status: Optional[str] = Field(default=None, index=True)
    metadata_extracted_at: Optional[datetime] = Field(default=None, index=True)
    raw_content: Optional[str] = None
    abstract: Optional[str] = None
    processed_content: Optional[str] = None
    embedding: Optional[str] = None  # JSON string
    processed_at: Optional[datetime] = Field(default=None, index=True)
    llm_stage_version: Optional[str] = None
    keyword_labels: Optional[str] = None  # JSON string
    keyword_match: Optional[bool] = Field(default=None, index=True)
    keyword_checked_at: Optional[datetime] = Field(default=None, index=True)
    doi: Optional[str] = Field(default=None, index=True)
    journal_name: Optional[str] = Field(default=None, index=True)
    authors: Optional[str] = None  # JSON string or normalized text
    article_type: Optional[str] = Field(default=None, index=True)
    citation_count: Optional[int] = Field(default=None, index=True)
    citation_source: Optional[str] = None
    is_review: Optional[bool] = Field(default=None, index=True)
    scientific_domain: Optional[str] = Field(default=None, index=True)
    subdomain: Optional[str] = Field(default=None, index=True)
    cluster_id: Optional[int] = None
    impact_score: Optional[int] = None
    relevance_score: Optional[float] = None
    novelty_score: Optional[float] = None
    canonical_score: Optional[float] = None
    novelty_window_match: Optional[bool] = Field(default=None, index=True)
    matrix_window_match: Optional[bool] = Field(default=None, index=True)
    eligibility_status: Optional[str] = Field(default=None, index=True)
    eligibility_reason: Optional[str] = None
    image_url: Optional[str] = None
    feed_profile: str = Field(default="default", index=True)


class FeedScrapeMetric(SQLModel, table=True):
    """Per-feed scrape metrics captured for a single scrape run."""

    __tablename__ = "feed_scrape_metrics"

    id: Optional[int] = Field(default=None, primary_key=True)
    scrape_run_id: str = Field(index=True)
    recorded_at: datetime = Field(default_factory=datetime.now, index=True)
    feed_profile: str = Field(index=True)
    rss_feed_url: str = Field(index=True)
    feed_source: Optional[str] = None
    detected_count: int = Field(default=0)
    duplicate_count: int = Field(default=0)
    scrape_success_count: int = Field(default=0)
    scrape_failed_count: int = Field(default=0)


class Brief(SQLModel, table=True):
    """Brief model representing generated news briefs."""

    # Old SQLite schema for reference
    """
    # Briefs Table
    CREATE TABLE IF NOT EXISTS briefs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        brief_markdown TEXT NOT NULL,
        contributing_article_ids TEXT,
        feed_profile TEXT NOT NULL DEFAULT 'default'
    )
    """

    __tablename__ = "briefs"

    id: Optional[int] = Field(default=None, primary_key=True)
    generated_at: datetime = Field(default_factory=datetime.now)
    brief_markdown: str
    contributing_article_ids: Optional[str] = None  # JSON string
    feed_profile: str = Field(default="default", index=True)


class WeeklyEdition(SQLModel, table=True):
    """Frozen weekly editorial edition for one block/profile."""

    __tablename__ = "weekly_editions"

    id: Optional[int] = Field(default=None, primary_key=True)
    edition_key: str = Field(index=True, unique=True)
    block_id: str = Field(index=True)
    feed_profile: str = Field(index=True)
    week_start_date: datetime = Field(index=True)
    week_end_date: datetime = Field(index=True)
    status: str = Field(default="draft", index=True)
    generated_at: datetime = Field(default_factory=datetime.now, index=True)
    notes: Optional[str] = None
    summary_markdown: Optional[str] = None


class WeeklyEditionArticle(SQLModel, table=True):
    """Articles selected into a frozen weekly edition."""

    __tablename__ = "weekly_edition_articles"

    edition_id: Optional[int] = Field(default=None, foreign_key="weekly_editions.id", primary_key=True)
    article_id: Optional[int] = Field(default=None, foreign_key="articles.id", primary_key=True)
    rank: Optional[int] = Field(default=None, index=True)
    inclusion_reason: Optional[str] = None
    selected_at: datetime = Field(default_factory=datetime.now, index=True)


# Collections models (many-to-many association) --------------------------------
class CollectionArticle(SQLModel, table=True):
    """Association table between collections and articles."""
    collection_id: Optional[int] = Field(default=None, foreign_key="collections.id", primary_key=True)
    article_id: Optional[int] = Field(default=None, foreign_key="articles.id", primary_key=True)


class Collection(SQLModel, table=True):
    """Collection of articles created by a user."""
    __tablename__ = "collections"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    archived: bool = Field(default=False, index=True)


# Database engine and session management
engine = create_engine(config.DATABASE_URL, echo=False)


def create_db_and_tables():
    """Create database tables if they don't exist."""
    SQLModel.metadata.create_all(engine)

    # Simple migration logic for 'archived' column in 'collections'
    with Session(engine) as session:
        try:
            # Check if column exists by trying to select it
            session.exec(text("SELECT archived FROM collections LIMIT 1"))
        except Exception:
            # If selection fails, the column likely doesn't exist. Add it.
            print("Migrating 'collections' table: Adding 'archived' column...")
            session.rollback()  # Clear the error state
            try:
                if "postgresql" in config.DATABASE_URL.lower():
                    session.exec(text("ALTER TABLE collections ADD COLUMN archived BOOLEAN DEFAULT FALSE"))
                    session.exec(text("CREATE INDEX ix_collections_archived ON collections (archived)"))
                else:
                    # SQLite
                    session.exec(text("ALTER TABLE collections ADD COLUMN archived BOOLEAN DEFAULT 0"))
                session.commit()
                print("Migration successful.")
            except Exception as e:
                print(f"Migration failed: {e}")
                session.rollback()

    with Session(engine) as session:
        article_column_migrations = [
            ("rss_feed_url", "TEXT"),
            ("publication_date_verified", "DATETIME"),
            ("publication_year", "INTEGER"),
            ("editorial_block", "TEXT"),
            ("scrape_status", "TEXT"),
            ("metadata_status", "TEXT"),
            ("metadata_extracted_at", "DATETIME"),
            ("abstract", "TEXT"),
            ("llm_stage_version", "TEXT"),
            ("keyword_labels", "TEXT"),
            ("keyword_match", "BOOLEAN"),
            ("keyword_checked_at", "DATETIME"),
            ("doi", "TEXT"),
            ("journal_name", "TEXT"),
            ("authors", "TEXT"),
            ("article_type", "TEXT"),
            ("citation_count", "INTEGER"),
            ("citation_source", "TEXT"),
            ("is_review", "BOOLEAN"),
            ("scientific_domain", "TEXT"),
            ("subdomain", "TEXT"),
            ("relevance_score", "REAL"),
            ("novelty_score", "REAL"),
            ("canonical_score", "REAL"),
            ("novelty_window_match", "BOOLEAN"),
            ("matrix_window_match", "BOOLEAN"),
            ("eligibility_status", "TEXT"),
            ("eligibility_reason", "TEXT"),
        ]
        for column_name, column_type in article_column_migrations:
            try:
                session.exec(text(f"SELECT {column_name} FROM articles LIMIT 1"))
            except Exception:
                print(f"Migrating 'articles' table: Adding '{column_name}' column...")
                session.rollback()
                try:
                    session.exec(text(f"ALTER TABLE articles ADD COLUMN {column_name} {column_type}"))
                    session.commit()
                    print("Migration successful.")
                except Exception as e:
                    print(f"Migration failed: {e}")
                    session.rollback()

    # Old SQLite schema for reference (replaced by to_tsvector in PostgreSQL)
    """
    # --- FTS5 Virtual Table ---
    # Create the virtual table to index title and raw_content from articles
    # content='' means it doesn't store the content itself, only index
    # content_rowid='id' links the FTS rowid to the articles table id column
    CREATE VIRTUAL TABLE IF NOT EXISTS articles_fts USING fts5(
        title,
        raw_content,
        content='articles',
        content_rowid='id'
    )

    # --- Triggers to keep FTS table synchronized ---
    # After inserting into articles, insert into articles_fts
    CREATE TRIGGER IF NOT EXISTS articles_ai AFTER INSERT ON articles BEGIN
        INSERT INTO articles_fts (rowid, title, raw_content)
        VALUES (new.id, new.title, new.raw_content);
    END;

    # Before deleting from articles, delete from articles_fts
    # Need old.id to identify the row in articles_fts
    CREATE TRIGGER IF NOT EXISTS articles_ad BEFORE DELETE ON articles BEGIN
        DELETE FROM articles_fts WHERE rowid=old.id;
    END;

    # After updating articles, update articles_fts
    CREATE TRIGGER IF NOT EXISTS articles_au AFTER UPDATE ON articles BEGIN
        UPDATE articles_fts SET title=new.title, raw_content=new.raw_content
        WHERE rowid=old.id;
    END;
    # --- End FTS Setup ---
    """

    # For PostgreSQL, create full-text search index
    if "postgresql" in config.DATABASE_URL.lower():
        with Session(engine) as session:
            try:
                # Create full-text search index
                session.exec(
                    text("""
                    CREATE INDEX IF NOT EXISTS idx_articles_fts
                    ON articles USING GIN(
                        to_tsvector('english',
                            coalesce(title, '') || ' ' || coalesce(raw_content, '')
                        )
                    )
                """)
                )
                session.commit()
                print("PostgreSQL full-text search index created")
            except Exception as e:
                print(f"Note: FTS index creation: {e}")
                session.rollback()


def get_session():
    """Get a database session."""
    return Session(engine)


def init_db():
    """Initialize the database - create all tables."""
    create_db_and_tables()
    print("Database initialized with SQLModel.")


if __name__ == "__main__":
    init_db()
