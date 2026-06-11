from datasets import load_dataset

def extract_data(filename_out, limit):
    dataset = load_dataset('wikimedia/wikipedia', '20231101.en', split='train', streaming=True)
    
    curr_limit = 0
    
    with open(filename_out, 'w', encoding='utf-8') as f:
        for example in dataset.take(limit):
            text = example['text'].replace('\n', ' ')
            f.write(text + '\n')
            curr_limit += 1

            if curr_limit >= limit:
                break

if __name__ == "__main__":
    with open('qty.txt', 'r') as f:
        size = int(f.read().strip())
    extract_data(f'input_{size}.txt', limit=size)