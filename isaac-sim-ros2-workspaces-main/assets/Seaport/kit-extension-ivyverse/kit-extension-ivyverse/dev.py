"""
Development helper script for Ivyverse extension
"""
import os
import sys
import argparse
import subprocess
def main():
    parser = argparse.ArgumentParser(description="Ivyverse development helper")
    parser.add_argument("action", choices=["test", "link", "build"], 
                       help="Action to perform")
    
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if args.action == "test":
        # Run tests
        test_cmd = [
            sys.executable,
            "-m", "pytest",
            os.path.join(script_dir, "exts/omni.ivyverse/omni/ivyverse/tests"),
            "-v"
        ]
        subprocess.run(test_cmd)
    
    elif args.action == "link":
        # Link to kit-app-template
        if sys.platform == "win32":
            link_script = os.path.join(script_dir, "link_app.bat")
        else:
            link_script = os.path.join(script_dir, "link_app.sh")
            os.chmod(link_script, 0o755)
        
        subprocess.run([link_script])
    
    elif args.action == "build":
        print("Build action not implemented yet")
if __name__ == "__main__":
    main()
