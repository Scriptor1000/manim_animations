import os
import re

from render_manim import run_manim

scene_name = 'Task641036'
file_name = 'math_olympiade.py'
quality = '720p30'

qualities = {
    '480p15': '-ql',
    '720p30': '-qm',
    '1080p60': '-qh',
    '1440p60': '-qp',
    '2160p60': '-qk'
}

def run_and_rename(args):
    result = run_manim(args)
    output = ''.join(map(lambda x: x.strip(), result.stdout.decode().splitlines()))

    pattern = r'\d+_\d+_\d+'
    matches = re.findall(re.compile(pattern), output)

    path_prefix = f'media/videos/{os.path.splitext(file_name)[0]}/{quality}/partial_movie_files/{scene_name}/'

    for idx, filename in enumerate(matches, start=1):
        new_path = path_prefix + f'{scene_name}_{idx}.mp4'
        old_path = path_prefix + filename + '.mp4'
        if os.path.exists(new_path):
            os.remove(new_path)
        os.rename(old_path, new_path)

if __name__ == '__main__':
    run_and_rename([qualities[quality], file_name, scene_name])