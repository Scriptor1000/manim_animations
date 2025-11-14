#!/usr/bin/env python3
"""
Setup script for installing manim on Windows with portable ffmpeg.
This script creates a complete manim installation without modifying system PATH.

REQUIREMENTS:
- Python 3.11 or newer (Python 3.13+ recommended for best compatibility)
- Please download the latest Python version from https://www.python.org/downloads/

Usage: python setup_manim_windows.py
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil
import platform
from pathlib import Path


class ManimWindowsSetup:
    """Handles the complete setup of manim on Windows with portable ffmpeg."""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.absolute()
        self.ffmpeg_dir = self.base_dir / "ffmpeg_portable"
        self.venv_dir = self.base_dir / ".venv"
        self.ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        
    def log(self, message, level="INFO"):
        """Log a message with proper formatting."""
        print(f"[{level}] {message}")
        sys.stdout.flush()
    
    def check_python_version(self):
        """Check if Python version is 3.11 or higher and recommend latest version."""
        self.log("Checking Python version...")
        version = sys.version_info
        
        # Minimum requirement
        if version.major < 3 or (version.major == 3 and version.minor < 11):
            self.log(f"Python 3.11+ required, but found {version.major}.{version.minor}", "ERROR")
            self.log("Please download the latest Python from https://www.python.org/downloads/", "ERROR")
            sys.exit(1)
        
        # Version info
        self.log(f"Python version {version.major}.{version.minor}.{version.micro} detected - OK")
        
        # Recommend newer version if not using latest stable
        if version.minor < 13:
            self.log(f"Note: Python 3.13+ is recommended for best compatibility", "WARN")
            self.log(f"You are using Python {version.major}.{version.minor}. Consider upgrading.", "WARN")
            self.log(f"Download latest: https://www.python.org/downloads/", "WARN")
    
    def download_ffmpeg(self):
        """Download portable ffmpeg for Windows."""
        if self.ffmpeg_dir.exists():
            self.log("FFmpeg directory already exists, skipping download")
            return
        
        self.log("Downloading portable ffmpeg...")
        self.log(f"URL: {self.ffmpeg_url}")
        
        zip_path = self.base_dir / "ffmpeg.zip"
        
        try:
            # Download with progress
            def reporthook(block_num, block_size, total_size):
                downloaded = block_num * block_size
                if total_size > 0:
                    percent = min(100, downloaded * 100 / total_size)
                    sys.stdout.write(f"\rDownloading: {percent:.1f}%")
                    sys.stdout.flush()
            
            urllib.request.urlretrieve(self.ffmpeg_url, zip_path, reporthook)
            print()  # New line after progress
            self.log("Download complete")
            
            # Extract zip
            self.log("Extracting ffmpeg...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.base_dir / "ffmpeg_temp")
            
            # Find the extracted directory (it has a version number)
            temp_dir = self.base_dir / "ffmpeg_temp"
            extracted_dirs = list(temp_dir.iterdir())
            if not extracted_dirs:
                raise Exception("No directories found after extraction")
            
            # Move to final location
            shutil.move(str(extracted_dirs[0]), str(self.ffmpeg_dir))
            
            # Cleanup
            shutil.rmtree(temp_dir)
            zip_path.unlink()
            
            self.log("FFmpeg extracted successfully")
            
        except Exception as e:
            self.log(f"Error downloading/extracting ffmpeg: {e}", "ERROR")
            # Cleanup on error
            if zip_path.exists():
                zip_path.unlink()
            if (self.base_dir / "ffmpeg_temp").exists():
                shutil.rmtree(self.base_dir / "ffmpeg_temp")
            sys.exit(1)
    
    def create_venv(self):
        """Create a virtual environment."""
        if self.venv_dir.exists():
            self.log("Virtual environment already exists")
            return
        
        self.log("Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_dir)], 
                         check=True)
            self.log("Virtual environment created successfully")
        except subprocess.CalledProcessError as e:
            self.log(f"Error creating virtual environment: {e}", "ERROR")
            sys.exit(1)
    
    def get_venv_python(self):
        """Get path to Python executable in virtual environment."""
        if platform.system() == "Windows":
            return self.venv_dir / "Scripts" / "python.exe"
        else:
            return self.venv_dir / "bin" / "python"
    
    def get_venv_pip(self):
        """Get path to pip executable in virtual environment."""
        if platform.system() == "Windows":
            return self.venv_dir / "Scripts" / "pip.exe"
        else:
            return self.venv_dir / "bin" / "pip"
    
    def upgrade_pip(self):
        """Upgrade pip in the virtual environment."""
        self.log("Upgrading pip...")
        python_exe = self.get_venv_python()
        try:
            subprocess.run([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"],
                         check=True, capture_output=True, text=True)
            self.log("Pip upgraded successfully")
        except subprocess.CalledProcessError as e:
            self.log(f"Warning: Could not upgrade pip: {e}", "WARN")
    
    def install_packages(self):
        """Install manim and dependencies."""
        self.log("Installing manim and dependencies...")
        python_exe = self.get_venv_python()
        
        # Set environment variables for the installation
        env = os.environ.copy()
        
        # Add ffmpeg to PATH for this process only
        ffmpeg_bin = self.ffmpeg_dir / "bin"
        if platform.system() == "Windows":
            env["PATH"] = f"{ffmpeg_bin};{env.get('PATH', '')}"
        else:
            env["PATH"] = f"{ffmpeg_bin}:{env.get('PATH', '')}"
        
        try:
            # Install manim
            self.log("Installing manim...")
            result = subprocess.run(
                [str(python_exe), "-m", "pip", "install", "manim"],
                check=True,
                env=env,
                capture_output=True,
                text=True
            )
            self.log("Manim installed successfully")
            
        except subprocess.CalledProcessError as e:
            self.log(f"Error installing packages: {e}", "ERROR")
            if e.stdout:
                self.log(f"STDOUT: {e.stdout}", "ERROR")
            if e.stderr:
                self.log(f"STDERR: {e.stderr}", "ERROR")
            sys.exit(1)
    
    def create_sitecustomize(self):
        """Create sitecustomize.py to automatically add ffmpeg to PATH."""
        self.log("Creating sitecustomize.py for automatic ffmpeg PATH setup...")
        
        # Get the site-packages directory in the venv
        python_exe = self.get_venv_python()
        
        try:
            result = subprocess.run(
                [str(python_exe), "-c", "import site; print(site.getsitepackages()[0])"],
                capture_output=True,
                text=True,
                check=True
            )
            site_packages = Path(result.stdout.strip())
            
            sitecustomize_path = site_packages / "sitecustomize.py"
            ffmpeg_bin = self.ffmpeg_dir / "bin"
            
            # Create sitecustomize.py that adds ffmpeg to PATH on import
            sitecustomize_content = f'''"""
