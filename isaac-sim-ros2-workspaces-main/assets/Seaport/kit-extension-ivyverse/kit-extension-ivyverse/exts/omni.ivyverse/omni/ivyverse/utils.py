"""Common utilities for Ivyverse extension"""
import json
import os
from typing import Any, Dict, List
def save_json(data: Dict[str, Any], filepath: str):
    """Save data to JSON file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
def load_json(filepath: str) -> Dict[str, Any]:
    """Load data from JSON file"""
    if not os.path.exists(filepath):
        return {}
    
    with open(filepath, 'r') as f:
        return json.load(f)
def format_usd_path(path: str) -> str:
    """Format USD path for display"""
    if not path.startswith("/"):
        path = "/" + path
    return path
def extract_prim_name(path: str) -> str:
    """Extract prim name from path"""
    return path.split("/")[-1] if path else ""
def build_breadcrumb(path: str) -> List[str]:
    """Build breadcrumb from USD path"""
    if not path or path == "/":
        return []
    
    parts = path.strip("/").split("/")
    return parts
def format_file_size(size_bytes: int) -> str:
    """Format file size for display"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"
def truncate_string(text: str, max_length: int = 50) -> str:
    """Truncate string with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
