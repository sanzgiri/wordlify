import re
import random
import streamlit as st
import pandas as pd

df = pd.DataFrame()


def get_words(sz):
    with open('/Users/sanzgiri/Downloads/words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    words = []
    for w in valid_words:
        if len(w) == sz:
            words.append(w)

    return words


def evaluate_guess_char(answer, guess, pos):
    if answer[pos]==guess[pos]:
        return "Y"
    if guess[pos] in answer:
        locs = [i for i in range(6) if answer[i]==guess[pos]]
        if any(guess[loc]!=answer[loc] for loc in locs):
            return "M"
    return "N"


def wordlify_guess(answer, guess, sz):

    f_guess = "".join(evaluate_guess_char(answer, guess, i) for i in range(sz))
    e_guess = "| ".join(evaluate_guess_char(answer, guess, i) for i in range(sz))
    w_guess = (e_guess.replace("Y", "🟩").replace("M", "🟨").replace("N", "⬜"))
    return w_guess, f_guess


def increment_counter():
    st.session_state.count += 1
    


if __name__ == '__main__':

    sz = 6
    n_tries = 6
    if 'count' not in st.session_state:
        st.session_state.count = 0
    if 'guess' not in st.session_state:
        st.session_state.guess = ''
    if 'resp' not in st.session_state:
        st.session_state.resp = ''
    
    st.write(f"Running attempt {st.session_state.count}")
    st.dataframe(df)

    words = get_words(sz)
    random.seed(10)
    my_word = random.choice(words)
    my_word = "equity"

    #for i in range(st.session_state.count):
    #    st.write(st.session_state.guess, st.session_state.resp)

    score = "NNNNNN"
    guess = st.text_input(label="guess", value="", max_chars=6)
 
    if guess:
        resp, score = wordlify_guess(my_word, guess, sz)


    if st.button('Next attempt'):
        st.session_state.count += 1
        st.session_state.guess = guess
        st.session_state.resp = resp
        st.experimental_rerun()
        df = df.append({guess: 'guess',
                        resp: 'resp'}, ignore_index=True)

    if score == "Y"*sz:
        st.write(f"You win in {st.session_state.count} tries!")
        st.stop()
    
    if st.session_state.count == sz:
        st.write(f"Sorry! You are out of tries!")
        st.stop()
        

    