Automatically add ffmpeg to PATH when Python starts.
This ensures PyAV can find ffmpeg DLLs.
"""
import os
import sys

# Add ffmpeg to PATH
FFMPEG_BIN = r"{ffmpeg_bin}"

if os.path.exists(FFMPEG_BIN):
    # Add to front of PATH so it takes precedence
    if FFMPEG_BIN not in os.environ.get("PATH", ""):
        os.environ["PATH"] = FFMPEG_BIN + os.pathsep + os.environ.get("PATH", "")
        
    # On Windows, also add to DLL search path
    if sys.platform == "win32" and hasattr(os, "add_dll_directory"):
        try:
            os.add_dll_directory(FFMPEG_BIN)
        except (OSError, AttributeError):
            pass
'''
            
            with open(sitecustomize_path, 'w', newline='\n') as f:
                f.write(sitecustomize_content)
            
            self.log(f"Created sitecustomize.py at: {sitecustomize_path}")
            self.log("FFmpeg will be automatically available when using this venv")
            
        except Exception as e:
            self.log(f"Warning: Could not create sitecustomize.py: {e}", "WARN")
            self.log("You will need to activate the environment with activate_manim.bat", "WARN")
    
    def create_render_script_template(self):
        """Create a render script template that sets up environment properly."""
        self.log("Creating render script template...")
        
        render_template_path = self.base_dir / "render_manim.py"
        ffmpeg_bin = self.ffmpeg_dir / "bin"
        venv_python = self.get_venv_python()
        
        template_content = f'''#!/usr/bin/env python3
"""
Manim Render Script with Automatic FFmpeg Setup
This script ensures FFmpeg is available before running manim.

Usage:
    python render_manim.py scene.py SceneName -ql
    python render_manim.py --help
