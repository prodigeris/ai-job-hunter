from flask import Flask, render_template
from store.sqlite import SQLiteStore
from datetime import datetime
from contextlib import contextmanager

app = Flask(__name__)

@contextmanager
def get_store():
    store = SQLiteStore()
    try:
        yield store
    finally:
        store.close()

@app.route('/')
def list_jobs():
    with get_store() as store:
        # Get all analyzed jobs with their analysis results
        conn = store._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                jl.title,
                jl.url,
                jl.salary_min as salary_from,
                jl.salary_max as salary_to,
                aj.is_remote_score,
                aj.is_applicable_score,
                aj.is_european_score,
                aj.analyzed_at
            FROM job_listings jl
            JOIN analyzed_jobs aj ON jl.id = aj.job_listing_id
            ORDER BY aj.analyzed_at DESC
        """)
        rows = cursor.fetchall()
        
        # Convert rows to list of dicts with proper datetime objects
        jobs = []
        for row in rows:
            job = dict(row)
            job['analyzed_at'] = datetime.fromisoformat(job['analyzed_at'])
            jobs.append(job)
            
        return render_template('jobs.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

