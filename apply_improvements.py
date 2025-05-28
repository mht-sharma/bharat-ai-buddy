# Update script to switch from original to improved implementations
import os
import shutil

# Paths
base_dir = '/Users/mohitsharma/Downloads/apce'
original_agent_tools = os.path.join(base_dir, 'agent_tools.py')
improved_agent_tools = os.path.join(base_dir, 'agent_tools_improved.py')
original_app_logic = os.path.join(base_dir, 'app_logic.py')
improved_app_logic = os.path.join(base_dir, 'app_logic_improved.py')

# Backup original files
backup_dir = os.path.join(base_dir, 'backups')
os.makedirs(backup_dir, exist_ok=True)

# Create backups
shutil.copy2(original_agent_tools, os.path.join(backup_dir, 'agent_tools.py.bak'))
shutil.copy2(original_app_logic, os.path.join(backup_dir, 'app_logic.py.bak'))

# Replace with improved versions
shutil.copy2(improved_agent_tools, original_agent_tools)
shutil.copy2(improved_app_logic, original_app_logic)

print("Successfully updated Bharat AI Buddy with improved agent augmentation!")
print("Original files backed up in:", backup_dir)
print("Run the app as normal - it now uses the enhanced implementation.")
print("\nKey improvements:")
print("1. Tools now provide factual context rather than replacing LLM responses")
print("2. Cultural and exam tools retrieve relevant information from Wikipedia and web")
print("3. Math problems show computational steps alongside LLM explanations")
print("4. Document analysis extracts key information instead of truncating")
print("5. App logic uses a judicious blend of tool augmentation and LLM capabilities")
