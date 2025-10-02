import pandas as pd
import json
from mecab import MeCab


### NER 태깅 작업 툴
def tokenizing(textData, tokenizer):
    tokenizer=tokenizer
    return [tokenizer.morphs(text) for text in textData]


def ner_tagging(textDF):
    '''
    NER 태깅 작업 툴
    params: 토큰화한 테이터(데이터 프레임 형태로)
    '''
    label=[]
    for row in textDF[:]:
        tokens=[]
        ner_tags=[]
        for token in row:
            print(row)
            print(token)
            while True:
                tag= input('토큰에 맞는 태그를 입력하세요')
                if tag and len(tag)==1 and 0<=int(tag)<=8: break
                else: print('올바른 토큰을 입력하세요')
            tokens.append(token)
            ner_tags.append(tag)
        label.append({
            'tokens': tokens,
            'ner_tags': ner_tags
            })
        print(f'{len(label)}/24')
    print('끝!')
    return label


# 토큰화할 데이터 입력
data= pd.read_table('data/테스트_데이터.txt')
# 토큰나이저 입력
tokenizer=MeCab()
print(data)
tokens= tokenizing(data['text'], tokenizer)
# 태깅작업
label= ner_tagging(tokens)
PATH='./labeling_mecab/'
with open(PATH+'test.json', 'w', encoding='utf-8') as f:
    json.dump(label, f, indent=4, ensure_ascii=False)
#1: 1~50
#2: 51~100
#3: 101~150
# 4: 151~200
# 5: 201~ 230