# Azure AI Studio Assistants Sample

This sample demonstrates how to use the Azure AI Studio Assistants API to test multiple assistants with a set of input messages.

## Setup
```shell
# Create a virtual environment
python -m venv .venv
# Activate the virtual environment
source .venv/bin/activate
# Install the requirements
pip install -r requirements.txt
```

## Run
```shell
# Set the Azure OpenAI API key and Endpoint
export AZURE_OPENAI_API_KEY=<YOUR_API_KEY>
export AZURE_OPENAI_ENDPOINT=<YOUR_ENDPOINT>
# Run the sample
python main.py

# The result should be saved in the `results` folder
```