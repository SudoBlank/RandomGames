import os
import shutil
import subprocess

def build_game():
    print("Building Mimicraft2D for web...")
    
    # Create build directory if it doesn't exist
    if not os.path.exists("build"):
        os.makedirs("build")
    
    # Copy all necessary files to build directory
    files_to_copy = [
        "main.py",
        "Mimicraft2D.py",
        "Blockbehconfig.py",
        "Blocktexconfig.py",
        "settings.json",
        "pygbag.toml",
        "index.html"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join("build", file))
            print(f"Copied {file}")
        else:
            print(f"Warning: {file} not found")
    
    # Build with pygbag
    try:
        os.chdir("build")
        result = subprocess.run(["pygbag", "--build", "."], capture_output=True, text=True)
        print("Build output:", result.stdout)
        if result.stderr:
            print("Build errors:", result.stderr)
        
        print("Build completed successfully!")
        print("The game is ready in the build directory.")
        print("Upload the contents of the build/web directory to your web server.")
        
    except Exception as e:
        print(f"Error during build: {e}")
    finally:
        os.chdir("..")

if __name__ == "__main__":
    build_game()