import logging
import subprocess



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


for i in range(0, 30):
    logging.info(f'STEP={i+1}')
    subprocess.run(['blender', '--background', '--python', 'main.py'], capture_output=False, text=True)
