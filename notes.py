from typing import Any, Dict, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP
import os
import glob
import json
from pathlib import Path

# Initialize FastMCP server
mcp = FastMCP("notes")

# Constants
NOTES_DIRECTORY = os.path.expanduser("~/DocumentationGenerator/notes/")

# Ensure the notes directory exists
os.makedirs(NOTES_DIRECTORY, exist_ok=True)

# Helper functions
def get_notes() -> List[Dict[str, Any]]:
    """
    Get all notes.
    Returns a list of note objects.
    """
    notes = []
    file_pattern = os.path.join(NOTES_DIRECTORY, "*.json")
    
    for file_path in glob.glob(file_pattern):
        try:
            with open(file_path, 'r') as f:
                note = json.load(f)
                notes.append(note)
        except Exception as e:
            print(f"Error reading note {file_path}: {e}")
    
    return notes

def get_note_by_name(note_name: str) -> Optional[Dict[str, Any]]:
    """
    Get a specific note by its name.
    Returns the note object or None if not found.
    """
    file_path = os.path.join(NOTES_DIRECTORY, f"{note_name}.json")
    
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                note = json.load(f)
                return note
        except Exception as e:
            print(f"Error reading note {file_path}: {e}")
    
    return None

def search_notes(query: str, note_name: str = None) -> List[Dict[str, Any]]:
    """
    Search notes by a query string in title and content.
    Optionally filter by user_id.
    Returns matching notes.
    """
    query = query.lower()
    notes = get_notes(note_name)
    
    return [
        note for note in notes
        if query in note.get('title', '').lower() or 
           query in note.get('content', '').lower()
    ]

# Register MCP endpoints
@mcp.command
async def list_notes(note_name: str = None) -> List[Dict[str, Any]]:
    """List all notes, optionally filtered by note_name"""
    return get_notes()

@mcp.command
async def get_note(note_name: str) -> Dict[str, Any]:
    """Get a specific note by name"""
    note = get_note_by_name(note_name)
    if note is None:
        raise ValueError(f"Note with name {note_name} not found")
    return note

@mcp.command
async def search(query: str, note_name: str = None) -> List[Dict[str, Any]]:
    """Search notes by query string"""
    return search_notes(query, note_name)

# Run the server if executed as script
if __name__ == "__main__":
    # Start the server
    print(f"Starting MCP Notes server, serving notes from {NOTES_DIRECTORY}")
    mcp.run(transport='stdio')


