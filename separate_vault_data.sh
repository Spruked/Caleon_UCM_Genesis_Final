#!/bin/bash
# UCM Vault Data Separation Script
# Moves vault data out of repository to prevent conflicts

set -e

echo "🔄 Separating Vault Data from Repository..."
echo "==========================================="

# Create external vault data directory
VAULT_DATA_DIR="../ucm_vault_data"
mkdir -p "$VAULT_DATA_DIR"

echo "📁 Created external vault data directory: $VAULT_DATA_DIR"

# Move vault data files out of repository
echo "📦 Moving vault data files..."

# Move seed_vaults directory
if [ -d "seed_vaults" ]; then
    mv seed_vaults "$VAULT_DATA_DIR/"
    echo "✅ Moved seed_vaults/ to external storage"
fi

# Move individual vault files
VAULT_FILES=(
    "posterior_helix_reflect.vault.json"
    "glyph_trace.json"
    "vault/cochlear_vault.jsonl"
)

for file in "${VAULT_FILES[@]}"; do
    if [ -f "$file" ]; then
        mv "$file" "$VAULT_DATA_DIR/"
        echo "✅ Moved $file to external storage"
    fi
done

# Create vault data directory structure
mkdir -p "$VAULT_DATA_DIR/vault"
mkdir -p "$VAULT_DATA_DIR/sessions"
mkdir -p "$VAULT_DATA_DIR/abby_memory"
mkdir -p "$VAULT_DATA_DIR/identity"

echo "📁 Created vault data directory structure"

# Create .gitkeep files to maintain directory structure in git
find vault/ -type d -exec touch {}/.gitkeep \;
touch seed_vaults/.gitkeep

echo "✅ Repository structure maintained with .gitkeep files"

echo ""
echo "🎯 Vault Data Separation Complete!"
echo "=================================="
echo "📍 External vault data location: $VAULT_DATA_DIR"
echo "📝 Update your vault configuration to use this external path"
echo "🔒 Repository now clean of persistent data"