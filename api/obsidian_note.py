from flask import Flask, request
import os

#import common variables, classes
from api.fabai_common import *

app = Flask(__name__)

# Setup logging using the built-in logging module
logging.basicConfig(level=logging.INFO)

from flask import Flask, request
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

def create_note(vault_path, file_name, note_header, note_content, tags=None, related_notes=None):
    # Ensure the vault directory exists
    if not os.path.exists(vault_path):
        app.logger.error(f"Vault path does not exist: {vault_path}")
        return False  # Indicate failure

    # Prepare the final note content
    final_note_content = f"# {note_header}\n\n{note_content}\n\n"

    # Add tags
    if tags:
        final_note_content += "Tags: " + ", ".join(tags) + "\n"

    # Add related notes
    if related_notes:
        final_note_content += "Related Notes: " + ", ".join(related_notes) + "\n"

    # Define the complete file path
    file_path = os.path.join(vault_path, f"{file_name}.md")

    # Create and write the note
    try:
        with open(file_path, 'w') as note_file:
            note_file.write(final_note_content)
        app.logger.info(f"Note created: {file_path}")
        return True  # Indicate success
    except Exception as e:
        app.logger.error(f"Failed to create note: {e}")
        return False  # Indicate failure

if __name__ == '__main__':
    app.run(debug=True)

