import json
import os
from utils.config import JSON_STORAGE_PATH

def save_to_json(document,domain):
    """
    Save a document to a JSON file. If a file with the same domain name exists,
    append the new document to the existing file. Otherwise, create a new file.

    Args:
        document (dict): The document to be saved. Must contain a 'domain' field.

    Raises:
        ValueError: If the document does not contain a 'domain' field.
    """
    print(f"Saving document to JSON: {document}")
    
    file_path = os.path.join(JSON_STORAGE_PATH, f"{domain}.json")
    
    if os.path.exists(file_path):
        with open(file_path, 'r+') as f:
            data = json.load(f)
            if isinstance(data, list):
                data.append(document)
            else:
                data = [data, document]
            f.seek(0)
            json.dump(data, f, indent=4)
    else:
        with open(file_path, 'w') as f:
            json.dump([document], f, indent=4)
