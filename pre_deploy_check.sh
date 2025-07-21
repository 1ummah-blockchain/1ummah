#!/bin/bash
exit 0
echo ""
echo "🔧 [1] Checking flask_cors in requirements.txt..."
if grep -q "flask_cors" requirements.txt; then
    echo "✅ flask_cors found."
else
    echo "❌ flask_cors missing. Adding it..."
    echo "flask_cors==6.0.1" >> requirements.txt
fi

echo ""
echo "🔍 [2] Validating UPLOAD_FOLDER in routes/kyc.py..."
ROUTE_FILE="routes/kyc.py"
if grep -q "UPLOAD_FOLDER = 'uploads" "$ROUTE_FILE"; then
    echo "❌ Unsafe upload path found. Updating to tempfile..."
    sed -i "s|UPLOAD_FOLDER = 'uploads.*'|UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'kyc_documents')|" "$ROUTE_FILE"
    if ! grep -q "import tempfile" "$ROUTE_FILE"; then
        echo "✅ Adding 'import tempfile' to routes/kyc.py"
        sed -i "1iimport tempfile" "$ROUTE_FILE"
    fi
else
    echo "✅ UPLOAD_FOLDER is safe."
fi

echo ""
echo "🧠 [3] Checking app.yaml config..."
if [ ! -f app.yaml ]; then
    echo "❌ app.yaml not found!"
    exit 1
fi

RUNTIME=$(grep "runtime:" app.yaml | awk '{print $2}')
ENTRY=$(grep "entrypoint:" app.yaml | cut -d':' -f2- | xargs)
if [[ "$RUNTIME" != "python311" ]]; then
    echo "❌ Invalid runtime. Fixing to python311..."
    sed -i "s|runtime:.*|runtime: python311|" app.yaml
else
    echo "✅ Runtime is python311."
fi

if [[ -z "$ENTRY" ]]; then
    echo "❌ Missing entrypoint. Adding default..."
    echo "entrypoint: gunicorn -b :\$PORT app:app" >> app.yaml
else
    echo "✅ Entrypoint exists: $ENTRY"
fi

echo ""
echo "📦 [4] Checking if app.py defines the Flask app..."
if grep -q "app = Flask(__name__)" app.py; then
    echo "✅ app.py contains Flask app."
else
    echo "❌ app.py missing Flask app. Add: app = Flask(__name__)"
    exit 1
fi

echo ""
echo "📥 [5] Pull latest code from GitHub? (y/n):"
read -r PULL_CONFIRM
if [[ "$PULL_CONFIRM" == "y" ]]; then
    git pull origin main || echo "⚠️ Git pull failed."
fi

echo ""
echo "🧹 [6] Cleaning cache and pyc files..."
rm -rf __pycache__ *.egg-info .venv
find . -name '*.pyc' -delete

echo ""
echo "🚀 [7] Deploying to App Engine..."
gcloud app deploy --quiet

echo ""
echo "⏳ [8] Waiting 5 seconds for logs..."
sleep 5

echo ""
echo "🔎 [9] Scanning recent logs for errors..."
LOGS=$(gcloud app logs read --limit=50 | grep -iE "ERROR|Traceback|Exception|OSError")
if [ -z "$LOGS" ]; then
    echo "✅ No critical errors found!"
else
    echo "⚠️ Found issues in logs:"
    echo "$LOGS"
fi

echo ""
echo "🎉 Deployment check complete. Endpoint should be ready to test!"
