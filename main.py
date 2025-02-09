from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/outline")
async def get_country_outline(country: str = Query(..., description="Country name")):
    """Fetch Wikipedia headings and return a Markdown outline."""

    # Construct Wikipedia URL
    wiki_url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    
    # Fetch Wikipedia page content
    response = requests.get(wiki_url)
    
    if response.status_code != 200:
        return {"error": "Country not found or Wikipedia page unavailable."}

    # Parse HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract headings
    markdown_outline = "## Contents\n\n" + f"# {country}\n\n"
    
    for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        level = int(heading.name[1])  # Convert 'h2' → 2, 'h3' → 3, etc.
        markdown_outline += f"{'#' * level} {heading.text.strip()}\n\n"

    return {"country": country, "markdown_outline": markdown_outline}

