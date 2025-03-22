
def format_text(text, words_per_line=15):
    words = text.split()  # Split text into words
    lines = [' '.join(words[i:i + words_per_line]) for i in range(0, len(words), words_per_line)]
    return '\n'.join(lines)  # Join lines with newline character
