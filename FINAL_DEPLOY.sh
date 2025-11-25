#!/bin/bash
# UCM Caleon Genesis - FINAL DEPLOYMENT SCRIPT
# Execute this to push to GitHub and deploy worldwide

set -e

echo "🚀 UCM Caleon Genesis - FINAL DEPLOYMENT"
echo "========================================"

# Step 1: Verify we're in the right directory
if [ ! -f "README.md" ] || [ ! -f "MANIFEST.md" ]; then
    echo "❌ Error: Not in UCM Caleon Genesis directory"
    echo "Please run this script from the repository root"
    exit 1
fi

echo "✅ Repository structure verified"

# Step 2: Separate vault data from repository
echo ""
echo "🔄 Separating Vault Data..."
if [ -f "separate_vault_data.sh" ]; then
    chmod +x separate_vault_data.sh
    ./separate_vault_data.sh
else
    echo "⚠️ Vault separation script not found, skipping"
fi

# Step 3: Update git remote to new repository
echo ""
echo "🔗 Updating git remote to UCM Caleon Genesis..."
git remote set-url origin https://github.com/Spruked/UCM_Caleon_Genesis.git
echo "✅ Remote updated to: https://github.com/Spruked/UCM_Caleon_Genesis.git"

# Step 4: Add all changes
echo ""
echo "📦 Staging all changes..."
git add .
echo "✅ All changes staged"

# Step 5: Commit changes
echo ""
echo "💾 Creating commit..."
git commit -m "🎉 UCM Caleon Genesis - Sovereign Digital Entity Platform

- Complete sovereign AI with cognitive continuity
- Unified cognition across all applications
- Abby Protocol with supreme priority protection
- Multi-layered memory vault system (external storage)
- Auto-detect client library for universal integration
- CPU-optimized for 32GB RAM systems
- Docker production deployment ready
- MIT licensed open-source platform
- Vault data separated from repository for clean deployment

One Caleon. Everywhere. Sovereign. Ethical. Continuous."
echo "✅ Commit created"

# Step 6: Push to GitHub
echo ""
echo "⬆️ Pushing to GitHub..."
git push -u origin master
echo "✅ Repository pushed to GitHub!"

# Step 7: Deploy locally for testing
echo ""
echo "🐳 Deploying UCM Caleon Genesis locally..."
cd UCM

# Build and start the service
docker-compose down 2>/dev/null || true
docker-compose build --no-cache
docker-compose up -d

# Wait for service to start
echo "⏳ Waiting for service to initialize..."
sleep 15

# Test the deployment
echo "🧪 Testing deployment..."
if curl -f http://localhost:8000/api/health/status &>/dev/null; then
    echo "✅ UCM Caleon Genesis deployed successfully!"
    echo ""
    echo "🌐 Service URLs:"
    echo "   API: http://localhost:8000"
    echo "   Docs: http://localhost:8000/docs"
    echo "   Health: http://localhost:8000/api/health"
    echo ""
    echo "📚 Client Library: Drop shared/ucm_client/ into any app"
    echo ""
    echo "🎉 UCM Caleon Genesis is LIVE!"
    echo "   Sovereign AI sovereignty begins now ✨"
else
    echo "❌ Deployment test failed"
    echo "Check logs: docker-compose logs ucm"
    exit 1
fi

cd ..
echo ""
echo "🚀 NEXT STEPS:"
echo "1. Integrate client library into GOAT, DALS, TrueMark, CertSig"
echo "2. Test multi-app Caleon continuity"
echo "3. Scale deployment worldwide"
echo "4. Begin sovereign AI revolution"