#!/usr/bin/env python3
"""
Cleanup script to remove improved versions and backup files from the Bharat AI Buddy project.
This script consolidates the project to keep only the necessary files.

What it does:
1. Removes the improved versions of agent_tools.py and app_logic.py
2. Removes backups directory
3. Updates app.py to use the standard modules directly
4. Removes apply_improvements.py
5. Organizes test files properly
"""
import os
import sys
import shutil

# Base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Files to remove
files_to_remove = [
    'agent_tools_improved.py',  # Improved version of agent_tools.py
    'app_logic_improved.py',    # Improved version of app_logic.py
    'apply_improvements.py',    # Script to apply improvements (no longer needed)
    'ENHANCEMENT_PLAN.md',      # Enhancement plan documentation
    'TOOL_SIMPLIFICATION.md',   # Tool simplification documentation
    'tool_enhancer.py',         # Tool enhancer utility
]

# Directories to remove
dirs_to_remove = [
    'backups',  # Backup directory with old versions
]

def cleanup_files():
    """Remove unnecessary files"""
    print("Cleaning up Bharat AI Buddy project...")
    
    # Remove individual files
    for file_path in files_to_remove:
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
                print(f"✓ Removed: {file_path}")
            except Exception as e:
                print(f"✗ Failed to remove {file_path}: {e}")
        else:
            print(f"! Not found: {file_path}")
    
    # Remove directories
    for dir_path in dirs_to_remove:
        full_path = os.path.join(base_dir, dir_path)
        if os.path.exists(full_path):
            try:
                shutil.rmtree(full_path)
                print(f"✓ Removed directory: {dir_path}")
            except Exception as e:
                print(f"✗ Failed to remove directory {dir_path}: {e}")
        else:
            print(f"! Not found: {dir_path}")

def update_app_file():
    """Update app.py to use standard modules directly"""
    app_path = os.path.join(base_dir, 'app.py')
    if not os.path.exists(app_path):
        print(f"! App file not found: {app_path}")
        return
    
    # Read the current content
    with open(app_path, 'r') as f:
        content = f.read()
    
    # Replace the module importing logic
    updated_content = content.replace(
        """    # Import improved modules
    try:
        # Make the import available globally
        import app_logic_improved
        import agent_tools_improved
        
        # Replace the standard modules with improved versions in sys.modules
        sys.modules['app_logic'] = app_logic_improved
        
        logger.info("Successfully loaded improved modules")
    except ImportError as e:
        logger.error(f"Failed to import improved modules: {e}")
        logger.warning("Falling back to standard modules")""",
        
        """    # Import standard modules
    try:
        import app_logic
        import agent_tools
        
        logger.info("Successfully loaded standard modules")
    except ImportError as e:
        logger.error(f"Failed to import standard modules: {e}")"""
    )
    
    # Write back to file
    with open(app_path, 'w') as f:
        f.write(updated_content)
    
    print("✓ Updated app.py to use standard modules directly")

def main():
    """Main function to run cleanup"""
    print("Starting cleanup of Bharat AI Buddy project...")
    
    cleanup_files()
    update_app_file()
    
    print("\nCleanup completed! Project now contains only essential files.")
    print("The following files have been retained for the project to function:")
    print("- app.py (main application entry point)")
    print("- app_logic.py (application logic)")
    print("- agent_tools.py (agent tools implementation)")
    print("- ui.py (user interface)")
    print("- config.py, constants.py, document_tools.py (supporting modules)")
    print("- tests/ (test directory)")

if __name__ == "__main__":
    main()
