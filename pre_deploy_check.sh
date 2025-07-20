#!/bin/bash

echo ""
echo "🔧 [1] Checking required packages in requirements.txt..."
REQ_FILE="requirements.txt"
if ! grep -q "flask_cors" "$REQ_FILE"; then
    echo "❌ flask_cors not found. Adding it..."
    echo "flask_cors==6.0.1" >> "$REQ_FILE"
else
    echo "✅ flask_cors found."
fi

echo ""
echo "🔍 [2] Validating upload folder path in routes/kyc.py..."
ROUTE_FILE="routes/kyc.py"
if grep -q "UPLOAD_FOLDER = 'uploads" "$ROUTE_FILE"; then
    echo "❌ Unsafe path detected. Updating to tempfile..."
    sed -i "s|UPLOAD_FOLDER = 'uploads.*'|UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'kyc_documents')|" "$ROUTE_FILE"
    if ! grep -q "import tempfile" "$ROUTE_FILE"; then
        echo "✅ Adding tempfile import..."
        sed -i "1iimport tempfile" "$ROUTE_FILE"
    fi
else
    echo "✅ UPLOAD_FOLDER uses safe temp path."
fi

echo ""
echo "🧠 [3] Checking app.yaml configuration..."
if [ ! -f app.yaml ]; then
    echo "❌ app.yaml not found!"
    exit 1
fi
if ! grep -q "runtime: python311" app.yaml; then
    echo "❌ Incorrect runtime. Fixing..."
    sed -i "s|runtime:.*|runtime: python311|" app.yaml
else
    echo "✅ Runtime is python311."
fi
if ! grep -q "entrypoint:" app.yaml; then
    echo "❌ Missing entrypoint. Adding default..."
    echo "entrypoint: gunicorn -b :\$PORT app:app" >> app.yaml
else
    echo "✅ Entrypoint exists."
fi

echo ""
echo "📥 [4] Git pull latest code? (y/n): "
read -r GIT_PULL
if [[ "$GIT_PULL" == "y" ]]; then
    git pull origin main || echo "⚠️ Git pull failed."
fi

echo ""
echo "🚀 [5] Deploying to App Engine..."
gcloud app deploy --quiet

echo ""
echo "⏳ [6] Checking for errors in logs..."
sleep 5
LOGS=$(gcloud app logs read --limit=30 | grep -iE "ERROR|Traceback|Exception|OSError")
if [ -z "$LOGS" ]; then
    echo "✅ No critical errors found in recent logs."
else
    echo "⚠️ Errors detected:"
    echo "$LOGS"
fi

echo ""
echo "✅ Deployment check complete. Ready to test your endpoint!"
