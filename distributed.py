import time
import psutil
import re
import os
import multiprocessing as mp
from collections import Counter
from itertools import islice

def counting_map(chunk):
    counter = Counter()
    word_pattern = re.compile(r'\b[a-z]+\b')
    for line in chunk:
        line_words = word_pattern.findall(line.lower())
        counter.update(line_words)
    return counter

def generate_chunks(file, chunk_size=1024*128):
    while True:
        chunk = list(islice(file, chunk_size))
        if not chunk:
            break
        yield chunk

def distributed_word_count(filepath_in, filepath_out):
    process = psutil.Process(os.getpid())
    psutil.cpu_percent(interval=None)
    start_time = time.time()

    counter = Counter()

    num_workers = mp.cpu_count()

    with open(filepath_in, 'r', encoding='utf-8') as f:
        chunks = generate_chunks(f)

        with mp.Pool(processes=num_workers) as pool:
            partial_results = pool.imap_unordered(counting_map, chunks)

            for partial_counter in partial_results:
                counter.update(partial_counter)

    end_time = time.time()
    cpu_usage = psutil.cpu_percent(interval=None)
    mem_usage = process.memory_info().rss / 1024 / 1024

    with open(filepath_out, 'w', encoding='utf-8') as f:
        f.write(f"Tempo Gasto: {end_time - start_time:.2f} segundos\n")
        f.write(f"Uso de CPU: {cpu_usage:.2f}%\n")
        f.write(f"Uso de Memoria: {mem_usage:.2f} MB\n")
        f.write("-" * 40 + "\n")

        for word, freq in counter.most_common():
            f.write(f'{word}: {freq}\n')

if __name__ == "__main__":
    with open('qty.txt', 'r') as f:
        size = int(f.read().strip())
    distributed_word_count(f'input_{size}.txt', f'output_distributed_{size}.txt')