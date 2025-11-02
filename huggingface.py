# Hugging Face Spaces configuration helper

import os
from pathlib import Path


def setup_huggingface_space():
    """Helper function to set up the application for Hugging Face Spaces deployment."""
    
    # This function can be called during deployment to ensure proper setup
    # Check if we're running on HF Spaces
    hf_space = os.getenv('HF_SPACE')
    hf_agent = os.getenv('HF_AGENT')
    hf_model = os.getenv('HF_MODELC)
    
    print(f"HF Spaces Environment:")
    print(f"  HF_SPACE: {hf_space}")
    print(f"  HF_AGENT: {hf_agent}")
    print(f"  HF_MODEL: {hf_model}")
    
    # Verify required files exist for HF Spaces
    required_files = [
        'app.py',
        'api_client.py', 
        'utils.py',
        'requirements.txt',
        'README.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        raise FileNotFoundError(f"Missing required files for HF Spaces: {missing_files}")
    
    print("✅ All required files found for HF Spaces deployment")
    
    # Check for API keys (these should be set as secrets)
    openrouter_key = os.getenv('OPENROUTER_API_KEY')
    cerebras_key = os.getenv('CEREBRAS_API_KEY')
    
    if not openrouter_key:
        print("⚠️  OPENROUTER_API_KEY not found - set this in HF Spaces Secrets")
    else:
        print("✅ OPENROUTER_API_KEY configured")
        
    if not cerebras_key:
        print("⚠️  CEREBRAS_API_KEY not found - set this in HF Spaces Secrets")
    else:
        print("✅ CEREBRAS_API_KEY configured")
    
    return True


if __name__ == "__main__":
    # Run setup check
    setup_huggingface_space()
