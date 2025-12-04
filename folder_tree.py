#!/usr/bin/env python3
"""
UCM Folder Tree Generator
Shows main folders and design files for the Unified Cognitive Model
"""
import os
import sys
from pathlib import Path

def should_include_file(filename):
    """Check if file should be included in the tree"""
    # Include design/architecture files
    design_files = {
        'README.md', 'SYSTEM_ARCHITECTURE.md', 'DEPLOYMENT_INSTRUCTIONS.md',
        'INTEGRATION_GUIDE.md', 'MANIFEST.md', 'PHASE_8_COMPLETE.md',
        'CODEBASE_VERIFICATION.md', 'CYCLE_QUICK_REFERENCE.md',
        'DEPLOYMENT_SUMMARY.md', 'CONTRIBUTING.md', 'LICENSE',
        'CONSENT_API_GUIDE.md', 'CONSENT_AUDIT_VOICE_GUIDE.md'
    }

    # Include config files
    config_files = {
        'docker-compose.yml', 'docker-compose.prod.yml', 'docker-compose.full.yml',
        'Dockerfile', 'Dockerfile.prod', 'requirements.txt', 'requirements.prod.txt',
        'config.py', 'config_whisper.json', 'settings.json', 'nginx.conf',
        'cloudflared.yml', 'database_init.sql', 'mongo_init.js'
    }

    # Include main application files
    main_files = {
        'main.py', 'routes.py', 'telemetry.py', 'vault_api.py',
        'voice_consent.py', 'voice_processor.py', 'unified_loop.py',
        'CORE_ARTICULATION_CYCLE.py', 'articulation_bridge.py',
        'reflection_vault.py', 'symbolic_memory_vault.py',
        'mongo_reflection_vault.py', 'cochlear_vault.py'
    }

    # Include startup/deployment scripts
    script_files = {
        'start_ucm.bat', 'start_ucm.ps1', 'deploy_ucm.sh',
        'build-optimized.sh', 'FINAL_DEPLOY.sh', 'create_deployment_package.py',
        'copy_to_deploy.py', 'separate_vault_data.sh'
    }

    return (filename in design_files or
            filename in config_files or
            filename in main_files or
            filename in script_files or
            filename.endswith('.py') and not filename.startswith('__') and not filename.startswith('test_'))

def should_include_dir(dirname):
    """Check if directory should be included"""
    main_dirs = {
        'api', 'articulator', 'cerebral_cortex', 'cochlear_processor_v2.0',
        'comms', 'draft_engine', 'echoripple', 'echostack', 'examples',
        'frontend', 'generative', 'glyphs', 'gyro_cortical_harmonizer_module',
        'ISS', 'ISS_Module', 'modules', 'monitoring', 'nginx', 'persona',
        'Phonatory_Output_Module', 'posterior_helix', 'shared', 'synaptic_resonator_core',
        'UCM', 'ucm_core', 'utils', 'Vault_System_1.0', 'anterior_helix'
    }

    return dirname in main_dirs

def print_tree(path, prefix="", max_depth=3, current_depth=0):
    """Print directory tree"""
    if current_depth > max_depth:
        return

    try:
        items = sorted(os.listdir(path))
    except PermissionError:
        return

    # Separate directories and files
    dirs = []
    files = []

    for item in items:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            if should_include_dir(item):
                dirs.append(item)
        else:
            if should_include_file(item):
                files.append(item)

    # Print directories first
    for i, dirname in enumerate(dirs):
        is_last = (i == len(dirs) - 1) and len(files) == 0
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{dirname}/")
        extension = "    " if is_last else "│   "
        print_tree(os.path.join(path, dirname), prefix + extension, max_depth, current_depth + 1)

    # Print files
    for i, filename in enumerate(files):
        is_last = i == len(files) - 1
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{filename}")

def main():
    workspace = Path(__file__).parent
    print("UCM Cognitive Architecture - Folder Structure")
    print("=" * 50)
    print(f"{workspace.name}/")
    print_tree(workspace, "", max_depth=2)

    print("\n" + "=" * 50)
    print("Legend:")
    print("├── Main application modules and cognitive components")
    print("├── Configuration and deployment files")
    print("├── Documentation and architecture guides")
    print("└── Integration and utility scripts")

if __name__ == "__main__":
    main()