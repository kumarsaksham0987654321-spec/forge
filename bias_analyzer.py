import os
import re
import httpx
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Initialize Google Gen AI client (reads GEMINI_API_KEY from environment)
client = genai.Client()

# Define structured output schema for Pydantic
class BiasAnalysisResult(BaseModel):
    input_type: str = Field(description="Source type evaluated: 'image', 'url', or 'text'")
    extracted_text: str = Field(description="Raw text extracted from image, URL, or directly provided")
    bias_score: int = Field(description="-100 (Far-Left) to +100 (Far-Right), 0 being Neutral")
    bias_label: str = Field(description="Classification: Far-Left, Center-Left, Neutral, Center-Right, or Far-Right")
    sensationalism_score: int = Field(description="0 (Objective reporting) to 100 (Extreme clickbait/sensationalism)")
    key_fallacies_or_framing: list[str] = Field(description="Loaded language, framing tactics, or logical fallacies detected")
    objective_summary: str = Field(description="A strictly neutral summary stripped of political slant")

def scrape_url_text(url: str) -> str:
    """Scrapes news headline and body text from a webpage."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    with httpx.Client(timeout=10.0, follow_redirects=True) as http_client:
        response = http_client.get(url, headers=headers)
        response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    for noisy_tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        noisy_tag.decompose()
        
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    full_text = " ".join([p for p in paragraphs if len(p) > 25])
    
    if not full_text.strip():
        raise ValueError("Could not extract readable article text from the URL.")
    return full_text[:4000]

def analyze_news_bias(
    text_content: str = None, 
    url: str = None, 
    image_bytes: bytes = None, 
    image_mime: str = "image/png"
) -> dict: # Updated return type hint to dict
    """Uses Gemini vision for free multimodal OCR and structured media bias extraction."""
    
    prompt = (
        "You are an expert media literacy analyst. "
        "Examine the input content (which may be an image screenshot, raw text, or web article). "
        "If an image is provided, perform precise OCR to extract all readable text first. "
        "Then evaluate political slant, loaded phrases, sensationalism, and logical framing. "
        "Populate the requested JSON schema accurately."
    )

    contents = [prompt]
    input_type = "text"

    if image_bytes:
        input_type = "image"
        pil_img = Image.open(BytesIO(image_bytes))
        contents.append(pil_img)
        contents.append("Extract all news text from this image and analyze its bias.")
    elif url:
        input_type = "url"
        scraped_text = scrape_url_text(url)
        contents.append(f"Analyze this news article content scraped from {url}:\n\n{scraped_text}")
    elif text_content:
        input_type = "text"
        contents.append(f"Analyze this news text:\n\n{text_content}")
    else:
        raise ValueError("No valid input provided. Upload an image, submit a URL, or paste text.")

    # Request structured response using Gemini 2.5 Flash
    response = client.models.generate_content(
        model="gemini-3.6-flash",  # Fixed model name
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=BiasAnalysisResult,
            temperature=0.2,
        ),
    )

    # Convert the parsed output to a dictionary so .get() calls in Streamlit work seamlessly
    result_dict = response.parsed.model_dump()
    result_dict["input_type"] = input_type
    
    return result_dict