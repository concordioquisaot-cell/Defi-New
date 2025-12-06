import os
import re

def fix_html_links(folder_path):
    """
    Fix absolute paths in HTML files to relative paths
    """
    # Get all HTML files in the folder
    html_files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
    
    print(f"Found {len(html_files)} HTML files:")
    for file in html_files:
        print(f"  - {file}")
    
    # Patterns to find and remove
    patterns_to_remove = [
        r'C:\\\\Users\\\\Dell\\\\Downloads\\\\Defi\\\\',  # Windows path with backslashes
        r'C:/Users/Dell/Downloads/Defi/',                 # Windows path with forward slashes
        r'file:///C:/Users/Dell/Downloads/Defi/',         # File protocol path
        r'C:\\Users\\Dell\\Downloads\\Defi\\',            # Single backslashes
    ]
    
    files_fixed = 0
    links_fixed = 0
    
    for html_file in html_files:
        file_path = os.path.join(folder_path, html_file)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original_content = content
            
            # Remove all the absolute path patterns
            for pattern in patterns_to_remove:
                content = re.sub(pattern, '', content)
            
            # Also fix any remaining absolute paths that might have different formats
            content = re.sub(r'[A-Z]:\\\\.*?Defi\\\\', '', content)
            
            # Fix href attributes that might have been partially fixed
            content = re.sub(r'href="\s*"', 'href="#"', content)  # Fix empty hrefs
            content = re.sub(r'src="\s*"', 'src="#"', content)    # Fix empty src
            
            if content != original_content:
                # Count how many links were fixed
                changes = len(re.findall(r'href="[^"]*"', original_content)) - len(re.findall(r'href="[^"]*"', content))
                links_fixed += changes
                
                # Save the fixed content
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                files_fixed += 1
                print(f"✓ Fixed {html_file}")
        
        except Exception as e:
            print(f"✗ Error processing {html_file}: {e}")
    
    print(f"\n✅ Fixed {links_fixed} links in {files_fixed} files")
    return files_fixed

def create_backup(folder_path):
    """
    Create a backup of all HTML files before modifying
    """
    backup_folder = os.path.join(folder_path, 'backup')
    os.makedirs(backup_folder, exist_ok=True)
    
    html_files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
    
    for file in html_files:
        src = os.path.join(folder_path, file)
        dst = os.path.join(backup_folder, file)
        
        with open(src, 'r', encoding='utf-8') as source:
            content = source.read()
        
        with open(dst, 'w', encoding='utf-8') as destination:
            destination.write(content)
    
    print(f"📁 Backup created in: {backup_folder}")
    return backup_folder

def add_navigation_to_all_files(folder_path):
    """
    Add consistent navigation to all HTML files
    """
    html_files = ['index.html', 'Defi1.html', 'Defi2.html', 'Defi3.html', 'Defi4.html', 'Defi5.html']
    
    navigation_template = '''
    <nav style="background: #f0f0f0; padding: 10px; margin-bottom: 20px; border-radius: 5px;">
        <a href="index.html">Home</a> | 
        <a href="Defi1.html">DeFi 1</a> | 
        <a href="Defi2.html">DeFi 2</a> | 
        <a href="Defi3.html">DeFi 3</a> | 
        <a href="Defi4.html">DeFi 4</a> | 
        <a href="Defi5.html">DeFi 5</a>
    </nav>
    '''
    
    files_updated = 0
    
    for html_file in html_files:
        file_path = os.path.join(folder_path, html_file)
        
        if not os.path.exists(file_path):
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Check if navigation already exists
            if '<nav' not in content or 'DeFi 1</a>' not in content:
                # Find the body tag and add navigation after it
                body_pos = content.find('<body>')
                if body_pos != -1:
                    # Insert navigation after <body> tag
                    insert_pos = body_pos + 6  # Length of '<body>'
                    new_content = content[:insert_pos] + navigation_template + content[insert_pos:]
                    
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    
                    files_updated += 1
                    print(f"✓ Added navigation to {html_file}")
        
        except Exception as e:
            print(f"✗ Error updating {html_file}: {e}")
    
    print(f"\n✅ Navigation added to {files_updated} files")
    return files_updated

def main():
    # Get current folder
    current_folder = os.getcwd()
    print(f"Working in folder: {current_folder}")
    
    # Create backup first
    create_backup(current_folder)
    
    # Fix the links
    print("\n" + "="*50)
    print("Fixing absolute paths to relative paths...")
    print("="*50)
    fix_html_links(current_folder)
    
    # Add navigation
    print("\n" + "="*50)
    print("Adding consistent navigation...")
    print("="*50)
    add_navigation_to_all_files(current_folder)
    
    print("\n" + "="*50)
    print("✅ ALL FILES HAVE BEEN FIXED!")
    print("="*50)
    print("\nNext steps:")
    print("1. Open index.html in your browser")
    print("2. Test all links")
    print("3. Run: git add .")
    print("4. Run: git commit -m 'Fixed all links'")
    print("5. Run: git push origin main")

if __name__ == "__main__":
    main()