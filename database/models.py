"""
Database models for storing research history
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import config
import os

Base = declarative_base()


class ResearchRun(Base):
    """Model for tracking research runs"""
    __tablename__ = 'research_runs'
    
    id = Column(Integer, primary_key=True)
    run_date = Column(DateTime, default=datetime.now)
    success = Column(Boolean, default=False)
    news_count = Column(Integer, default=0)
    papers_count = Column(Integer, default=0)
    execution_time = Column(Integer)  # in seconds
    errors = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)


class Paper(Base):
    """Model for storing paper information"""
    __tablename__ = 'papers'
    
    id = Column(Integer, primary_key=True)
    paper_id = Column(String(50), unique=True, index=True)  # arXiv ID
    title = Column(Text)
    authors = Column(Text)
    abstract = Column(Text)
    published_date = Column(DateTime)
    category = Column(String(50))
    pdf_url = Column(String(500))
    featured_date = Column(DateTime, nullable=True)  # When it was featured in digest
    created_at = Column(DateTime, default=datetime.now)


class NewsArticle(Base):
    """Model for storing news articles"""
    __tablename__ = 'news_articles'
    
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    link = Column(String(500), unique=True, index=True)
    source = Column(String(200))
    published_date = Column(DateTime)
    summary = Column(Text)
    featured_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)


class DatabaseManager:
    """Manager for database operations"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = config.DATABASE_PATH
        
        # Ensure directory exists
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        # Create engine
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        
        # Create session
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def add_research_run(self, success: bool, news_count: int, papers_count: int, 
                        execution_time: int, errors: str = None) -> ResearchRun:
        """Add a research run record"""
        run = ResearchRun(
            success=success,
            news_count=news_count,
            papers_count=papers_count,
            execution_time=execution_time,
            errors=errors
        )
        self.session.add(run)
        self.session.commit()
        return run
    
    def add_paper(self, paper_data: dict, featured: bool = False) -> Paper:
        """Add or update a paper record"""
        # Check if paper already exists
        existing = self.session.query(Paper).filter_by(
            paper_id=paper_data.get('id')
        ).first()
        
        if existing:
            if featured:
                existing.featured_date = datetime.now()
                self.session.commit()
            return existing
        
        # Create new paper
        paper = Paper(
            paper_id=paper_data.get('id'),
            title=paper_data.get('title'),
            authors=', '.join(paper_data.get('authors', [])),
            abstract=paper_data.get('abstract'),
            published_date=datetime.strptime(paper_data.get('published', '2000-01-01'), '%Y-%m-%d'),
            category=paper_data.get('primary_category', 'unknown'),
            pdf_url=paper_data.get('pdf_url'),
            featured_date=datetime.now() if featured else None
        )
        self.session.add(paper)
        self.session.commit()
        return paper
    
    def add_news_article(self, article_data: dict, featured: bool = False) -> NewsArticle:
        """Add or update a news article record"""
        # Check if article already exists
        existing = self.session.query(NewsArticle).filter_by(
            link=article_data.get('link')
        ).first()
        
        if existing:
            if featured:
                existing.featured_date = datetime.now()
                self.session.commit()
            return existing
        
        # Create new article
        article = NewsArticle(
            title=article_data.get('title'),
            link=article_data.get('link'),
            source=article_data.get('source'),
            published_date=datetime.now(),  # Can be improved to parse actual date
            summary=article_data.get('summary'),
            featured_date=datetime.now() if featured else None
        )
        self.session.add(article)
        self.session.commit()
        return article
    
    def get_recent_papers(self, days: int = 7) -> list:
        """Get papers featured in last N days"""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days)
        
        papers = self.session.query(Paper).filter(
            Paper.featured_date >= cutoff
        ).all()
        
        return papers
    
    def paper_was_featured(self, paper_id: str, days: int = 30) -> bool:
        """
        Check if a paper was already featured in the last N days
        
        Args:
            paper_id: arXiv paper ID
            days: Number of days to look back (default: 30)
            
        Returns:
            True if paper was featured in the last N days
        """
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days)
        
        paper = self.session.query(Paper).filter_by(
            paper_id=paper_id
        ).first()
        
        return paper is not None and paper.featured_date is not None and paper.featured_date >= cutoff
    
    def get_statistics(self) -> dict:
        """Get database statistics"""
        return {
            'total_runs': self.session.query(ResearchRun).count(),
            'successful_runs': self.session.query(ResearchRun).filter_by(success=True).count(),
            'total_papers': self.session.query(Paper).count(),
            'featured_papers': self.session.query(Paper).filter(Paper.featured_date.isnot(None)).count(),
            'total_articles': self.session.query(NewsArticle).count(),
            'featured_articles': self.session.query(NewsArticle).filter(NewsArticle.featured_date.isnot(None)).count(),
        }
    
    def close(self):
        """Close database connection"""
        self.session.close()


def get_db() -> DatabaseManager:
    """Get database manager instance"""
    return DatabaseManager()
