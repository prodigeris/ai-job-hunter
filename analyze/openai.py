from openai import OpenAI
from datetime import datetime, UTC
from .models import AnalyzedJob
from dotenv import load_dotenv
import json
import os

load_dotenv()

client = OpenAI()

def analyze_job_listing(job_description: str, job_id: int, url: str, salary_from: float | None = None, salary_to: float | None = None, location: str | None = None, title: str | None = None) -> AnalyzedJob:
    """
    Analyze a job listing using OpenAI to extract key metrics.
    
    Args:
        job_description: The job listing text content
        job_id: The ID of the job listing
        url: The URL of the job listing
        salary_from: Optional minimum salary 
        salary_to: Optional maximum salary
        location: Optional job location
    
    Returns:
        AnalyzedJob containing salary range and various job scores
    """

    job = f"""
    Job description: {job_description}
    Salary range: {f'${salary_from:,.0f}-${salary_to:,.0f}' if salary_from and salary_to else 'Not specified'}
    Location: {location if location else 'Not specified'}
    Job title: {title if title else 'Not specified'}
    """

    response = client.responses.create(
  model="gpt-4o-mini",
  input=[
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": f"Analyze this job description into json\n\n\"\"\"\n{job}\"\"\""
          }
      ]
    }
  ],
  text={
    "format": {
      "type": "json_schema",
      "name": "job_position_score",
      "strict": True,
      "schema": {
        "type": "object",
        "properties": {
          "yearly_salary_from": {
            "type": "number",
            "description": "Minimum yearly salary in USD for the position, can be null."
          },
          "yearly_salary_to": {
            "type": "number",
            "description": "Maximum yearly salary in USD for the position, can be null."
          },
          "how_likely_remote_role": {
            "type": "number",
            "description": "Score indicating how likely that the position is remote, on a scale of 0 to 1."
          },
          "is_backend_role": {
            "type": "number", 
            "description": "Is it a backend engineering or fullstack engineering role? Any other role is false, 0 for false, 1 for true."
          },
          "can_work_from_eu": {
            "type": "number",
            "description": "How likely that I can work from the EU for this role, on a scale of 0 to 1."
          }
        },
        "required": [
          "yearly_salary_from",
          "yearly_salary_to",
          "how_likely_remote_role",
          "is_backend_role",
          "can_work_from_eu"
        ],
        "additionalProperties": False
      }
    }
  },
  reasoning={},
  tools=[],
  temperature=1,
  max_output_tokens=2048,
  top_p=1,
  store=True
)
    
    scores = json.loads(response.output[0].content[0].text)
    
    return AnalyzedJob(
        job_listing_id=job_id,
        url=str(url),  
        salary_from=str(scores["yearly_salary_from"]),
        salary_to=str(scores["yearly_salary_to"]),
        is_remote_score=scores["how_likely_remote_role"],
        is_applicable_score=scores["is_backend_role"], 
        is_european_score=scores["can_work_from_eu"],
        analyzed_at=datetime.now(UTC)
    )