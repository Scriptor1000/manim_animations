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
        
        with open(script_path, 'w', newline='\n') as f:
            f.write(script_content)
        
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

### Windows:
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
- You must activate the environment before using manim

## Troubleshooting:
- If manim cannot find ffmpeg, make sure you activated the environment with the activation script
- If you get permission errors, try running as administrator (Windows) or with sudo (Linux)
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
            self.create_activation_script()
            self.create_readme()
            self.run_healthcheck()
            
            self.log("=" * 60)
            self.log("SETUP COMPLETED SUCCESSFULLY!", "SUCCESS")
            self.log("=" * 60)
            self.log("")
            self.log("Next steps:")
            if platform.system() == "Windows":
                self.log("1. Run: activate_manim.bat")
            else:
                self.log("1. Run: source activate_manim.sh")
            self.log("2. Test: manim checkhealth")
            self.log("3. Start creating animations!")
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
