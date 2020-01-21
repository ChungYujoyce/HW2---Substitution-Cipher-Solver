import itertools

with open('textfile/ciphertext1.txt') as f:
    cipher = f.read()
    count = 0
    for c in cipher:
        if c.isupper():
            count +=1
    flagg = cipher[1:20]
with open('three_no_spaces_freqs.txt') as ff:
    triscores = {}
    # type(ff) <class '_io.TextIOWrapper'>
    # type(ff.read()) <class 'str'>
    for item in ff:
        (word, score) = item.split()
        triscores[word] = float(score)

    
def count_frequency(ciphertext):
    
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letters = 'abcdefghijklmnopqrstuvwxyz'
    letterCount_big = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0,
     'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
    letterCount_small = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0,
     'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}
    for letter in ciphertext:
        if letter in LETTERS:
            letterCount_big[letter] += 1
        elif letter in letters:
            letterCount_small[letter] += 1

    return letterCount_big, letterCount_small

def frequency_table(fre_big, fre_small):

    new_table_big = dict()
    new_table_small = dict()
    new_fre_big = dict()
    new_fre_small = dict()

    table_big = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41,
    'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}

    table_small = {'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702, 'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153, 'k': 0.772, 'l': 4.025, 'm': 2.406,
    'n': 6.749, 'o': 7.507, 'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056, 'u': 2.758, 'v': 0.978, 'w': 2.36, 'x': 0.15, 'y': 1.974, 'z': 0.074}

    new_table_big = sorted(table_big, key=table_big.get, reverse= True)
    new_table_small = sorted(table_small, key=table_small.get, reverse= True)
    new_fre_big = sorted(fre_big, key=fre_big.get, reverse= True)
    new_fre_small = sorted(fre_small, key=fre_small.get, reverse= True)

    return new_fre_small, new_fre_big

def create_first_key(new_fre_small):
    guesskey = ""
    for c in new_fre_small:
        guesskey += c
    return guesskey
        
# !!!!!
def tri_freq_score(guesskey): # score the higher the better
    
    guess_plaintext, match = create_article(cipher, guesskey)
    totalcost = 0
    
    for i in range(len(guess_plaintext)-2):
        curstr = guess_plaintext[i:i+3]
        if triscores.get(curstr):
            totalcost += triscores[curstr]
        else:
            totalcost -= 90.0
    return totalcost

def swap(string, i, j):
    c = list(string)
    c[i], c[j] = c[j], c[i]
    return ''.join(c)

def key_modify(guesskey):
    key_score = tri_freq_score(guesskey)
    Swap = list(itertools.combinations(range(26), 2)) 
    item = 0
    while len(Swap) > 0:
        new_key = swap(guesskey, Swap[item][0], Swap[item][1]) 
        new_score = tri_freq_score(new_key)
        if new_score > key_score:
            key_score = new_score
            guesskey = new_key
            item = 0
        else:
            Swap.pop(item)
        item += 1
        if item >= len(Swap):
            item = 0
            
    for i in range(0,2):
        Swap = list(itertools.combinations(range(26), 2))             
        for item in range(0,len(Swap)):                 
            new_key = swap(guesskey, Swap[item][0], Swap[item][1])  
            new_score = tri_freq_score(new_key)                 
            if new_score > key_score: 
                key_score = new_score
                guesskey = new_key
    return guesskey, key_score
       

def create_article(article, key):
    
    original_article = ""
    match = list()
    table = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}

    for i,j in zip(table, key):
        new = (i,j)
        match.append(new)
        
    for c in article:
        if c == '{' or c == '}':
            continue
        for pair in match:
            if pair[1] == c:
                original_article = original_article + pair[0]

    return original_article, match

def main():
    letterCount_big, letterCount_small = count_frequency(cipher)
    new_fre_small, new_fre_big = frequency_table(letterCount_big, letterCount_small)
    
    guesskey = create_first_key(new_fre_small)
    key, score = key_modify(guesskey)
    # print(score) -43526.37898300028
    flag, match = create_article(flagg.lower(), key)
    print("{",flag,"}")
    # {} ->set is not subscriptable use list() -> [] to let elements iterate in order
    table = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    final = ""
    for k in table:
        for i,j in match:
            if i == k:
                final += j
    print("key=",final)            
    
    article, match = create_article(cipher, key)
    print(article)

if __name__ == "__main__":
    main()
