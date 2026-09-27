import string
import urllib.request
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

def get_text(url):
    """Завантажує текст із заданої URL-адреси."""
    try:
        with urllib.request.urlopen(url) as response:
            text = response.read().decode('utf-8')
        return text
    except Exception as e:
        print(f"Помилка завантаження тексту: {e}")
        return None

def remove_punctuation(text):
    """Видаляє пунктуацію з тексту."""
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    """Етап Map: повертає пару слово, 1."""
    return word.lower(), 1

def shuffle_function(mapped_values):
    """Етап Shuffle: групує значення за ключем словом."""
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    """Етап Reduce: підсумовує кількість входжень слова."""
    key, values = key_values
    return key, sum(values)

def map_reduce(text):
    """Виконує MapReduce з використанням багатопотоковості."""
    text = remove_punctuation(text)
    words = text.split()

    # Паралельний Map
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    shuffled_values = shuffle_function(mapped_values)

    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)



def visualize_top_words(word_counts, top_n=10):
    """
    Візуалізує топ-N слів з найвищою частотою використання.
    Будує горизонтальну стовпчасту діаграму.
    """
    if not word_counts:
        print("Немає даних для візуалізації.")
        return

    sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:top_n]
    
    words = [item[0] for item in sorted_words]
    counts = [item[1] for item in sorted_words]

    # Побудова графіка
    plt.figure(figsize=(10, 6))
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.gca().invert_yaxis()
    plt.show()

if __name__ == '__main__':
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    
    print(f"Завантаження тексту з {url}...")
    text = get_text(url)
    
    if text:
        print("Виконання аналізу MapReduce (це може зайняти кілька секунд)...")
        word_counts = map_reduce(text)
        
        print("Візуалізація результатів...")
        visualize_top_words(word_counts, top_n=10)