import torch.nn.functional as F
import torch.nn as nn
from torchmetrics.functional import f1_score
from typing import Literal


class Custom_model(nn.Module):
    '''
    커스텀 모델을 만드는 함수
    model_type= 'reg'|'binary'|'mclf'
    은닉층 수= 리스트 수-1
    '''
    def __init__(self, in_in, out_out, af, model_type: Literal['bin', 'multiclass', 'reg'], hidden: list) -> None:
        super().__init__()
        self.af=af
        self.model_type=model_type


        self.in_layer= nn.Linear(in_in, hidden[0])
        self.h_layers=nn.ModuleList()
        for h in range(len(hidden)-1):
            self.h_layers.append(nn.Linear(hidden[h], hidden[h+1]))
        self.out_layer= nn.Linear(hidden[-1], out_out)
    
    def forward(self, input_data):
        af=self.af
        
        y= self.in_layer(input_data)
        y= af(y)

        for layer in self.h_layers:
            y=layer(y)
            y=af(y)
        
            y=self.out_layer(y)
        if self.model_type=='bin':
            y=F.sigmoid(y)
        elif self.model_type=='muticlass':
            pass
        elif self.model_type=='reg':
            pass
        
        
        return y