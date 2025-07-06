#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Launching FastAPI server..."
uvicorn app.main:app --reload
