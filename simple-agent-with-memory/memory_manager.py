import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


class MemoryManager:
    """Manages persistent memory for AI agents"""
    
    def __init__(self, memory_file_path: str = './memory.json'):
        self.memory_file_path = Path(memory_file_path)
    
    def load_memories(self) -> Dict[str, Any]:
        """Load memories from the JSON file"""
        try:
            with open(self.memory_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is invalid, return empty memory
            return {
                'facts': [],
                'preferences': {},
                'conversations': []
            }
    
    def save_memories(self, memories: Dict[str, Any]) -> None:
        """Save new memories to the JSON file"""
        with open(self.memory_file_path, 'w', encoding='utf-8') as f:
            json.dump(memories, f, indent=2, ensure_ascii=False)
    
    def add_fact(self, fact: str) -> None:
        """Add a specific fact"""
        memories = self.load_memories()
        memories['facts'].append({
            'content': fact,
            'timestamp': datetime.now().isoformat()
        })
        self.save_memories(memories)
    
    def add_preference(self, key: str, value: str) -> None:
        """Add a user preference"""
        memories = self.load_memories()
        memories['preferences'][key] = value
        self.save_memories(memories)
    
    def get_memory_summary(self) -> str:
        """Get a summary of all memories for the system prompt"""
        memories = self.load_memories()
        summary = "\n=== LONG-TERM MEMORY ===\n"
        
        if memories['facts']:
            summary += "\nKnown Facts:\n"
            for fact in memories['facts']:
                summary += f"- {fact['content']}\n"
        
        if memories['preferences']:
            summary += "\nUser Preferences:\n"
            for key, value in memories['preferences'].items():
                summary += f"- {key}: {value}\n"
        
        return summary
