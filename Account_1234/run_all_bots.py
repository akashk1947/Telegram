import subprocess
import os

workspace_root = os.path.dirname(os.path.abspath(__file__))
bot_dirs = [f'bot{i}' for i in range(1, 11)]
processes = []

for bot_dir in bot_dirs:
    start_py = os.path.join(workspace_root, bot_dir, 'start.py')
    env = os.environ.copy()
    env['PYTHONPATH'] = workspace_root  # Add workspace root to PYTHONPATH
    proc = subprocess.Popen(
        ['python', start_py],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=workspace_root,
        env=env
    )
    processes.append((bot_dir, proc))

for bot_dir, proc in processes:
    stdout, stderr = proc.communicate()
    print(f'\n--- Output for {bot_dir} ---')
    print(stdout)
    if stderr:
        print(f'--- Errors for {bot_dir} ---')
        print(stderr)