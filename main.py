import pandas as pd
import os

# Set file path as working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def get_words():
    df = pd.read_csv('data/scrabble.csv', header=None, encoding='ISO-8859-1')
    words = df.iloc[:, 0].dropna().astype(str).tolist()
    return words


def string_to_squares(colors):
    colors = colors.upper()
    return {key: value for key, value in enumerate(colors)}


def create_info(submission, colors):
    info = {
        "submission": submission.upper(),
        "squares": string_to_squares(colors)
    }
    return info


def censor(word, indexes):
    censored_word = list(word)
    for index in indexes:
        censored_word[index] = "*"
    return "".join(censored_word)


def is_valid(word, info):
    if len(word) != len(info['submission']):
        return False
    
    squares = info['squares']
    submission = info['submission']
    
    for index, color in squares.items():
        letter = submission[index]
        
        if color == 'R' and letter != word[index]:
            return False
        
        if color == 'Y':
            if letter == word[index]:
                return False
            
            red_indexes = [k for k, v in squares.items() if v == 'R']
            if letter not in censor(word, red_indexes):
                return False
        
        if color == 'B':
            red_yellow_indexes = [k for k, v in squares.items() if v in ['R', 'Y']]
            red_yellow_letters = ''.join([submission[i] for i in red_yellow_indexes])
            
            if word.count(letter) > red_yellow_letters.count(letter):
                return False
    
    return True


def solve(sample):
    pool = get_words()
    for word, colors in sample:
        info = create_info(word, colors)
        pool = [x for x in pool if is_valid(x, info)]
    return pool




sample = [('R-----', 'R'),
          ('REGION', 'RYBBBB'),
          ('RAFLER', 'RRBBYR')]

res = solve(sample)
print(res)


sample = [('B-----', 'R'),
          ('BALLON', 'RBBBBB'),
          ('BRUITS', 'RYBBBB'),
          ('BERGER', 'RRRBRR')]

res = solve(sample)
print(res)