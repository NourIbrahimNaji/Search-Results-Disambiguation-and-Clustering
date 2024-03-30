import tkinter as tk
from tkinter import scrolledtext
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from pywsd.lesk import simple_lesk
from sklearn.metrics import precision_score, recall_score

# Initialize the WordNet Lemmatizer
lemmatizer = WordNetLemmatizer()

tp = 0
fp = 0
fn = 0
def search_senses():
    global tp, fp, fn

    query = query_entry.get().strip()
    word = word_entry.get().strip()
    words = word_tokenize(query)

    result_text.delete("1.0", tk.END)  # Clear previous results

    if word in words:
        lemmas = [lemmatizer.lemmatize(w) for w in word_tokenize(query)]
        if word in lemmas:
            synset = simple_lesk(query, word)
            if synset:
                result_text.insert(tk.END, f"Ambiguous word found: '{word}'\n")
                result_text.insert(tk.END, f"\nPossible senses for '{word}':\n")
                result_text.tag_config("intended", foreground="red")
                result_text.insert(tk.END, f"\nIntended meaning of '{word}' in the given query:\n", "intended")
                result_text.insert(tk.END, f"{synset.name()}: {synset.definition()}\n", "intended")

                # Update the true positives count
                tp += 1
            else:
                result_text.insert(tk.END, f"No sense found for '{word}' in the query\n")

                # Update the false negatives count
                fn += 1
        else:
            result_text.insert(tk.END, f"'{word}' is not an ambiguous word in the query\n")

            # Update the false positives count
            fp += 1

    else:
        result_text.insert(tk.END, f"'{word}' is not present in the query\n")

        # Update the false negatives count
        fn += 1

    print("-----------TP--------------" , tp)
    print("-----------FN--------------" , fn)
    print("-----------FP--------------" , fp)

    # Calculate precision and recall
    if tp + fp == 0:
        precision = 0
    else:
        precision = tp / (tp + fp)

    if tp + fn == 0:
        recall = 0
    else:
        recall = tp / (tp + fn)

    result_text.insert(tk.END, f"\nPrecision: {precision}\n")
    result_text.insert(tk.END, f"Recall: {recall}\n")


# Create the GUI window
window = tk.Tk()
window.title("Word Sense Search")

# Set the background color of the window
window.configure(bg="#f8f8f8")

# Create a frame for the search bar
search_frame = tk.Frame(window, bg="#f8f8f8")
search_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=(50, 20))

# Create a label and entry for the query input
query_label = tk.Label(search_frame, text="Query:", font=("Arial", 14), bg="#f8f8f8")
query_label.pack(side=tk.LEFT, padx=(0, 10))

query_entry = tk.Entry(search_frame, font=("Arial", 14), bd=0, relief=tk.FLAT)
query_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
query_entry.focus_set()

# Create a label and entry for the word input
word_label = tk.Label(search_frame, text="Word:", font=("Arial", 14), bg="#f8f8f8")
word_label.pack(side=tk.LEFT, padx=(10, 0))

word_entry = tk.Entry(search_frame, font=("Arial", 14), bd=0, relief=tk.FLAT)
word_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

# Create a button to trigger the search
search_button = tk.Button(search_frame, text="Search", font=("Arial", 12), padx=10, bg="#4285f4", fg="white", bd=0,
                          activebackground="#3b7dd8", activeforeground="white", command=search_senses)
search_button.pack(side=tk.LEFT)

# Create a frame for the search results
results_frame = tk.Frame(window, bg="#f8f8f8")
results_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=(20, 50))

# Create a scrolled text area to display the search results
result_text = scrolledtext.ScrolledText(results_frame, font=("Arial", 12), bd=0, relief=tk.FLAT, wrap=tk.WORD)
result_text.pack(fill=tk.BOTH, expand=True)

# Set the background color of the window
window.configure(bg="#f8f8f8")

# Start the GUI event loop
window.mainloop()