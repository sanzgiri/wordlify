import streamlit as st
import random
import json
import os
import time


def get_word(length: int) -> str:

    with open(os.path.join('assets', 'words_6c.txt')) as word_file:
        valid_words = list(set(word_file.read().split()))
    
    #random.seed(42)
    word = random.choice(valid_words)

    return word
    

def init(length: int = 6, heart: int = 6, post_init=False):
    if not post_init:
        st.session_state.input = 0
        st.session_state.win = 0
        st.session_state.length = length
        st.session_state.heart = heart
    st.session_state.word = get_word(length)
    st.session_state.lives = heart
    st.session_state.guessed = []
    st.session_state.wordle = []


def restart():
    init(st.session_state.length,
         st.session_state.heart,
         post_init=True)
    st.session_state.input += 1


def contains_non_alpha(guess):
    k = False
    for g in guess:
        if not g.isalpha():
            k = True
            return k
    return k


def evaluate_wordbox_char(answer, guess, pos):
    if answer[pos]==guess[pos]:
        return answer[pos]
    else:
        return "-"
    

def box_guess(answer, guess, length):
    b_guess = " | ".join(evaluate_wordbox_char(answer, guess, i) for i in range(length))
    return b_guess


def evaluate_guess_char(answer, guess, pos):
    if answer[pos]==guess[pos]:
        return "Y"
    if guess[pos] in answer:
        locs = [i for i in range(st.session_state.length) if answer[i]==guess[pos]]
        if any(guess[loc]!=answer[loc] for loc in locs):
            return "M"
    return "N"


def wordlify_guess(answer, guess, length):

    f_guess = "".join(evaluate_guess_char(answer, guess, i) for i in range(length))
    e_guess = " | ".join(evaluate_guess_char(answer, guess, i) for i in range(length))
    w_guess = (e_guess.replace("Y", " 🟩 ").replace("M", " 🟨 ").replace("N", "⬜"))
    return w_guess, f_guess


def main():

    st.write(
        '''
        # 🔠 Wordlify
        '''
    )

    if 'word' not in st.session_state:
        init()

    reset, win, lives = st.columns([.1, .1, .1])
    reset.button('New Wordle', on_click=restart)

    placeholder, debug = st.empty(), st.empty()
    print(f"Word to guess is {st.session_state.word}")
    guess = placeholder.text_input('Guess the wordle', key=st.session_state.input, max_chars=st.session_state.length).lower()

    if not guess or contains_non_alpha(guess) or len(guess) != 6:
        # don't show warning at start of game
        if st.session_state.lives < st.session_state.heart:
            debug.warning('Please input valid word')
    elif guess in st.session_state.guessed:
        debug.warning(f"You already guessed **{guess}**")
    elif guess != st.session_state.word:
        #debug.warning(f"Incorrect guess **{guess}**")
        resp, score = wordlify_guess(st.session_state.word, guess, st.session_state.length)
        st.session_state.lives -= 1
        st.session_state.guessed.append(guess)
        st.session_state.wordle.append(resp)

    if st.session_state.lives == 0:
        debug.error(f"**You lost**, the word was **{st.session_state.word}** 😓")
        placeholder.empty()
    elif guess == st.session_state.word:
        debug.success(f"**You win**, the word was {st.session_state.word} 🎈")
        st.session_state.win += 1
        placeholder.empty()


    lives.button(f'{("❤️" * st.session_state.lives) if st.session_state.lives else "💀 Lost"}')
    win.button(f'🏆 {st.session_state.win}')

    left, center, right = st.columns([.25,.55, 1.2])
    with left:
        key = f"guess_{st.session_state.lives}"
        for g in st.session_state.guessed:
            st.button(g, key = key)
    with center:
        for w in st.session_state.wordle:
            key = f"wordle_{st.session_state.lives}_{time.time()}"
            st.button(w, key = key)
    with right:
        for b in st.session_state.guessed:
            key = f"box_{st.session_state.lives}_{time.time()}"
            word = box_guess(b, st.session_state.word, st.session_state.length)
            st.button(word, key = key)


if __name__ == '__main__':
    main()