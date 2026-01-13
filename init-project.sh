#!/bin/bash

# Solo Agent Agile Project Initializer
# Usage: ./init-project.sh [agent-name]

set -e

AGENT_NAME=${1:-"MyAgent"}

echo "=== Solo Agent Agile Project Initializer ==="
echo "Build AI Agents powered by Claude Code"
echo ""
echo "Agent Name: $AGENT_NAME"
echo ""

# Function to replace placeholders
replace_placeholders() {
    local file=$1
    if [[ -f "$file" ]]; then
        sed -i "s/\[AGENT_NAME\]/$AGENT_NAME/g" "$file" 2>/dev/null || true
        sed -i "s/\[PROJECT_NAME\]/$AGENT_NAME/g" "$file" 2>/dev/null || true
        sed -i "s/\[DATE\]/$(date +%Y-%m-%d)/g" "$file" 2>/dev/null || true
    fi
}

# Step 0: Check for Claude Code CLI
echo "[0/8] Checking for Claude Code CLI..."
if command -v claude &> /dev/null; then
    echo "  ✓ Claude Code CLI found"
else
    echo "  ⚠ Claude Code CLI not found!"
    echo "  Install with: npm install -g @anthropic-ai/claude-code"
    echo ""
fi

# Step 1: Initialize git if not already
if [[ ! -d ".git" ]]; then
    echo "[1/8] Initializing git repository..."
    git init
else
    echo "[1/8] Git repository already exists."
fi

# Step 2: Copy environment files
echo "[2/8] Setting up environment files..."
if [[ ! -f "backend/.env" ]]; then
    cp backend/.env.example backend/.env
    echo "  Created backend/.env"
    echo "  ⚠ Don't forget to add your ANTHROPIC_API_KEY!"
fi

# Step 3: Replace placeholders in key files
echo "[3/8] Customizing project files..."
replace_placeholders "CLAUDE.md"
replace_placeholders "ROADMAP.md"
replace_placeholders "STATUS.md"
replace_placeholders "README.md"
replace_placeholders "frontend/index.html"
replace_placeholders "frontend/src/pages/HomePage.tsx"
replace_placeholders "backend/.env"
replace_placeholders "backend/src/config/settings.py"
replace_placeholders "backend/src/modules/agent/prompts/system.md"

# Step 4: Create first epic from template
if [[ ! -d "epics/01-agent-setup" ]]; then
    echo "[4/8] Creating initial epic..."
    cp -r epics/00-template epics/01-agent-setup
    sed -i "s/\[Epic Name\]/Agent Setup/g" epics/01-agent-setup/EPIC.md 2>/dev/null || true
    sed -i "s/\[NN\]/01/g" epics/01-agent-setup/EPIC.md 2>/dev/null || true
else
    echo "[4/8] Initial epic already exists."
fi

# Step 5: Generate SECRET_KEY if not set
echo "[5/8] Generating secret key..."
if grep -q "change-this-to-a-secure" backend/.env 2>/dev/null; then
    NEW_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || openssl rand -base64 32)
    sed -i "s/change-this-to-a-secure-random-string-min-32-chars/$NEW_SECRET/g" backend/.env 2>/dev/null || true
    echo "  Generated new SECRET_KEY."
fi

# Step 6: Create Python virtual environment
echo "[6/8] Setting up Python virtual environment..."
if [[ ! -d "backend/.venv" ]]; then
    cd backend
    python3 -m venv .venv
    cd ..
    echo "  Created backend/.venv"
else
    echo "  Virtual environment already exists."
fi

# Step 7: Create agent workspace directory
echo "[7/8] Creating agent workspace directory..."
mkdir -p /tmp/agent_workspaces
echo "  Created /tmp/agent_workspaces"

# Step 8: Update STATUS.md with current date
echo "[8/8] Updating status..."
sed -i "s/Last Updated: \[DATE\]/Last Updated: $(date +%Y-%m-%d)/g" STATUS.md 2>/dev/null || true

echo ""
echo "=== Initialization Complete ==="
echo ""
echo "Your agent '$AGENT_NAME' is ready for development!"
echo ""
echo "Next steps:"
echo ""
echo "  1. Add your API key to backend/.env:"
echo "     ANTHROPIC_API_KEY=sk-ant-..."
echo ""
echo "  2. Edit your agent's personality:"
echo "     backend/src/modules/agent/prompts/system.md"
echo ""
echo "  3. Install dependencies & run:"
echo "     make install"
echo "     make db-start"
echo "     make dev"
echo ""
echo "     Frontend: http://localhost:3000"
echo "     Backend:  http://localhost:8000"
echo ""
echo "With Claude Code:"
echo "  claude"
echo "  > /project:context"
echo ""
