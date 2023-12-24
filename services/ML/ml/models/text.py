import os
from functools import lru_cache

import math

import numpy as np

import torch
import torch.nn.functional as F

from torch import nn

from transformers import AutoTokenizer, AutoModel

class CFG:
    compute_cv = True  # set False to train model for submission

    bert_model_name = 'sentence-transformers/paraphrase-xlm-r-multilingual-v1'

    max_length = 128

    ### ArcFace
    scale = 30
    margin = 0.5
    fc_dim = 768
    seed = 412
    classes = 11014

    ### Training
    n_splits = 4  # GroupKFold(n_splits)
    batch_size = 16
    accum_iter = 1  # 1 if use_sam = True
    epochs = 15
    min_save_epoch = 0
    use_sam = True  # SAM (Sharpness-Aware Minimization for Efficiently Improving Generalization)
    use_amp = True  # Automatic Mixed Precision
    num_workers = 2  # On Windows, set 0 or export train_fn and TitleDataset as .py files for faster training.
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print(device)

    ### GradualWarmupSchedulerV2（lr_start -> lr_max -> lr_min）
    scheduler_params = {
        "lr_start": 7.5e-6,
        "lr_max": 1e-4,
        "lr_min": 2.74e-5, # 1.5e-5,
    }
    multiplier = scheduler_params['lr_max'] / scheduler_params['lr_start']
    eta_min = scheduler_params['lr_min']  # last minimum learning rate
    freeze_epo = 0
    warmup_epo = 2
    cosine_epo = epochs - freeze_epo - warmup_epo

    save_model_path = f'/content/drive/MyDrive/berts/final2/e{epochs}_bs{batch_size}_bertellio.pt'

### BERT

# Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask

### ArcFace
class ArcMarginProduct(nn.Module):
    def __init__(self, in_features, out_features, scale=30.0, margin=0.50, easy_margin=False, ls_eps=0.0):
        super(ArcMarginProduct, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.scale = scale
        self.margin = margin
        self.ls_eps = ls_eps  # label smoothing
        self.weight = nn.Parameter(torch.FloatTensor(out_features, in_features))
        nn.init.xavier_uniform_(self.weight)

        self.easy_margin = easy_margin
        self.cos_m = math.cos(margin)
        self.sin_m = math.sin(margin)
        self.th = math.cos(math.pi - margin)
        self.mm = math.sin(math.pi - margin) * margin

        self.criterion = nn.CrossEntropyLoss()

    def forward(self, input, label):
        # --------------------------- cos(theta) & phi(theta) ---------------------------
        if CFG.use_amp:
            cosine = F.linear(F.normalize(input), F.normalize(self.weight)).float()  # if CFG.use_amp
        else:
            cosine = F.linear(F.normalize(input), F.normalize(self.weight))
        sine = torch.sqrt(1.0 - torch.pow(cosine, 2))
        phi = cosine * self.cos_m - sine * self.sin_m
        if self.easy_margin:
            phi = torch.where(cosine > 0, phi, cosine)
        else:
            phi = torch.where(cosine > self.th, phi, cosine - self.mm)
        # --------------------------- convert label to one-hot ---------------------------
        one_hot = torch.zeros(cosine.size(), device=CFG.device)
        one_hot.scatter_(1, label.view(-1, 1).long(), 1)
        if self.ls_eps > 0:
            one_hot = (1 - self.ls_eps) * one_hot + self.ls_eps / self.out_features

        output = (one_hot * phi) + ((1.0 - one_hot) * cosine)
        output *= self.scale
        return output, self.criterion(output,label)

class ShopeeBertModel(nn.Module):

    def __init__(
        self,
        n_classes = CFG.classes,
        model_name = CFG.bert_model_name,
        fc_dim = CFG.fc_dim,
        margin = CFG.margin,
        scale = CFG.scale,
        use_fc = True
    ):

        super(ShopeeBertModel,self).__init__()
        print('Building Model Backbone for {} model'.format(model_name))


        self.backbone = AutoModel.from_pretrained(model_name).to(CFG.device)

        in_features = 768
        self.use_fc = use_fc

        if use_fc:
            self.dropout = nn.Dropout(p=0.0)
            self.classifier = nn.Linear(in_features, fc_dim)
            self.bn = nn.BatchNorm1d(fc_dim)
            self._init_params()
            in_features = fc_dim

        self.final = ArcMarginProduct(
            in_features,
            n_classes,
            scale = scale,
            margin = margin,
            easy_margin = False,
            ls_eps = 0.0
        )

    def _init_params(self):
        nn.init.xavier_normal_(self.classifier.weight)
        nn.init.constant_(self.classifier.bias, 0)
        nn.init.constant_(self.bn.weight, 1)
        nn.init.constant_(self.bn.bias, 0)

    def forward(self, texts, labels=torch.tensor([0])):

        input_ids = texts['input_ids']
        attention_mask = texts['attention_mask']

        #print(input_ids.shape)

        embedding = self.backbone(input_ids, attention_mask=attention_mask)

        x = mean_pooling(embedding, attention_mask)

        return x



class MatchingModel:
    def __init__(self):
        # ai-goods-backend/services/ML/ml/models/weights/model.onnx
        weights_path = '/content/drive/MyDrive/berts/final2/e15_bs16_bertellio.pt'

        self.bert_model = ShopeeBertModel()
        self.bert_model.load_state_dict(torch.load(weights_path))

        self.bert_model.to(self.device)

        self.tokenizer = AutoTokenizer.from_pretrained(CFG.bert_model_name)

    def run(self, text: np.ndarray) -> list[float]:

        text = self.tokenizer(text, padding=True, truncation=True,
                              max_length=CFG.max_length, return_tensors='pt').to(CFG.device)

        text_embeddings = self.bert_model(text).cpu()

        return text_embeddings

@lru_cache()
def get_matching_model():
    return MatchingModel()  # add caching class to avoid loading model each time
