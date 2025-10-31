# Model Setup Instructions

## Why Models Are Not Included in Git

The AI models (phi3:mini) are approximately **2GB** in size, which exceeds GitHub's file size limits. Instead of including them in the repository, they are downloaded automatically when you first run the application.

## Automatic Model Download

Both `demo.py` and `demo-Win.py` will automatically:
1. Check if the phi3:mini model exists
2. Download it if missing using `ollama pull phi3:mini`
3. Store it locally in `model/ollama_models/`

## Manual Model Setup

If you prefer to download the model manually:

### macOS/Linux:
```bash
cd GenAI-Demo
ollama pull phi3:mini
```

### Windows:
```cmd
cd GenAI-Demo
ollama pull phi3:mini
```

## Model Storage Location

Models are stored in:
- **Path**: `model/ollama_models/`
- **Size**: ~2.2 GB for phi3:mini
- **Structure**: 
  ```
  model/ollama_models/
  ├── blobs/          # Model binary data
  └── manifests/      # Model metadata
  ```

## Benefits of This Approach

✅ **GitHub-compatible**: Repository stays under size limits  
✅ **Always fresh**: Users get the latest model version  
✅ **Bandwidth-efficient**: Only download when needed  
✅ **Cross-platform**: Works the same on all systems  

## Troubleshooting

**Model download fails?**
- Check internet connection
- Verify Ollama is installed and in PATH
- Try manual download: `ollama pull phi3:mini`
- On Windows, use `troubleshoot-windows.bat`

**Model seems corrupted?**
- Delete model folder: `rm -rf model/ollama_models/`
- Re-run the application to re-download

The model will be automatically managed by your GenAI Demo application! 🚀