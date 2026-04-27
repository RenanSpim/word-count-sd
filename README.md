# Word Count: Análise de Performance (Sequencial vs. MapReduce)

Este projeto implementa uma ferramenta de análise de frequência de palavras (Word Count) para grandes volumes de dados (Big Data), comparando uma abordagem sequencial tradicional com uma arquitetura distribuída baseada no modelo **MapReduce**.

O objetivo é avaliar o impacto do I/O de disco, uso de memória RAM e overhead de comunicação em ambientes de cloud computing (AWS/GCP).

## 🚀 Estrutura do Problema

### 1. Abordagem Sequencial
Lê o ficheiro linha por linha, processando o texto num único núcleo de CPU. 
- **Prós:** Baixo consumo de memória inicial.
- **Contras:** Lento para datasets de 5GB+; não escala com o hardware.

### 2. Abordagem Distribuída (MapReduce)
O dataset é fragmentado em *chunks*. 
- **Map:** Cada processo (worker) conta as palavras do seu pedaço de forma independente.
- **Reduce:** Um nó central agrega os dicionários parciais para gerar a contagem final.
- **Foco:** Evidenciar o ganho de velocidade vs. o custo de sincronização e troca de dados.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Bibliotecas:** `multiprocessing` (simulação de nós distribuídos), `collections.Counter`, `re`.
* **Ambiente de Teste Recomendado:** Instâncias Linux (t2.micro/e2-micro) para análise de restrição de recursos.

## 📂 Como Executar

1.  **Preparação do Dataset:**
    Coloque o seu ficheiro de texto (ex: `dataset.txt`) na raiz do projeto. Pode utilizar dumps da Wikipédia ou livros do Projeto Gutenberg.

2.  **Execução:**
    ```bash
    # Para medir o tempo e consumo de recursos no Linux
    /usr/bin/time -v python3 distributed_word_count.py
    ```

3.  **Monitorização em Tempo Real:**
    Recomenda-se o uso do `htop` noutro terminal para observar o escalonamento dos processos nos núcleos da CPU.

## 📊 Métricas de Análise

Para o relatório técnico, são considerados os seguintes pontos:
* **Tempo de Execução:** Comparação entre `T_sequencial` e `T_mapreduce`.
* **Throughput de Rede/Disco:** Impacto da leitura de grandes blocos.
* **CPU Throttling:** Comportamento da aplicação quando os créditos de CPU da instância cloud terminam.