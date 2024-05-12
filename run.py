import time
import logging
import subprocess



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


DATASET_SIZE = 5000 # a number divisible by 100
BATCHES = int(DATASET_SIZE/100)

start_time = time.time()
step = 1

while step <= BATCHES:
    logging.info(f' │ STARTED BATCH_STEP={step}')
    iter_start_time = time.time()   # fixing iteration start time

    subprocess.run(['blender', '--background', '--python', 'main.py'], capture_output=False, text=True)

    # logging time
    current_iter = time.time() - iter_start_time
    avg_time_per_iteration = (time.time() - start_time) / step
    remaining_time = avg_time_per_iteration * (BATCHES - step)

    logging.info(f' └─ COMPLEATED BATCH_STEP={step}, avg_time={avg_time_per_iteration:.2f}s, current_batch={current_iter:.2f}s, spent_time={(avg_time_per_iteration*step/60):.2f}min, remain ~ {remaining_time/60:.2f}min')

    step += 1