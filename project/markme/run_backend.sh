#!/bin/bash
# run_backend.sh - Start the Hajri Hub AI Attendance Backend
# Usage: ./run_backend.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo "🚀 Hajri Hub AI Attendance Backend"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Activate venv
source "$SCRIPT_DIR/venv/bin/activate"

# Navigate to backend dir
cd "$SCRIPT_DIR/backend"

# Run migrations
echo "📦 Applying migrations..."
python manage.py migrate --run-syncdb 2>&1 | grep -E "OK|No|error" | head -5
echo ""

# Collect static files (for admin panel CSS/JS)
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput 2>&1 | tail -1
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Backend running at:  http://127.0.0.1:8000"
echo "📖 Admin panel:         http://127.0.0.1:8000/admin/"
echo "   Login:               admin@hajrihub.ai / admin1234"
echo ""
echo "🔌 WebSocket:           ws://127.0.0.1:8000/ws/attendance/live/"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start with Daphne (ASGI – supports HTTP + WebSocket)
daphne -p 8000 -b 0.0.0.0 backend.asgi:application
