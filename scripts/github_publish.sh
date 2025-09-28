#!/usr/bin/env bash
set -e
if [ -z "$1" ]; then
  echo "Usage: $0 git@github.com:yourname/yourrepo.git"
  exit 1
fi
repo_url=$1
git init
git add .
git commit -m "Initial commit: production RAG tool (continued)"
git branch -M main
git remote add origin "$repo_url"
git push -u origin main
echo "Remember to add repository secrets: OPENAI_API_KEY, MCP_API_KEY, NOTION_TOKEN, AWS_*"
echo "Consider enabling branch protection and required status checks."
