from flask import Flask, render_template, jsonify
from urllib.request import urlopen
from random import randint
from collections import defaultdict

app = Flask(__name__)

def retrieve_random_word(word_list):
    rand_index = randint(1, sum(word_list.values()))
    for word, value in word_list.items():
        rand_index -= value
        if rand_index <= 0:
            return word

def clean_and_split_text(text):
    text = text.replace('\n', ' ').replace('"', '')
    punctuation = [',', '.', ';', ':']
    for symbol in punctuation:
        text = text.replace(symbol, f' {symbol} ')
    return [word for word in text.split(' ') if word != '']

def build_word_dict(text):
    words = clean_and_split_text(text)
    word_dict = defaultdict(dict)
    for i in range(1, len(words)):
        word_dict[words[i-1]][words[i]] = word_dict[words[i-1]].get(words[i], 0) + 1
    return word_dict

def generate_chain(length=100):
    text = str(urlopen('http://pythonscraping.com/files/inaugurationSpeech.txt').read(), 'utf-8')
    word_dict = build_word_dict(text)
    chain = ['I']
    for _ in range(length):
        new_word = retrieve_random_word(word_dict[chain[-1]])
        chain.append(new_word)
    return ' '.join(chain)

@app.route('/')
def index():
    generated_text = generate_chain()
    return render_template('index.html', generated_text=generated_text)

@app.route('/generate')
def generate_ajax():
    return jsonify({'text': generate_chain()})

if __name__ == '__main__':
    app.run(debug=True)
