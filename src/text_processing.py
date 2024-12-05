import re
import nltk
from nltk.data import find
from nltk.corpus import words
from nltk.tokenize import word_tokenize
from multiprocessing import Pool
from spellchecker import SpellChecker
from Levenshtein import distance as lev


spell = SpellChecker()

try:
    find('corpora/words.zip')
except LookupError:
    nltk.download('words')

try:
    find('tokenizers/punkt_tab.zip')
except LookupError:
    nltk.download('punkt_tab')

# create a set of english words from the downloaded corpus
english_words = set(words.words())


def clean_text(text: str) -> str:
    """Perform basic cleaning steps on text.
    
    Args:
        text (str): Text to process.
    
    Returns:
        str: Cleaned text.
    """
    # convert to lowercase
    text_lowercase = text.lower().strip()
    # filter punctuation
    text_filtered = re.sub(r'[^\w\s]|(\d+)', ' ', text_lowercase)

    return text_filtered


def correct_batch(batch: list, max_distance: int = 1):
    """
    Correct spelling for a batch of words.

    Args:
        batch (list): A batch of words to process.
        max_distance (int): Threshold for correction.

    Returns:
        list: Corrected words for the batch.
    """
    corrected_batch = []
    for word in batch:
        word = word.strip()
        if word in english_words:
            corrected_batch.append(word)
        else:
            # try:
            correction = spell.correction(word)
            if correction in english_words and lev(word, correction) <= max_distance:
                corrected_batch.append(correction)
            else:
                corrected_batch.append(word)
            # except Exception:
            #     corrected_batch.append(word)
    return corrected_batch


def process_texts_in_batches(texts: list, max_distance: int = 1, num_workers: int = 4):
    """
    Process multiple rows of text in parallel.

    Args:
        texts (list): List of text rows to process.
        max_distance (int): Threshold for word correction.
        num_workers (int): Number of parallel workers.

    Returns:
        list: List of processed rows with corrected words.
    """
    # ensure all rows are strings and handle edge cases
    cleaned_texts = [str(text) if text is not None else "" for text in texts]

    # convert to lowercase and remove punctuation
    filtered_texts = [clean_text(text) if text is not None else "" for text in cleaned_texts]

    # tokenize rows into lists of words
    tokenized_rows = [word_tokenize(row) if row.strip() else [] for row in filtered_texts]

    # flatten tokenized rows into batches of words
    words = [word for row in tokenized_rows for word in row]

    # split words into smaller batches for processing
    batch_size = max(1, len(words) // num_workers)
    batches = [words[i:i + batch_size] for i in range(0, len(words), batch_size)]

    # process batches in parallel
    corrected_batches = []
    if batches:
        with Pool(num_workers) as pool:
            corrected_batches = pool.map(correct_batch, batches)

    # combine corrected batches and reassemble rows
    corrected_words = [word for batch in corrected_batches for word in batch]
    corrected_rows = []
    idx = 0
    for row in tokenized_rows:
        corrected_rows.append(' '.join(corrected_words[idx:idx + len(row)]))
        idx += len(row)

    # return corrected_rows
    return corrected_rows