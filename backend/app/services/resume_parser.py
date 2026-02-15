from __future__ import annotations

import re
from io import BytesIO

from fastapi import HTTPException, status

from app.schemas import ParsedResumeProfile

try:
    from pypdf import PdfReader
except ModuleNotFoundError:  # pragma: no cover
    PdfReader = None

try:
    from docx import Document
except ModuleNotFoundError:  # pragma: no cover
    Document = None

SKILL_CATALOG = [
    "Python",
    "JavaScript",
    "TypeScript",
    "React",
    "Next.js",
    "Node.js",
    "FastAPI",
    "Django",
    "SQL",
    "PostgreSQL",
    "MongoDB",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "Machine Learning",
    "Generative AI",
    "Data Analysis",
    "Git",
    "CI/CD",
    "Testing",
    "Communication",
]

EDUCATION_TERMS = {
    "Bachelors": ["bachelor", "b.tech", "b.e", "bs", "b.sc"],
    "Masters": ["master", "m.tech", "ms", "m.sc", "mba"],
    "Doctorate": ["phd", "doctorate"],
}

INTEREST_TERMS = {
    "AI Engineering": ["machine learning", "generative ai", "llm", "nlp"],
    "Cloud Engineering": ["aws", "azure", "cloud", "devops", "kubernetes"],
    "Product Engineering": ["react", "next.js", "frontend", "backend", "fullstack"],
    "Data Engineering": ["sql", "etl", "analytics", "data pipeline"],
}


def parse_resume(file_name: str, mime_type: str | None, file_bytes: bytes) -> ParsedResumeProfile:
    text = _extract_text(file_name=file_name, mime_type=mime_type or "", file_bytes=file_bytes)
    cleaned = " ".join(text.split())
    if not cleaned:
        return ParsedResumeProfile(
            skills=[],
            experience_level="Unknown",
            education=["Not specified"],
            interests=["General Software Engineering"],
            raw_text_preview="",
            parse_warning=(
                "Could not extract readable text from this file. "
                "It may be a scanned/image-based or protected PDF. "
                "Try a text-based PDF, DOCX, or TXT for better analysis."
            ),
        )

    skills = _extract_skills(cleaned)
    return ParsedResumeProfile(
        skills=skills,
        experience_level=_infer_experience_level(cleaned),
        education=_extract_education(cleaned),
        interests=_extract_interests(cleaned),
        raw_text_preview=cleaned[:450],
    )


def _extract_text(file_name: str, mime_type: str, file_bytes: bytes) -> str:
    suffix = file_name.lower().split(".")[-1] if "." in file_name else ""
    if suffix == "txt" or mime_type == "text/plain":
        return file_bytes.decode("utf-8", errors="ignore")
    if suffix == "pdf" or mime_type == "application/pdf":
        return _extract_pdf_text(file_bytes)
    if suffix == "docx" or "wordprocessingml.document" in mime_type:
        return _extract_docx_text(file_bytes)

    raise HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail="Unsupported file type. Please upload PDF, DOCX, or TXT.",
    )


def _extract_pdf_text(file_bytes: bytes) -> str:
    if PdfReader is None:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="PDF parsing dependency is missing. Install pypdf to enable this format.",
        )
    reader = PdfReader(BytesIO(file_bytes))
    chunks = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(chunks)


def _extract_docx_text(file_bytes: bytes) -> str:
    if Document is None:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="DOCX parsing dependency is missing. Install python-docx to enable this format.",
        )
    document = Document(BytesIO(file_bytes))
    return "\n".join(paragraph.text for paragraph in document.paragraphs)


def _extract_skills(text: str) -> list[str]:
    lower = text.lower()
    found: list[str] = []
    for skill in SKILL_CATALOG:
        token = skill.lower()
        if token in {"c++", "c#", "node.js", "next.js"}:
            match = token in lower
        else:
            match = re.search(rf"\b{re.escape(token)}\b", lower) is not None
        if match:
            found.append(skill)
    return found


def _infer_experience_level(text: str) -> str:
    lower = text.lower()
    years = re.findall(r"(\d+)\+?\s+years?", lower)
    max_years = max((int(value) for value in years), default=0)

    if max_years >= 8 or any(word in lower for word in ["architect", "principal", "lead"]):
        return "Senior"
    if max_years >= 4:
        return "Mid-level"
    if any(word in lower for word in ["intern", "entry level", "fresher"]):
        return "Entry-level"
    return "Early-career"


def _extract_education(text: str) -> list[str]:
    lower = text.lower()
    results = [label for label, keys in EDUCATION_TERMS.items() if any(key in lower for key in keys)]
    return results or ["Not specified"]


def _extract_interests(text: str) -> list[str]:
    lower = text.lower()
    interests = [label for label, keys in INTEREST_TERMS.items() if any(key in lower for key in keys)]
    return interests or ["General Software Engineering"]
