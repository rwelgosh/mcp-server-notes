# MCP Notes Server

A simple MCP (Message Coordination Protocol) server that provides access to notes stored in `~/DocumentationGenerator/notes/`.

## Setup

1. Make sure you have Python 3.7+ installed
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On macOS/Linux: `source venv/bin/activate`
   - On Windows: `venv\Scripts\activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Server

To start the MCP server:

```
python notes.py
```

This will start the server on `http://0.0.0.0:8000`.

## API Endpoints

The server exposes the following MCP commands:

- `list_notes(user_id=None)` - Get all notes, optionally filtered by user_id
- `get_note(note_id)` - Get a specific note by ID
- `add_note(title, content, user_id=None, tags=None)` - Create a new note
- `modify_note(note_id, title=None, content=None, tags=None)` - Update an existing note
- `remove_note(note_id)` - Delete a note by ID
- `search(query, user_id=None)` - Search notes by query string

## Note Format

Notes are stored as JSON files in the specified directory with the following format:

```json
{
    "category": {best_category},
    "summary": "summary of the notes", 
    "tags": [
        {
            "tag": "tag of the sub detail",
            "summary": "high level business logic of the sub details",
            "messages": [
                {
                    "timestamp": "timestamp of the message",
                    "message": "message content"
                },
                {
                    "timestamp": "timestamp of the message",
                    "message": "message content"
                },
                ...
            ]
        }
    ]
}
```

## Client Usage Example

Here's a simple Python example of how to connect to the MCP server from a client:

```python
from mcp.client import MCPClient

# Connect to the MCP server
client = MCPClient("http://localhost:8000")

# List all notes
notes = client.call("notes.list_notes")

# Get a specific note
note = client.call("notes.get_note", note_id="your-note-id")

# Create a new note
new_note = client.call(
    "notes.add_note", 
    title="My New Note", 
    content="This is the content of my note", 
    tags=["important", "work"]
)

# Search for notes
search_results = client.call("notes.search", query="important")
``` 