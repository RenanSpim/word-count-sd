import time
import re
import multiprocessing as mp
from collections import Counter

def mapper(chunk):
    """
    Fase MAP: Recebe um pedaço de texto, limpa e retorna a contagem de palavras dele.
    Isso ocorre em paralelo em vários núcleos/nós.
    """
    words = re.findall(r'\b\w+\b', chunk.lower())
    return Counter(words)

def chunk_reader(filepath, chunk_size=1024*1024*5):
    """
    Gerador que lê o arquivo em pedaços (ex: 5MB por pedaço)
    para não estourar a memória RAM.
    """
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

def distributed_word_count(filepath, num_workers=None):
    print(f"Iniciando contagem distribuída (MapReduce)...")
    start_time = time.time()
    
    # Se num_workers não for definido, usa o número de núcleos da máquina
    if num_workers is None:
        num_workers = mp.cpu_count()
        
    print(f"Utilizando {num_workers} processos trabalhadores.")
    
    # Cria o Pool de processos (nós)
    pool = mp.Pool(processes=num_workers)
    
    # Lê os pedaços do arquivo
    chunks = chunk_reader(filepath)
    
    # Fase MAP: Distribui os chunks para os workers executarem a função `mapper`
    # imap_unordered é ótimo porque retorna os resultados assim que cada nó termina
    mapped_results = pool.imap_unordered(mapper, chunks)
    
    # Fase REDUCE: Combina (soma) os dicionários parciais gerados pelos nós
    final_counts = Counter()
    for local_count in mapped_results:
        final_counts.update(local_count)
        
    pool.close()
    pool.join()
    
    end_time = time.time()
    print(f"Tempo de execução (MapReduce): {end_time - start_time:.4f} segundos")
    return final_counts

if __name__ == '__main__':
    # Exemplo de uso
    arquivo = 'dataset_gigante.txt' # Substitua pelo seu arquivo
    # counts_dist = distributed_word_count(arquivo)
    # print(counts_dist.most_common(10))