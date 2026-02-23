#!/data/data/com.termux/files/usr/bin/bash
cd ~/jongpt/frontend
# Use npx serve if you don't want to install globally
npx serve -s . -l 5000 &
FRONTEND_PID=$!
echo "Frontend running at http://localhost:5000 (PID: $FRONTEND_PID)"
