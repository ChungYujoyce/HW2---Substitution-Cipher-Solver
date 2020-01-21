import itertools
import random
import base64

with open('textfile/bonus2.txt') as f:
    cipher = f.read()

with open('three_no_spaces_freqs.txt') as ff:
    triscores = {}
    for item in ff:
        (word, score) = item.split()
        triscores[word] = float(score)
# !!!!!
# -----------------------difference--------------------------------------

def create_first_key():
    key = list(range(26))
    random.shuffle(key)
    return key

def swap(string, i, j):
    c = list(string)
    c[i], c[j] = c[j], c[i]
    return c

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
       

def create_article(article, key): # ord -> num
    
    original_article = ""
    
    for x in article:
        if (ord(x) >= 65) & (ord(x) <= 90):
            original_article += chr(65 + key[ord(x)-65])
        elif (ord(x) >= 97) & (ord(x) <= 122):
            original_article += chr(97 + key[ord(x)-97])
        else:
            original_article += x
    
    return original_article

def isBase64(ciphertext):
    try:
        temp_text = ciphertext.encode() 
        return base64.b64encode(base64.b64decode(temp_text)) == ciphertext.encode() 
    except Exception:
        return False  
    
# decrypt then change to base256
def tri_freq_score(guesskey): # score the higher the better
    
    totalcost = 0
    plaintext = create_article(cipher, guesskey)
    
    for i in range(int(len(plaintext)/4)):
        if isBase64(plaintext[i*4:i*4+4]): 
            try: 
                curstr = plaintext[i*4:i*4+4].encode()
                curstr = base64.b64decode(curstr) #decode base64 to base256 
                curstr = curstr.decode()
                totalcost += triscores[curstr]  
            except:
                totalcost -= 50.0 
        else:
            totalcost -= 50.0 
    
    return totalcost

def main():
    
    guesskey = create_first_key()
    key, score = key_modify(guesskey)
    print(score)
    # {} ->set is not subscriptable use list() -> [] to let elements iterate in order

    ch = [0]*26
    for i in key:
        ch[key[i]] = chr(i+97).upper()
    print("key=", "".join(ch))
    
    article = create_article(cipher, key)
    print(base64.b64decode(article))
    #print(article)

if __name__ == "__main__":
    main()