# UCM Caleon Genesis - Deployment Copy Script
# Copies the entire workspace to the deployment directory

import shutil
import os
from pathlib import Path

def copy_ucm_to_deploy():
    # Source: Current workspace (where this script is located)
    source_dir = Path(__file__).parent

    # Destination: The deployment directory we created
    dest_dir = Path("C:/Users/bryan/Caleon_UCM_Genesis_Deploy")

    print("🚀 UCM Caleon Genesis - Deployment Copy")
    print("=" * 40)
    print(f"📂 Source: {source_dir}")
    print(f"🎯 Destination: {dest_dir}")
    print()

    if not dest_dir.exists():
        print("❌ Deployment directory not found!")
        return False

    try:
        # Copy all files and directories
        print("📦 Copying files...")
        for item in source_dir.iterdir():
            if item.name == ".git":
                continue  # Skip any existing git directories

            dest_item = dest_dir / item.name
            if item.is_file():
                shutil.copy2(item, dest_item)
                print(f"✅ Copied: {item.name}")
            elif item.is_dir():
                if dest_item.exists():
                    shutil.rmtree(dest_item)
                shutil.copytree(item, dest_item)
                print(f"✅ Copied: {item.name}/")

        print()
        print("✅ All files copied successfully!")
        print(f"📊 Ready to deploy from: {dest_dir}")
        return True

    except Exception as e:
        print(f"❌ Copy failed: {e}")
        return False

if __name__ == "__main__":
    success = copy_ucm_to_deploy()
    if success:
        print()
        print("🎉 Ready for git commit and push!")
        print("Run: git add . && git commit -m 'Initial commit' && git push -u origin master")
    else:
        print()
        print("❌ Copy failed - check paths and permissions")