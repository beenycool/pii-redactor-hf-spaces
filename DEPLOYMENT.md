# Quick deployment guide for Hugging Face Spaces

## Automated Deployment Script

Run this script to prepare and validate your files for HF Spaces:

```bash
python huggingface.py
```

## Manual HF Spaces Deployment Steps

### Step 1: Create New Space
1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Choose **Gradio** as the SDK
4. Name your space (e.g., `pii-redactor-court-docs`)
5. Set visibility (Public/Private)
6. Click "Create a Space"

### Step 2: Upload Files
Upload these files in this order:
1. ✅ **app.py** - Main Gradio application
2. ✅ **api_client.py** - OpenRouter and Cerebras API clients
3. ✅ **utils.py** - Text processing and PII utilities
4. ✅ **requirements.txt** - Python dependencies
5. ✅ **README.md** - Documentation and usage
6. ✅ **env.example** - Environment variable template
7. ✅ **huggingface.py** - Deployment helper (optional)

### Step 3: Configure Secrets
In your Space's Settings → Secrets, add:

**Required:**
- `OPENROUTER_API_KEY` = `your_openrouter_key_here`
- `CEREBRAS_API_KEY` = `your_cerebras_key_here`

**Optional:**
- `OPENROUTER_SITE_URL` = `https://huggingface.co/spaces/your-username/your-space`
- `OPENROUTER_APP_NAME` = `PII Redactor`
- `CEREBRAS_MODEL` = `llama3.1-8b-instruct`

### Step 4: Build and Launch
1. Commit your changes
2. Wait for the build to complete (usually 3-5 minutes)
3. Your app will be available at: `https://your-username-your-space.hf.space`

## API Key Setup

### OpenRouter API Key
1. Visit https://openrouter.ai
2. Sign up for account
3. Go to dashboard and generate API key
4. Copy the key and add as secret in HF Spaces

### Cerebras API Key  
1. Visit https://inference.cerebras.ai/
2. Sign up for account
3. Get API key from dashboard
4. Copy the key and add as secret in HF Spaces

## Troubleshooting

**Build Fails:**
- Check that all required files are uploaded
- Verify `requirements.txt` has correct dependencies
- Check logs for any import errors

**Runtime Errors:**
- Verify API keys are set in Secrets
- Check that port is properly configured
- Ensure app.py launches on port specified by environment

**API Errors:**
- Test API keys outside of HF Spaces first
- Check rate limits for free tier APIs
- Verify model names are correct

## Files Structure in HF Space
```
pii-redactor/
├── app.py              # Main application
├── api_client.py       # LLM API integrations  
├── utils.py            # Text processing utilities
├── requirements.txt    # Python dependencies
├── README.md           # Documentation
├── env.example         # Environment template
└── huggingface.py      # Deployment helper
```

## Testing Your Deployment
1. Open your Space URL
2. Try the sample court document from README.md
3. Test both OpenRouter and Cerebras providers
4. Verify download functionality works
5. Test validation features

Your PII redactor is now ready for production use! 🎉
