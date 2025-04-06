# Phi-4 API

A Flask API server using the Phi-4-mini model. Can be deployed locally or on Replit.

## Overview

This project is a Flask application that provides Microsoft's small language model Phi-4-mini as an API using the llama.cpp library. It uses a quantized model (GGUF format) which allows it to run with relatively few resources.

## Features

- Standard text generation API
- Streaming response API
- Model information API
- Simple web interface

## Setup Instructions

### Running Locally

1. Clone the repository
```bash
git clone https://github.com/yourusername/phi-4-api.git
cd phi-4-api
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Download the model
```bash
python download_model.py
```

4. Start the application
```bash
python app.py
```

### Running on Replit

1. Import this repository into Replit
   - From the Replit dashboard, click "+ Create Repl" → "Import from GitHub"
   - Enter the repository URL

2. Run the setup script
```bash
python setup.py
```

3. Start the application
```bash
python main.py
```

## API Endpoints

### Text Generation (`/api/generate`)
- Method: POST
- Parameters:
  - `prompt`: Prompt for generation (required)
  - `max_tokens`: Maximum number of tokens to generate (optional, default: 256)
  - `temperature`: Temperature parameter for generation (optional, default: 0.7)

### Streaming Response (`/api/generate_stream`)
- Method: POST
- Parameters: Same as `/api/generate`

### Model Information (`/api/info`)
- Method: GET
- Response: JSON containing model name, context length, and application version

## Customization

Settings can be modified in the `config.py` file:
- Model path
- Context length
- Batch size
- Maximum tokens
- Temperature parameter
- Stop tokens

## License

This project is released under the MIT license.

## Notes

- The Phi-4-mini model was developed by Microsoft and is subject to a separate license.
- For production use, consider implementing proper error handling, authentication, and scaling.