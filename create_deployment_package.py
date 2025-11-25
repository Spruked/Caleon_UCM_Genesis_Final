# UCM Caleon Genesis - Clean Deployment Package
# This script creates a clean deployment package without VS Code issues

import zipfile
import os
from pathlib import Path
from datetime import datetime

def create_clean_deployment():
    """Create a clean deployment package for GitHub"""

    print("🚀 UCM Caleon Genesis - Clean Deployment Package")
    print("=" * 50)

    # Get current directory (should be workspace root)
    workspace_dir = Path.cwd()
    print(f"📂 Workspace: {workspace_dir}")

    # Create deployment package name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"UCM_Caleon_Deployment_{timestamp}"
    package_path = workspace_dir / package_name

    print(f"📦 Creating package: {package_name}")

    # Create package directory
    package_path.mkdir(exist_ok=True)

    # Files and directories to include (exclude problematic ones)
    include_items = [
        'README.md',
        'MANIFEST.md',
        'LICENSE',
        'requirements.txt',
        'UCM/',
        'shared/',
        'ucm_core/',
        'articulator/',
        'api/',
        'seed_vaults/',
        'vault/',
        'FINAL_DEPLOY.sh',
        'separate_vault_data.sh',
        'DEPLOYMENT_SUMMARY.md',
        'CODEBASE_VERIFICATION.md'
    ]

    # Copy files
    for item in include_items:
        src = workspace_dir / item
        dst = package_path / item

        if src.exists():
            if src.is_file():
                # Copy file
                dst.parent.mkdir(parents=True, exist_ok=True)
                with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
                    fdst.write(fsrc.read())
                print(f"✅ Copied: {item}")
            elif src.is_dir():
                # Copy directory
                import shutil
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                print(f"✅ Copied: {item}/")
        else:
            print(f"⚠️  Skipped (not found): {item}")

    # Create deployment README
    deploy_readme = package_path / "DEPLOY_README.md"
    with open(deploy_readme, 'w') as f:
        f.write(f"""# UCM Caleon Genesis - Deployment Package

**Created:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Package:** {package_name}

## 🚀 Quick Deploy

1. **Extract** this package to a clean directory
2. **Navigate** to the extracted folder
3. **Run deployment:**

```bash
# Initialize git (if needed)
git init
git remote add origin https://github.com/Spruked/Caleon_UCM_Genesis_Final.git

# Add and commit
git add .
git commit -m "🎉 UCM Caleon Genesis - Sovereign Digital Entity Platform"

# Push to GitHub
git push -u origin master
```

## 🐳 Docker Deployment

```bash
cd UCM
docker-compose up --build -d
```

## 📋 What's Included

- ✅ Complete UCM Caleon Genesis codebase
- ✅ Sovereign AI architecture
- ✅ Multi-platform client libraries
- ✅ Docker production setup
- ✅ CPU-only configuration
- ✅ All documentation

## 🎯 Repository

**https://github.com/Spruked/Caleon_UCM_Genesis_Final.git**

---

**One Caleon. Everywhere. Sovereign. Ethical. Continuous.** ✨
""")

    print(f"✅ Created: DEPLOY_README.md")

    # Create ZIP file
    zip_path = workspace_dir / f"{package_name}.zip"
    print(f"📦 Creating ZIP: {zip_path.name}")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_path):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(workspace_dir)
                zipf.write(file_path, arcname)

    # Get ZIP size
    zip_size = zip_path.stat().st_size / (1024 * 1024)  # MB

    print(f"✅ Deployment package created successfully!")
    print(f"📊 Size: {zip_size:.2f} MB")
    print(f"📁 Location: {zip_path}")
    print()
    print("🎉 Ready for GitHub deployment!")
    print()
    print("Next steps:")
    print("1. Extract the ZIP to a clean directory")
    print("2. Run the git commands in DEPLOY_README.md")
    print("3. Your sovereign AI will be live worldwide!")

    return zip_path

if __name__ == "__main__":
    create_clean_deployment()