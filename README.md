# ComicCraft

ComicCraft is an AI-powered web application that transforms a user's story idea into a five-panel comic.

## Features

- Story prompt input
- Character customization
- Setting selection
- Tone selection
- Art style selection
- Five-panel story outline
- AI-generated narration
- AI-generated dialogue
- AI-generated comic illustrations
- Comic preview
- PDF export
- FastAPI REST API
- Interactive FastAPI documentation

## Architecture

Browser

↓

FastAPI

↓

Gemini

↓

Five-panel outline

↓

Gemini story generation

↓

Hugging Face image generation

↓

Comic layout builder

↓

PDF exporter

↓

Comic preview and download

## Installation

Create a virtual environment:

```powershell
py -3.11 -m venv .venv