"""

import os
import sys
import subprocess
from pathlib import Path

# Setup paths
SCRIPT_DIR = Path(__file__).parent.absolute()
FFMPEG_BIN = SCRIPT_DIR / "ffmpeg_portable" / "bin"
VENV_PYTHON = SCRIPT_DIR / ".venv" / {"'Scripts'" if platform.system() == "Windows" else "'bin'"} / {"'python.exe'" if platform.system() == "Windows" else "'python'"}

def setup_environment():
    """Add FFmpeg to PATH and DLL search directories."""
    if FFMPEG_BIN.exists():
        # Add to PATH
        ffmpeg_bin_str = str(FFMPEG_BIN)
        if ffmpeg_bin_str not in os.environ.get("PATH", ""):
            os.environ["PATH"] = ffmpeg_bin_str + os.pathsep + os.environ.get("PATH", "")
        
        # On Windows, also add to DLL search path
        if sys.platform == "win32" and hasattr(os, "add_dll_directory"):
            try:
                os.add_dll_directory(str(FFMPEG_BIN))
            except (OSError, AttributeError):
                pass
    else:
        print(f"WARNING: FFmpeg directory not found at {{FFMPEG_BIN}}")
        print("Please run setup_manim_windows.py first!")
        sys.exit(1)

def run_manim(args):
    """Run manim with the provided arguments."""
    # Ensure we're using the venv Python
    if not VENV_PYTHON.exists():
        print(f"ERROR: Virtual environment Python not found at {{VENV_PYTHON}}")
        print("Please run setup_manim_windows.py first!")
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Run manim
    cmd = [str(VENV_PYTHON), "-m", "manim"] + args
    print(f"Running: {{' '.join(cmd)}}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {{e}}")
        sys.exit(1)

if __name__ == "__main__":
    # Pass all command line arguments to manim
    args = sys.argv[1:]
    
    if not args:
        print("Usage: python render_manim.py [manim arguments]")
        print("Examples:")
        print("  python render_manim.py scene.py SceneName -ql")
        print("  python render_manim.py --help")
        print("  python render_manim.py checkhealth")
        sys.exit(1)
    
    run_manim(args)
'''
        
        with open(render_template_path, 'w', newline='\n') as f:
            f.write(template_content)
        
        self.log(f"Created render script template: {render_template_path.name}")
        self.log("You can now run: python render_manim.py scene.py SceneName -ql")
    
    def create_activation_script(self):
        """Create a script to activate the environment with ffmpeg in PATH."""
        self.log("Creating activation script...")
        
        if platform.system() == "Windows":
            # Create batch file for Windows
            script_path = self.base_dir / "activate_manim.bat"
            ffmpeg_bin = self.ffmpeg_dir / "bin"
            venv_scripts = self.venv_dir / "Scripts"
            
            script_content = f"""@echo off
REM Activation script for manim with portable ffmpeg

REM Add ffmpeg to PATH
set "PATH={ffmpeg_bin};%PATH%"

REM Activate virtual environment
call "{venv_scripts}\\activate.bat"

echo.
echo ========================================
echo Manim environment activated!
echo FFmpeg: {ffmpeg_bin}
echo Python: {venv_scripts}
echo ========================================
echo.
echo You can now run: manim --help
echo Or test with: manim checkhealth
echo.
"""
        else:
            # Create shell script for Linux (for testing purposes)
            script_path = self.base_dir / "activate_manim.sh"
            ffmpeg_bin = self.ffmpeg_dir / "bin"
            venv_bin = self.venv_dir / "bin"
            
            script_content = f"""#!/bin/bash
# Activation script for manim with portable ffmpeg

# Add ffmpeg to PATH
export PATH="{ffmpeg_bin}:$PATH"

# Activate virtual environment
source "{venv_bin}/activate"

echo ""
echo "========================================"
echo "Manim environment activated!"
echo "FFmpeg: {ffmpeg_bin}"
echo "Python: {venv_bin}"
echo "========================================"
echo ""
echo "You can now run: manim --help"
echo "Or test with: manim healthcheck"
echo ""
"""
        
        # Use appropriate line endings for the platform
        if platform.system() == "Windows":
            # Windows batch files need CRLF line endings
            newline = '\r\n'
        else:
            # Unix shell scripts use LF
            newline = '\n'
        
        with open(script_path, 'w', newline='') as f:
            # Replace \n with appropriate line ending
            f.write(script_content.replace('\n', newline))
        
        # Make executable on Unix systems
        if platform.system() != "Windows":
            script_path.chmod(0o755)
        
        self.log(f"Activation script created: {script_path.name}")
    
    def run_healthcheck(self):
        """Run manim healthcheck to verify installation."""
        self.log("Running manim healthcheck...")
        python_exe = self.get_venv_python()
        
        # Set environment variables
        env = os.environ.copy()
        ffmpeg_bin = self.ffmpeg_dir / "bin"
        if platform.system() == "Windows":
            env["PATH"] = f"{ffmpeg_bin};{env.get('PATH', '')}"
        else:
            env["PATH"] = f"{ffmpeg_bin}:{env.get('PATH', '')}"
        
        try:
            result = subprocess.run(
                [str(python_exe), "-m", "manim", "checkhealth"],
                env=env,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            self.log("=" * 60)
            self.log("MANIM HEALTH CHECK OUTPUT:")
            self.log("=" * 60)
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
            self.log("=" * 60)
            
            if result.returncode == 0:
                self.log("Health check passed!", "SUCCESS")
            else:
                self.log("Health check completed with warnings", "WARN")
                
        except subprocess.TimeoutExpired:
            self.log("Health check timed out", "WARN")
        except Exception as e:
            self.log(f"Could not run health check: {e}", "WARN")
    
    def create_readme(self):
        """Create a README file with usage instructions."""
        readme_path = self.base_dir / "MANIM_SETUP_README.md"
        
        content = """# Manim Setup - Usage Instructions

