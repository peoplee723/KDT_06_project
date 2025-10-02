import torch
from torch.utils.data import Dataset

class Custom_Dataset(Dataset):
    def __init__(self, featureDF, targetDF) -> None:
        super().__init__()
        self.featureDF= featureDF
        self.targetDF= targetDF
        self.n_rows= featureDF.shape[0]
        self.n_features= featureDF.shape[1]
    
    def __len__(self):
        return self.n_rows
    
    def __getitem__(self, index):
        featureTS= torch.FloatTensor(self.featureDF.iloc[index].values)
        targetTS= torch.FloatTensor(self.targetDF.iloc[index].values)
        return featureTS, targetTS