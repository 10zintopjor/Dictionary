import sqlite3
from pathlib import Path


def extract_line(text, cur):
    count = 0
    prev_word = ''
    matched_word = 0
    total_word = 0
    lines = text.splitlines()
    for line in lines:
        res = get_elem(line)
        if prev_word == res[0]:
            count += 1
        else:
            count = 0
        if count < 3:
            total_word += 1
            matched_word += contains_elem(res, cur)
        prev_word = res[0]
    return (matched_word, total_word)


def contains_elem(res, cur):
    for row in cur.execute('SELECT word text,definition text FROM tben LIMIT 10000'):
        (bo, en) = row
        if bo == res[0]:
            return check_matchedstring(row, res)
    return 0


def check_matchedstring(row, res):
    (bo, en) = row
    if (en.find(res[1]) == -1):
        return 0
    else:
        print(row)
        print(res)
        print("\n")
        return 1


def get_elem(line):
    res = line.split()
    return res


if __name__ == "__main__":
    con = sqlite3.connect("MLDic.ml")
    cur = con.cursor()

    text = Path("lexi.final.txt").read_text(encoding='utf-8')
    matched_word, total_word = extract_line(text, cur)
    print(str(matched_word)+" Words matched out of "+str(total_word))
    con.close()
