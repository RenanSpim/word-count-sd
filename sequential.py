import time
import re
from collections import Counter

def sequential_word_count(filepath):
    print("Iniciando contagem sequencial...")
    start_time = time.time()
    word_counts = Counter()
    
    try:
        # Lê o arquivo linha por linha (evita carregar um arquivo de 10GB inteiro na RAM)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # Extrai apenas palavras, convertendo para minúsculo
                words = re.findall(r'\b\w+\b', line.lower())
                word_counts.update(words)
                
    except FileNotFoundError:
        print(f"Arquivo {filepath} não encontrado.")
        return None

    end_time = time.time()
    print(f"Tempo de execução (Sequencial): {end_time - start_time:.4f} segundos")
    return word_counts

if __name__ == '__main__':
    # Exemplo de uso
    arquivo = 'dataset_gigante.txt' # Substitua pelo seu arquivo
    # counts = sequential_word_count(arquivo)
    # print(counts.most_common(10)) # Mostra as 10 palavras mais comuns