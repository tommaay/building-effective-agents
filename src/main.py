from typing import Dict
import os
from dotenv import load_dotenv

def main() -> Dict[str, str]:
    """
    Main entry point of the application.
    
    Returns:
        Dict[str, str]: Environment information
    """
    # Load environment variables from .env file
    load_dotenv()
    
    return {
        "environment": os.getenv("ENV", "development"),
        "debug": os.getenv("DEBUG", "True")
    }

if __name__ == "__main__":
    result = main()
    print(f"Running in {result['environment']} mode") 