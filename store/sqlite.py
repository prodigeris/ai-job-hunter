import sqlite3
from pathlib import Path
from datetime import datetime
from scrape.providers.models import JobListing

class SQLiteStore:
    def __init__(self, db_path: str | Path = "data/jobs.db"):
        # Ensure data directory exists
        db_path = Path(db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.db_path = db_path
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        
        # Create tables if they don't exist
        self._init_db()
    
    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL UNIQUE,
                content TEXT NOT NULL,
                checksum TEXT NOT NULL,
                published_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP NOT NULL,
                salary_min REAL,
                salary_max REAL,
                location TEXT,
                UNIQUE(checksum)
            )
        """)
        self.conn.commit()
    
    def insert_job(self, job: JobListing) -> bool:
        """Insert a job listing into the database. Returns True if inserted, False if already exists."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO job_listings 
                (url, content, checksum, published_at, created_at, salary_min, salary_max, location)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(job.url),
                job.content,
                job.checksum,
                job.published_at,
                job.created_at,
                job.salary_min,
                job.salary_max,
                job.location
            ))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_job_by_checksum(self, checksum: str) -> JobListing | None:
        """Retrieve a job listing by its checksum."""
        cursor = self.conn.cursor()
        row = cursor.execute(
            "SELECT * FROM job_listings WHERE checksum = ?", 
            (checksum,)
        ).fetchone()
        
        if not row:
            return None
            
        return JobListing(
            url=row['url'],
            content=row['content'],
            _checksum=row['checksum'],
            published_at=datetime.fromisoformat(row['published_at']),
            created_at=datetime.fromisoformat(row['created_at']),
            salary_min=row['salary_min'],
            salary_max=row['salary_max'],
            location=row['location']
        )
    
    def get_all_jobs(self) -> list[JobListing]:
        """Retrieve all job listings."""
        cursor = self.conn.cursor()
        rows = cursor.execute("SELECT * FROM job_listings").fetchall()
        
        return [
            JobListing(
                url=row['url'],
                content=row['content'],
                _checksum=row['checksum'],
                published_at=datetime.fromisoformat(row['published_at']),
                created_at=datetime.fromisoformat(row['created_at']),
                salary_min=row['salary_min'],
                salary_max=row['salary_max'],
                location=row['location']
            )
            for row in rows
        ]
    
    def __del__(self):
        """Ensure database connection is closed when object is destroyed."""
        if hasattr(self, 'conn'):
            self.conn.close()
