# Conda Environment Setup for WSG MCP Server

## Create Conda Environment

```bash
# Create conda environment with Python 3.12
conda create -n wsg-courses-mcp python=3.12 -y

# Activate the environment
conda activate wsg-courses-mcp

# Install dependencies
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt
```

## Alternative: Create from environment.yml

```bash
conda env create -f environment.yml
conda activate wsg-courses-mcp
```

## Managing the Environment

```bash
# Activate environment
conda activate wsg-courses-mcp

# Deactivate environment
conda deactivate

# List all conda environments
conda env list

# Remove environment
conda env remove -n wsg-courses-mcp

# Export environment
conda env export > environment.yml
```

## Verify Installation

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Run the server
python main.py
```
