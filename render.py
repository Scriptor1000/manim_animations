import os
import subprocess
import re

scene_name = 'Task641036'
file_name = 'math_olympiade.py'
quality = '1440p60'

qualities = {
    '480p15': '-ql',
    '720p30': '-qm',
    '1080p60': '-qh',
    '1440p60': '-qp',
    '2160p60': '-qk'
}

# result = subprocess.run(['manim', '-ql', 'math_olympiade.py', scene_name], capture_output=True, text=True, )
# one_line = ''.join(line.strip() for line in result.stdout.splitlines())

process = subprocess.Popen(['manim', qualities[quality], file_name, scene_name],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

one_line = ''
while True:
    line = process.stdout.readline()
    if not line:
        break
    print(line, end='')
    one_line += line.replace('\n', '').strip()

pattern = r'\d+_\d+_\d+'
matches = re.findall(re.compile(pattern), one_line)

path_prefix = f'media/videos/{os.path.splitext(file_name)[0]}/{quality}/partial_movie_files/{scene_name}/'

for idx, filename in enumerate(matches, start=1):
    new_path = path_prefix + f'{scene_name}_{idx}.mp4'
    old_path = path_prefix + filename + '.mp4'
    if os.path.exists(new_path):
        os.remove(new_path)
    os.rename(old_path, new_path)
