from get_model import Custom_model
from torchmetrics.classification import F1Score, MulticlassF1Score
import torch.nn as nn
import torch.nn.functional as F
from torchmetrics.regression import R2Score, MeanSquaredError
import torch
import matplotlib.pyplot as plt
from typing import Literal
import pandas as pd
import torch.optim.lr_scheduler as lr_scheduler


def model_training(model, trainDL, testDL, optimizer, device, epoch: int, LIMIT: int, break_param: Literal['score', 'loss'],
                   type: Literal['reg', 'binary', 'muticlass'],optim_type: Literal['score', 'loss'], SAVE_PATH, SAVE_FILE,
                   save_type: Literal['all', 'param', 'None'], numcls: int):
    '''
    학습진행+ 모니터링+ 최적의 결과 저장\n
    type= 'reg'|'binary'|'mclf'  \n
    return: LOSS_HISTORY, SCORE_HISTORY
    '''
    #스케쥴러 옵션 설정
    if optim_type== 'score':
        scheduler= lr_scheduler.ReduceLROnPlateau(optimizer, patience=LIMIT, mode='max')
    else: scheduler= lr_scheduler.ReduceLROnPlateau(optimizer, patience=LIMIT, mode='min')
    EPOCH=epoch
    # 손실, 평가값 저장
    LOSS_HISTORY, SCORE_HISTORY= [[],[]], [[],[]]
    for ep in range(EPOCH):
        print(f'{ep+1}/{EPOCH}')
        model.train()
        loss_total, score_total= 0,0
        loss_val_total, score_val_total=0,0

        for train_feature, train_target in trainDL:
            # 학습
            train_feature.to(device); train_target.to(device)
            pre_y=model(train_feature)

            # 손실
            if type=='reg':
                Lossfunc=MeanSquaredError().to(device)
                Scorefunc=R2Score().to(device)
            elif type=='binary':
                Lossfunc= nn.BCELoss().to(device)
                Scorefunc=F1Score(task='binary', num_classes=numcls).to(device)
            elif type=='muticlass':
                Lossfunc=nn.CrossEntropyLoss().to(device)
                Scorefunc=F1Score(task='multiclass', num_classes=numcls).to(device)

            loss= Lossfunc(pre_y, train_target)
            loss_total+=loss.item()

            # 평가
            score= Scorefunc(pre_y, train_target)
            score_total+=score.item()
            # 최적화
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # 검증

        model.eval()
        with torch.no_grad():
            for val_feature, val_target in testDL:
                val_feature.to(device)
                val_target.to(device)
                # 학습
                pre_val= model(val_feature)

                # 손실
                loss= Lossfunc(pre_val, val_target.reshape(-1).long() if type=='muticlass' else val_target if type=='reg' else val_target)
                loss_val_total+=loss.item()

                # 평가
                score= Scorefunc(pre_val, val_target.reshape(-1) if type=='muticlass' else val_target)
                score_val_total+=score.item()

        
        # 저장
        LOSS_HISTORY[0].append(loss_total/len(trainDL))
        SCORE_HISTORY[0].append(score_total/len(trainDL))
        print(f'Train\n Loss: {loss_total/len(trainDL)}\n Score: {score_total/len(trainDL)}')

        LOSS_HISTORY[1].append(loss_val_total/len(testDL))
        SCORE_HISTORY[1].append(score_val_total/len(testDL))
        print(f'Val\n Loss: {loss_val_total/len(testDL)}\n Score: {score_val_total/len(testDL)}')

        # 성능이 좋은 학습 가중치 저장
        if save_type:
            if save_type=='all':
                save_type= model
            elif save_type=='param':
                save_type=model.state_dict()
            if len(SCORE_HISTORY[1]) == 1: 
            #첫번째는 무조건 저장
                torch.save(save_type, SAVE_PATH+SAVE_FILE)  
                
            else:
                if SCORE_HISTORY[1][-1]> max(SCORE_HISTORY[1][:-1]): # 자신을 제외한 최대점수값과 비교
                    torch.save(save_type, SAVE_PATH+SAVE_FILE) 
                     
        else: pass

        
        # 학습 진행 모니터링 (검증 데이터 개선이 되지 않았을때 누적 ->  평가, 손실 중 지표 하나 선택)
        # 최적화 스케쥴러 인스턴스 업데이트
        scheduler.step(score_val_total/len(testDL))
        # 손실 감소 (또는 성능 개선)이 안되는 경우 조기종료
        if scheduler.num_bad_epochs== scheduler.patience:
            print(f'{scheduler.patience} EPOCH 성능 개선이 없어서 조기종료함')
            break

    return LOSS_HISTORY, SCORE_HISTORY, ep
    

def draw_result(EPOCH:int, LOSS_HISTORY, SCORE_HISTORY):
    '''
    결과 시각화
    '''

    fig, (ax1, ax2)= plt.subplots(1,2, figsize=(15,6))
    ax1.plot(range(1,EPOCH+1), LOSS_HISTORY[0][:EPOCH], label='Train')
    ax1.plot(range(1,EPOCH+1), LOSS_HISTORY[1][:EPOCH], label='Val')
    ax1.set_title('Train & Val Loss')
    ax2.plot(range(1, EPOCH+1), SCORE_HISTORY[0][:EPOCH], label='Train')
    ax2.plot(range(1, EPOCH+1), SCORE_HISTORY[1][:EPOCH], label='Val')
    ax2.set_title('Train & Val Score')
    plt.legend()
    plt.show()

def predict_mcf2(model, data, result):
    dataTS=data.reshape(1,-1) 
    pre_val=model(dataTS)
    pre_val=F.softmax(pre_val, dim=1)
    num=pre_val.argmax(dim=1)
    print(pre_val, pre_val.argmax(dim=1))
    print(f'{result[num]}: {max(pre_val[0].detach()):.4f}')
    return f'{result[num]}: {max(pre_val[0].detach()):.4f}'