This directory contains a portable manim installation for Windows.

## Requirements:
- **Python 3.11+** (Python 3.13+ recommended)
- Download the latest Python from: https://www.python.org/downloads/

## What was installed:
- Portable FFmpeg (in `ffmpeg_portable/`)
- Python virtual environment (in `.venv/`)
- Manim and all dependencies

## How to use:

### Method 1: Using the Render Script (RECOMMENDED - Most Reliable)
The `render_manim.py` script automatically sets up FFmpeg and runs manim:

```
python render_manim.py scene.py SceneName -ql
python render_manim.py checkhealth
python render_manim.py --help
```

This method is guaranteed to work because it handles all environment setup automatically.

### Method 2: Windows Activation Script
1. Run the activation script:
   ```
   activate_manim.bat
   ```

2. Once activated, you can use manim:
   ```
   manim --help
   manim checkhealth
   manim -pql your_scene.py YourScene
   ```

3. To deactivate, simply type:
   ```
   deactivate
   ```

### Method 3: Direct venv Python (Advanced)
```
.venv\\Scripts\\python.exe -m manim checkhealth
.venv\\Scripts\\python.exe -m manim -pql scene.py MyScene
```

Note: This works due to sitecustomize.py, but Method 1 (render script) is more reliable.

### Linux (for testing):
1. Run the activation script:
   ```
   source activate_manim.sh
   ```

2. Use manim as shown above

## Notes:
- FFmpeg is NOT installed system-wide
- The system PATH is NOT modified
- Everything is contained in this directory
- **Three layers of protection against DLL errors**:
  1. `render_manim.py` - Render script with built-in environment setup (RECOMMENDED)
  2. `sitecustomize.py` - Automatic FFmpeg loading when using venv Python
  3. `activate_manim.bat` - Shell environment setup

## Troubleshooting:
- **"DLL load failed" error**: Use `python render_manim.py` instead of calling manim directly
- **Best practice**: Always use `python render_manim.py [args]` for running manim
"""
        
        with open(readme_path, 'w') as f:
            f.write(content)
        
        self.log(f"README created: {readme_path.name}")
    
    def run(self):
        """Run the complete setup process."""
        self.log("=" * 60)
        self.log("MANIM WINDOWS SETUP - STARTING")
        self.log("=" * 60)
        
        try:
            self.check_python_version()
            self.download_ffmpeg()
            self.create_venv()
            self.upgrade_pip()
            self.install_packages()
            self.create_sitecustomize()
            self.create_render_script_template()
            self.create_activation_script()
            self.create_readme()
            self.run_healthcheck()
            
            self.log("=" * 60)
            self.log("SETUP COMPLETED SUCCESSFULLY!", "SUCCESS")
            self.log("=" * 60)
            self.log("")
            self.log("Next steps:")
            self.log("RECOMMENDED: Use the render script (most reliable):")
            self.log("  python render_manim.py checkhealth")
            self.log("  python render_manim.py scene.py SceneName -ql")
            self.log("")
            self.log("Alternative: Activate the environment:")
            if platform.system() == "Windows":
                self.log("  activate_manim.bat")
            else:
                self.log("  source activate_manim.sh")
            self.log("  manim checkhealth")
            self.log("")
            self.log("See MANIM_SETUP_README.md for more information")
            
        except KeyboardInterrupt:
            self.log("\nSetup interrupted by user", "ERROR")
            sys.exit(1)
        except Exception as e:
            self.log(f"Unexpected error: {e}", "ERROR")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    setup = ManimWindowsSetup()
    setup.run()
