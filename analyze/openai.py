from openai import OpenAI
from datetime import datetime, UTC
from .models import AnalyzedJob
from dotenv import load_dotenv
import json

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

    job_description = f"""
    Job description: {job_description}
    Salary range: {f'${salary_from:,.0f}-${salary_to:,.0f}' if salary_from and salary_to else 'Not specified'}
    Location: {location if location else 'Not specified'}
    Job title: {title if title else 'Not specified'}
    """

    response = client.responses.create(
  model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
  input=[
    {
      "role": "system",
      "content": [
        {
          "type": "input_text",
          "text": "You are AI assistant that helps me classify job listings."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "Analyze this job description into json\n\n\"\"\"\n Job description: {job_description}"
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
          "salary_from": {
            "type": "number",
            "description": "Minimum salary for the position, can be null."
          },
          "salary_to": {
            "type": "number",
            "description": "Maximum salary for the position, can be null."
          },
          "is_remote_score": {
            "type": "number",
            "description": "Score indicating how likely that the position is remote, on a scale of 0 to 1."
          },
          "is_applicable_score": {
            "type": "number", 
            "description": "Score how directly the job involves backend engineering based on the job title. Use:\n\
            - 1.0 for pure backend engineers (working with APIs, databases, services).\n\
            - 0.8 for fullstack or DevOps engineers (who also work on backend).\n\
            - 0.5 for frontend or mobile developers.\n\
            - 0.2 for adjacent IT roles (data, QA, PM).\n\
            - 0.0 for all non-technical roles (marketing, recruiting, HR, design, social media). \
            Do not assign a value > 0.0 unless the role involves writing code for backend systems."
          },
          "is_european_score": {
            "type": "number",
            "description": "Score indicating how likely that the employee can be located in the EU, on a scale of 0 to 1."
          }
        },
        "required": [
          "salary_from",
          "salary_to",
          "is_remote_score",
          "is_applicable_score",
          "is_european_score"
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
    
    # Save response to output.json for analysis
    with open("data/output_{job_id}.json", "w") as f:
        json.dump({
            "job_id": job_id,
            "url": str(url), 
            "response": response.model_dump(),
            "timestamp": datetime.now(UTC).isoformat()
        }, f, indent=2)

    scores = json.loads(response.output[0].content[0].text)
    
    return AnalyzedJob(
        job_listing_id=job_id,
        url=str(url),  
        salary_from=salary_from,
        salary_to=salary_to,
        is_remote_score=scores["is_remote_score"],
        is_applicable_score=scores["is_applicable_score"], 
        is_european_score=scores["is_european_score"],
        analyzed_at=datetime.now(UTC)
    )