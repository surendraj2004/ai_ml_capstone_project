#!/bin/bash

echo "Starting Zepto Support Assistant..."

export MOCK_LLM=1

python -m streamlit run app.py