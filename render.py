import os
import re
import subprocess
from pathlib import Path

qualities = {
    '480p15': '-ql',
    '720p30': '-qm',
    '1080p60': '-qh',
    '1440p60': '-qp',
    '2160p60': '-qk'
}

def run_and_rename(filename: str, scene_name: str, quality: str) -> list[str]:
    home_dir = Path(os.path.dirname(os.path.abspath(__file__)))

    cmd = [home_dir / '.venv' / 'Scripts' / 'manim', qualities[quality], filename, scene_name]
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    output = ''.join(map(lambda x: x.strip(), result.stdout.decode().splitlines()))

    pattern = r'\d+_\d+_\d+'
    matches = re.findall(re.compile(pattern), output)

    path_prefix = f'media/videos/{os.path.splitext(filename)[0]}/{quality}/partial_movie_files/{scene_name}/'
    new_filenames = []

    for idx, filename in enumerate(matches, start=1):
        new_path = path_prefix + f'{scene_name}_{idx}.mp4'
        old_path = path_prefix + filename + '.mp4'
        if os.path.exists(new_path):
            os.remove(new_path)
        os.rename(old_path, new_path)
        new_filenames.append(new_path)

    return new_filenames

def just_run(filename: str, scene_name: str) -> None:
    home_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    quality = '720p30'
    cmd = [home_dir / '.venv' / 'Scripts' / 'manim', qualities[quality], filename, scene_name]
    subprocess.run(cmd)

if __name__ == '__main__':
    scene_name = 'Task641036'
    file_name = 'math_olympiade.py'
    just_run(file_name, scene_name)
