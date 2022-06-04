import string
import math
import pickle
import nltk
import re
from nltk import sent_tokenize

"""
This file contains the functions to truecase a sentence.
"""


def get_score(prev_token, possible_token, next_token, word_casing_look, uniq_dist, backward_bi_dist, forward_bi_dist,
              trigram_dist) -> float:
    pseudo_count = 5.0

    # Get Unigram Score
    nominator = uniq_dist[possible_token] + pseudo_count
    denominator = 0
    for alter_token in word_casing_look[possible_token.lower()]:
        denominator += uniq_dist[alter_token] + pseudo_count

    unigram_score = nominator / denominator

    # Get Backward Score
    bigram_backward_score = 1
    if prev_token is not None:
        nominator = backward_bi_dist[prev_token + '_' + possible_token] + pseudo_count
        denominator = 0
        for alter_token in word_casing_look[possible_token.lower()]:
            denominator += backward_bi_dist[prev_token + '_' + alter_token] + pseudo_count

        bigram_backward_score = nominator / denominator

    # Get Forward Score
    bigram_forward_score = 1
    if next_token is not None:
        next_token = next_token.lower()
        nominator = forward_bi_dist[possible_token + "_" + next_token] + pseudo_count
        denominator = 0
        for alter_token in word_casing_look[possible_token.lower()]:
            denominator += forward_bi_dist[alter_token + "_" + next_token] + pseudo_count

        bigram_forward_score = nominator / denominator

    # Get Trigram Score
    trigram_score = 1
    if prev_token is not None and next_token is not None:
        next_token = next_token.lower()
        nominator = trigram_dist[prev_token + "_" + possible_token + "_" + next_token] + pseudo_count
        denominator = 0
        for alter_token in word_casing_look[possible_token.lower()]:
            denominator += trigram_dist[prev_token + "_" + alter_token + "_" + next_token] + pseudo_count

        trigram_score = nominator / denominator

    result = math.log(unigram_score) + math.log(bigram_backward_score) + math.log(bigram_forward_score) + \
             math.log(trigram_score)

    return result


def get_true_case(tokens, vocabulary_token_option, word_casing_look, uniq_dist, backward_bi_dist, forward_bi_dist,
                  trigram_dist) -> list:
    """
    Returns the true case for the passed tokens.
    @param tokens: Tokens in a single sentence
    @param outOfVocabulariyTokenOption:
        title: Returns out of vocabulary (OOV) tokens in 'title' format
        lower: Returns OOV tokens in lower case
        as-is: Returns OOV tokens as is
    """
    tokens_true_case = []
    for tokenIdx in range(len(tokens)):
        token = tokens[tokenIdx]
        if token in string.punctuation or token.isdigit():
            tokens_true_case.append(token)
        else:
            if token in word_casing_look:
                if len(word_casing_look[token]) == 1:
                    tokens_true_case.append(list(word_casing_look[token])[0])
                else:
                    prev_token = tokens_true_case[tokenIdx - 1] if tokenIdx > 0 else None
                    next_token = tokens[tokenIdx + 1] if tokenIdx < len(tokens) - 1 else None

                    bestToken = None
                    highestScore = float("-inf")

                    for possible_token in word_casing_look[token]:
                        score = get_score(prev_token, possible_token, next_token, word_casing_look, uniq_dist,
                                          backward_bi_dist,
                                          forward_bi_dist, trigram_dist)

                        if score > highestScore:
                            bestToken = possible_token
                            highestScore = score

                    tokens_true_case.append(bestToken)

                if tokenIdx == 0:
                    tokens_true_case[0] = tokens_true_case[0].title()

            else:  # Token out of vocabulary
                if vocabulary_token_option == 'title':
                    tokens_true_case.append(token.title())
                elif vocabulary_token_option == 'lower':
                    tokens_true_case.append(token.lower())
                else:
                    tokens_true_case.append(token)

    return tokens_true_case


def true_casing_by_stats(input_text) -> str:
    true_case_text = ''
    f = open('./frequency_analysis/distributions.obj', 'rb')
    uniq_dist = pickle.load(f)
    backward_bi_dist = pickle.load(f)
    forward_bi_dist = pickle.load(f)
    trigram_dist = pickle.load(f)
    word_casing_look = pickle.load(f)
    f.close()

    sentences = sent_tokenize(input_text, language='english')
    for s in sentences:
        tokens = [token.lower() for token in nltk.word_tokenize(s)]
        tokens_true_case = get_true_case(tokens, 'lower', word_casing_look, uniq_dist, backward_bi_dist,
                                         forward_bi_dist, trigram_dist)
        str_true_case = re.sub(" (?=[.,'!?:;])", "", ' '.join(tokens_true_case))
        true_case_text = true_case_text + str_true_case + ' '
    return true_case_text.strip()
