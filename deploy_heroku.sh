#!/bin/bash
echo "🚀 PyTerm Heroku Deployment Script"
echo ""

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed."
    echo "Please install it from: https://devcenter.heroku.com/articles/heroku-cli"
    echo "Then restart this script."
    exit 1
fi

echo "✅ Heroku CLI found"

# Login to Heroku
echo "🔑 Logging into Heroku (browser will open)..."
heroku login

# Prompt for app name
read -p "Enter your app name (e.g., kushal-pyterm-demo): " APP_NAME

# Create Heroku app
echo "📦 Creating Heroku app: $APP_NAME"
heroku create $APP_NAME

# Deploy to Heroku
echo "🚀 Deploying to Heroku..."
git push heroku main

# Open the app
echo "🌐 Opening your live app..."
heroku open

echo ""
echo "✅ Deployment complete!"
echo "Your app is live at: https://$APP_NAME.herokuapp.com"
echo ""
echo "📊 Useful commands:"
echo "  heroku logs --tail    (view logs)"
echo "  heroku restart        (restart app)"
echo "  heroku open          (open app)"
echo ""
