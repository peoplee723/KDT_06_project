import torch                    #텐서 및 수치 계산 모듈
import torch.nn as nn           #인공신경망
import torch.nn.functional as F      #손실, 거리 계산 모듈
import torch.optim as optimizer # 최적화 기법 모듈
from torchmetrics.classification import ConfusionMatrix
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler, OneHotEncoder, OrdinalEncoder, LabelEncoder
import matplotlib.pyplot as plt





# 함수 만들기
# 입력받은 데이터의 shape과 type을 바꿔주는 함수 (피쳐의 개수에 따라)


class Torch_proccesing:
    def __init__(self, Data) -> None:
        self.data=Data
        
        # self.sc_model=None
        # self.model=None
        # self.optim=None
        # self.X_train=None
        # self.X_train_sacled=None
        # self.Y_train=None
        # self.X_val=None
        # self.X_val_scaled=None
        # self.Y_val=None
        # self.X_test=None
        # self.X_test_scaled=None
        # self.Y_test=None
        # self.feature=None
        # self.target=None
        # self.loss_history=[]

    def make_tensor(self, feature, target, show_shape=False): 
        '''
        DF를 tensor로 만드는 함수
        params: feature, target 컬럼명
        '''
        self.feature=torch.from_numpy(self.data[feature].values).float()
        self.target=torch.from_numpy(self.data[[target]].values).float()
        # self.feature=torch.from_numpy(feature.values).float()
        # self.target=torch.from_numpy(target.values).float()
        
        if show_shape:
            print(self.feature.shape, self.target.shape)
        return self.feature, self.target
    
    def encoding(self, encoder, Data):
        '''
        인코딩 하는 함수
        '''
        encode_model=encoder
        enc_data= encode_model.fit_transform(Data)
        print(f'enc: {enc_data.shape}, {enc_data.ndim}')
        return enc_data
        

    
    def split(self, val=True, testsize=.25, random_state=None, 
              get_data=False,  classification=True):
        '''
        데이터를 분리하는 함수
        params: testsize, ranodm_state, val, get_data
        return: get_data=True일때 스케일링된 데이터 반환
        '''
        if val:
            if classification:

                self.X_train, self.X_test, self.Y_train, self.Y_test= train_test_split(self.feature, self.target, 
                                                                    test_size=testsize, 
                                                                    random_state=random_state,stratify=self.target)
                self.X_train, self.X_val, self.Y_train, self.Y_val=train_test_split(self.X_train, self.Y_train,
                                                                                    test_size=testsize,
                                                                                    random_state=random_state,
                                                                                    stratify=self.Y_train)
            else:
                self.X_train, self.X_test, self.Y_train, self.Y_test= train_test_split(self.feature, self.target, 
                                                                    test_size=testsize, 
                                                                    random_state=random_state)
                self.X_train, self.X_val, self.Y_train, self.Y_val=train_test_split(self.X_train, self.Y_train,
                                                                                    test_size=testsize,
                                                                                    random_state=random_state)
            print(f'train: {self.X_train.shape},{self.Y_train.shape}\n\
test: {self.X_test.shape},{self.Y_test.shape}\n\
val: {self.X_val.shape},{self.Y_val.shape}')
        else: pass

        
        if get_data:
            X_train, X_test, Y_train, Y_test= train_test_split(self.feature, self.target, 
                                                            test_size=testsize, 
                                                            random_state=random_state)
            print(f'train: {X_train.shape},{Y_train.shape}\n\
test: {X_test.shape},{Y_test.shape}')
            return X_train, X_test, Y_train, Y_test
        
        else:

            self.X_train, self.X_test, self.Y_train, self.Y_test= train_test_split(self.feature, self.target, 
                                                                test_size=testsize, 
                                                                random_state=random_state)
            print(f'train: {self.X_train.shape},{self.Y_train.shape}\n\
test: {self.X_test.shape},{self.Y_test.shape}')

    def look_params(self):
        '''
        모델 파라미터 보는함수
        '''
        for name, param in self.model.named_parameters():
            print(name, param, '\n')
    
    
    def get_scaled(self, scaler_name, val=True):
        '''
        분리된 데이터를 바탕으로 스케일링 하는 함수(인스턴스에 저장 또는 반환)\n
        params: scaler_name, get_data\n
        return: 스케일링된 데이터의 shape, nidim 또는 스케일링된 데이터\n
        '''
        self.sc_model=scaler_name
        # shape 변환-> numpy일 경우 reshape, Series일 경우 DataFrame으로

        
        self.sc_model.fit(self.X_train)

        if val:
            self.X_train_scaled= self.sc_model.transform(self.X_train)
            self.X_test_scaled= self.sc_model.transform(self.X_test)
            self.X_val_scaled= self.sc_model.transform(self.X_val)
            print(f'X_train_scaled: {self.X_train_scaled.shape},{self.X_test_scaled.ndim}\n\
X_test_scaled: {self.X_test_scaled.shape},{self.X_test_scaled.ndim}\n\
X_val_scaled: {self.X_val_scaled.shape},{self.X_val_scaled.ndim}')
        else:
            self.X_train_scaled= self.sc_model.transform(self.X_train)
            self.X_test_scaled= self.sc_model.transform(self.X_test)
            print(f'X_train_scaled: {self.X_train_scaled.shape},{self.X_test_scaled.ndim}\n\
X_test_scaled: {self.X_test_scaled.shape},{self.X_test_scaled.ndim}')
    
    def diff_check(self):
        '''
        학습과 검증데이터의 오차를 시각화하는 함수
        '''
        plt.plot(range(1,len(self.loss_history[0])+1), self.loss_history[0], label='train')
        plt.plot(range(1,len(self.loss_history[1])+1), self.loss_history[1], label='Val')
        plt.title('train & valid')
        plt.grid()
        plt.legend()
        plt.show()
    
    def confusion_matrix(self, task):
        metric= ConfusionMatrix(task=task)
        metric.update(self.pred, self.Y_test)
        fig, ax= metric.plot()

def version_check(module_list: list):
    '''
    모듈의 버전을 확인하는 함수
    '''
    
    for modul in module_list:
        print(modul.__version__)

def show_outliers(DF, colname: str):
    '''
    이상치 데이터를 도출하는 함수
    params: 데이터프레임, 컬럼명
    '''
    q1=DF[colname].quantile(0.25)
    q3= DF[colname].quantile(0.75)
    iqr= q3-q1
    lower_bound=q1-( 1.5*iqr)
    upper_bound=q1+ (1.5*iqr)

    outliers= DF[(DF[colname] < lower_bound) | (DF[colname] > upper_bound)]
    return outliers