# Cryptanalysis with genetic algorithms (GA)

Natural language text cracking, a method for optimizing the search for the key of permutation ciphers using genetic algorithms(GA) is presented.

## Previously
1. Clone
```
git clone git@github.com:Blackbackofficial/cryptanalysis-with-ga.git
```

2. Install dependencies
```
pip freeze > requirements.txt
```

3. Download <code>distributions.obj</code> file [this](https://github.com/nreimers/truecaser/releases/download/v1.0/english_distributions.obj.zip) to compose N-grams and and move it to <code>frequency_analysis</code> folder

## Run

```
python3 main.py
```

## Additionally

1. The date folder will store the encrypted text and the decrypted text.
2. <code>truecasing.py</code> need it for frequency analysis, compiling bigrams and trigrams.