import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class OutputType(Enum):
    """Output types for debugging"""
    EXACT_PROMPT = 'exactPrompt'
    CONTEXT_STATE = 'contextState'
    STRUCTURED = 'structured'


class PromptDebugger:
    """
    Helper class for debugging and logging LLM prompts
    
    Note: This is a simplified Python version. The node-llama-cpp library has specific
    features for capturing context state that don't have direct equivalents in llama-cpp-python.
    This class focuses on logging prompts and responses for debugging purposes.
    """
    
    def __init__(self, options: Optional[Dict[str, Any]] = None):
        options = options or {}
        self.output_dir = options.get('outputDir', './')
        self.filename = options.get('filename', 'debug_output.txt')
        self.include_timestamp = options.get('includeTimestamp', False)
        self.append_mode = options.get('appendMode', False)
        
        # Configure which outputs to include
        output_types = options.get('outputTypes', [OutputType.EXACT_PROMPT])
        if not isinstance(output_types, list):
            output_types = [output_types]
        self.output_types = output_types
        
        # Ensure output directory exists
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    
    def capture_exact_prompt(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Captures the exact prompt (user input + system + functions)
        
        Args:
            params: Dictionary containing 'messages', 'functions' (optional)
        """
        messages = params.get('messages', [])
        functions = params.get('functions', [])
        
        # Format the prompt
        formatted_prompt = self._format_messages(messages)
        
        if functions:
            formatted_prompt += "\n\n=== Available Functions ===\n"
            formatted_prompt += json.dumps(functions, indent=2)
        
        return {
            'exactPrompt': formatted_prompt,
            'timestamp': datetime.now().isoformat(),
            'messages': messages,
            'functions': functions
        }
    
    def capture_response(self, response: str) -> Dict[str, Any]:
        """
        Captures the model response
        
        Args:
            response: The model's response text
        """
        return {
            'response': response,
            'timestamp': datetime.now().isoformat()
        }
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """Format messages for display"""
        formatted = ""
        for msg in messages:
            role = msg.get('role', 'unknown').upper()
            content = msg.get('content', '')
            formatted += f"\n=== {role} ===\n{content}\n"
        return formatted
    
    def capture_all(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Captures all configured output types
        
        Args:
            params: Dictionary with 'messages', 'functions', 'response' (optional)
        """
        result = {
            'timestamp': datetime.now().isoformat()
        }
        
        if OutputType.EXACT_PROMPT in self.output_types:
            exact_data = self.capture_exact_prompt(params)
            result.update(exact_data)
        
        if 'response' in params:
            response_data = self.capture_response(params['response'])
            result.update(response_data)
        
        return result
    
    def format_output(self, captured_data: Dict[str, Any]) -> str:
        """
        Formats the captured data for output
        
        Args:
            captured_data: Data from capture methods
        """
        output = "\n========== PROMPT DEBUG OUTPUT ==========\n"
        output += f"Timestamp: {captured_data.get('timestamp', 'N/A')}\n"
        
        if 'exactPrompt' in captured_data:
            output += "\n=== EXACT PROMPT ===\n"
            output += captured_data['exactPrompt']
            output += "\n"
        
        if 'response' in captured_data:
            output += "\n=== MODEL RESPONSE ===\n"
            output += captured_data['response']
            output += "\n"
        
        if 'functions' in captured_data and captured_data['functions']:
            output += f"\nFunctions: {len(captured_data['functions'])} available\n"
        
        output += "==========================================\n"
        return output
    
    def save_to_file(self, captured_data: Dict[str, Any], custom_filename: Optional[str] = None) -> str:
        """
        Saves data to file
        
        Args:
            captured_data: Data to save
            custom_filename: Optional custom filename
            
        Returns:
            Path to the saved file
        """
        content = self.format_output(captured_data)
        
        filename = custom_filename or self.filename
        
        if self.include_timestamp:
            timestamp = datetime.now().isoformat().replace(':', '-').replace('.', '-')
            ext = Path(filename).suffix
            base = Path(filename).stem
            filename = f"{base}_{timestamp}{ext}"
        
        filepath = Path(self.output_dir) / filename
        
        mode = 'a' if self.append_mode else 'w'
        with open(filepath, mode, encoding='utf-8') as f:
            f.write(content)
        
        print(f"Prompt debug output written to {filepath}")
        return str(filepath)
    
    def debug(self, params: Dict[str, Any], custom_filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Debug with configured output types
        
        Args:
            params: All parameters (messages, functions, response, etc.)
            custom_filename: Optional custom filename
            
        Returns:
            Dictionary with 'capturedData' and 'filepath' keys
        """
        captured_data = self.capture_all(params)
        filepath = self.save_to_file(captured_data, custom_filename)
        return {'capturedData': captured_data, 'filepath': filepath}
    
    def log_to_console(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log to console only
        
        Args:
            params: Parameters based on configured output types
            
        Returns:
            Captured data
        """
        captured_data = self.capture_all(params)
        print(self.format_output(captured_data))
        return captured_data


# Quick utility functions
def debug_prompt(messages: List[Dict[str, str]], functions: Optional[List[Dict]] = None, 
                 response: Optional[str] = None, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Quick function to debug a prompt
    
    Args:
        messages: List of message dictionaries
        functions: Optional list of function definitions
        response: Optional model response
        options: Optional debugger options
    """
    debugger = PromptDebugger(options)
    params = {
        'messages': messages,
        'functions': functions or [],
    }
    if response:
        params['response'] = response
    return debugger.debug(params)


def log_prompt(messages: List[Dict[str, str]], functions: Optional[List[Dict]] = None,
               response: Optional[str] = None) -> None:
    """
    Quick function to log a prompt to console
    
    Args:
        messages: List of message dictionaries
        functions: Optional list of function definitions
        response: Optional model response
    """
    debugger = PromptDebugger()
    params = {
        'messages': messages,
        'functions': functions or [],
    }
    if response:
        params['response'] = response
    debugger.log_to_console(params)
