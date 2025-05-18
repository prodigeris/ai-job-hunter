from openai import OpenAI
from datetime import datetime, UTC
from .models import AnalyzedJob

client = OpenAI()

def analyze_job_listing(job_description: str, job_id: int, url: str, salary_from: float | None = None, salary_to: float | None = None, location: str | None = None) -> AnalyzedJob:
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
    """

    response = client.responses.create(
  model="gpt-4o-mini",
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
    },
    {
      "id": "msg_68292425afb48198a01a2ed0f87796920c1de4fa2af5624d",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "{\n  \"salary_from\": 0,\n  \"salary_to\": 0,\n  \"is_remote_score\": 0,\n  \"is_applicable_score\": 0.8,\n  \"is_european_score\": 0.6\n}"
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
            "description": "Score indicating how likely that the job is for a backend engineering role, on a scale of 0 to 1."
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

    scores = response.choices[0].message.content
    
    return AnalyzedJob(
        job_listing_id=job_id,
        url=url,
        salary_from=salary_from,
        salary_to=salary_to,
        is_remote_score=scores["is_remote"],
        is_applicable_score=scores["is_backend_role"], 
        is_european_score=scores["can_work_from_europe"],
        analyzed_at=datetime.now(UTC)
    )