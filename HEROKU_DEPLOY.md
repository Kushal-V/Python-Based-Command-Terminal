# 🚀 Heroku Deployment Guide for PyTerm

## Prerequisites

### 1. Install Heroku CLI
- **Windows**: Download from https://devcenter.heroku.com/articles/heroku-cli
- **Mac**: `brew tap heroku/brew && brew install heroku`
- **Linux**: `sudo snap install --classic heroku`

### 2. Create Heroku Account
- Sign up at: https://signup.heroku.com/
- Verify your email address

## Step-by-Step Deployment

### Step 1: Login to Heroku
```bash
heroku login
```
*This will open a browser window for authentication*

### Step 2: Create Heroku App
```bash
heroku create your-pyterm-app
```
*Replace "your-pyterm-app" with your desired app name*

### Step 3: Deploy Your Code
```bash
git push heroku main
```

### Step 4: Open Your App
```bash
heroku open
```

## Complete Commands Sequence

```bash
# 1. Login (browser authentication)
heroku login

# 2. Create app with custom name
heroku create kushal-pyterm-demo

# 3. Deploy
git push heroku main

# 4. View logs (if needed)
heroku logs --tail

# 5. Open your live app
heroku open
```

## Your App Files (Already Configured)

✅ **Procfile** - Tells Heroku how to run your app
```
web: python app.py
```

✅ **runtime.txt** - Specifies Python version
```
python-3.11.5
```

✅ **requirements.txt** - Lists dependencies
```
flask==3.0.0
Werkzeug==3.0.1
...
```

✅ **app.py** - Already configured for production
- Uses environment PORT variable
- Debug mode disabled for production

## Troubleshooting

### If deployment fails:
```bash
# Check build logs
heroku logs --tail

# Check app status
heroku ps

# Restart if needed
heroku restart
```

### Common Issues:

1. **Port Error**: Already fixed in app.py
2. **Python Version**: Specified in runtime.txt
3. **Dependencies**: Listed in requirements.txt

## Environment Variables (Optional)

```bash
# Set custom secret key
heroku config:set SECRET_KEY="your-secret-key-here"

# View all config vars
heroku config
```

## Custom Domain (Optional)

```bash
# Add custom domain
heroku domains:add yourdomain.com

# View domains
heroku domains
```

## App Management

```bash
# View app info
heroku info

# Scale dynos (free tier: 1 dyno)
heroku ps:scale web=1

# View releases
heroku releases

# Rollback if needed
heroku rollback v1
```

## Expected URLs

After deployment, your app will be available at:
- **Default**: https://your-app-name.herokuapp.com
- **Example**: https://kushal-pyterm-demo.herokuapp.com

## Final Checklist

- [ ] Heroku CLI installed
- [ ] Logged into Heroku account
- [ ] App created with unique name
- [ ] Code pushed to heroku main branch
- [ ] App opens successfully

## Free Tier Limitations

- **Dyno Hours**: 550 hours/month (enough for hobby projects)
- **Sleep Mode**: App sleeps after 30 min of inactivity
- **Wake Time**: ~10 seconds to wake up
- **Storage**: Ephemeral (files don't persist between restarts)

Perfect for your PyTerm demo since it uses virtual file system anyway!
