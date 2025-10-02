### NLP 데이터셋 전처리 및 기타 함수
from torch.utils.data import DataLoader, Dataset
from collections import Counter
from konlpy.tag import Okt
import re
from typing import Literal
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np

class TextDataset(Dataset):
    def __init__(self, feature, label):
        super().__init__()
        self.feature= feature
        self.label= label
        self.length=feature.shape[0]

    
    def __len__(self):
        return self.length

    def __getitem__(self, index):
        return self.feature[index], self.label[index]


def make_stopwords(STOP_PATH):
    '''
    txt불용어 사전을 가져오는 함수
    return: 불용어사전 집합
    '''
    with open(STOP_PATH, 'r', encoding='utf-8') as f:
        stopwords = f.read().splitlines() # 문장단위로
    return set(stopwords)

def make_vocab(data, tag, stopwords, vocab_num):
    '''
    데이터를 통해 단어사전을 만드는 함수 \n
    DF 데이터 분리했을 경우 인덱스 초기화하기!\n
    단어사전 반환\n
    params: 데이터프레임
    '''
    token_list=[]
    counter=Counter()
    for text in data:
        # 한글빼고 다지우기
        # text=re.sub('[^ㄱ-ㅎ가-힣]+',' ',text)
        # 형태소 분석 (stem-> 어근으로 통일, norm-> 정규화)
        tokens=tag.morphs(text)
        token_list.append(tokens)
        #불용어, 구두점, 특수문자 제거

    # 형태소 단어 counter에 저장
    for t in token_list:
        for token in t:
            if token in stopwords:
                t.remove
            for s in stopwords:
                if t == s:  #불용어 제거
                    t.remove(token)
        counter.update(t)
    # 빈도순으로 임의의 수만큼 추출
    
    # 단어 사전에 저장
    vocab={'<PAD>':0, '<UNK>':1}
    vocab_list=[]
    for token, cnt in counter.most_common(vocab_num):
        if token in stopwords:
            pass
        else: vocab_list.append(token)
    vocab.update({word: i+2 for i, word in enumerate(vocab_list)})
    return vocab

def vectorize(vocab, DF, tokenizer):
    '''
    단어사전을 통해 문장을 수치화하는 함수

    '''
    vector_list=[]
    vecDF=DF.copy()
    for t in DF['text']:
        token_lists=tokenizer.morphs(t)
        vector_token=[vocab[token] if token in vocab else vocab['<UNK>'] for token in token_lists]
        vector_list.append(vector_token)
    vecDF['text']=vector_list

    return vecDF

def check_length(data):
    '''
    수치화한 데이터 길이 확인하는 함수
    '''
    len_list=[]
    for t in trainVec['text']:
        len_list.append(len(t))
        print(len(t))
    print(np.mean(len_list), max(len_list))
    plt.hist(len_list)

def padding(length, textList):
    '''
    패딩함수
    '''
    pad_texts=[]
    for text in textList:
            # 선택 길이> 문장길이 일때
        if length>len(text):
                                            # 남은 텍스트 길이만큼 0으로 채우기
            text=text+[0]*(length-len(text))
        else: # 선택 길이< 문장 길이 일때
            text=text[:length]              # 선택 길이만큼 슬라이싱
        pad_texts.append(text)
    return pad_texts

class textCLF(nn.Module):
    '''
    자연어 처리를 위한 기본 모델 생성
    '''
    def __init__(self, n_vocab, hidden_dim, embedding_dim, n_layers,
                 model_type: Literal['lstm', 'rnn'], dropout=0.5, bidirectional=True):
        super().__init__()

        # 임베딩 층
        # num-> 단어사전의 크기
        self.embedding= nn.Embedding(
            num_embeddings=n_vocab,
            embedding_dim=embedding_dim,
            padding_idx=0
        )
        if model_type =='rnn':
            self.model=nn.RNN(
                input_size=embedding_dim,
                hidden_size=hidden_dim,
                num_layers=n_layers,
                bidirectional=bidirectional,
                dropout=dropout,
                batch_first=True
            )
        elif model_type =='lstm':
            self.model= nn.LSTM(
                input_size=embedding_dim,
                hidden_size=hidden_dim,
                num_layers=n_layers,
                bidirectional=bidirectional,
                dropout=dropout,
                batch_first=True
            )
        # 양방향 여부
        if bidirectional:
            self.classifier= nn.Linear(hidden_dim*2, 3)
        else:
            self.classifier= nn.Linear(hidden_dim, 3)
        self.dropout=nn.Dropout(dropout)

    #포워딩
    def forward(self, input):
        embeddings= self.embedding(input)
        output,_= self.model(embeddings)
        last_output=output[:,-1,:]
        last_output=self.dropout(last_output)
        logits=self.classifier(last_output)
        return logits



