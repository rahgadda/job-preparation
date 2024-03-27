#!/bin/bash

docker build -t google-genai-local-server .
# docker run -p 7860:7860 -e GOOGLE_API_KEY=--- google-genai-local-server
docker tag rahgadda/google-genai-local-server:latest
docker push rahgadda/google-genai-local-server:latest