import torch
import torch.nn as nn
import torch.nn.functional as F

class Encoder(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers=1, dropout=0.1):
        super(Encoder, self).__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.dropout = dropout
        
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, dropout=dropout, batch_first=True)
    
    
class Attention(nn.Module):
    def __init__(self, input_dim,hidden_dim, output_dim):
        super(Attention, self).__init__()
        self.input_dim = input_dim
        self.hidden_dim = input_dim // 2
        self.output_dim = output_dim
        
    def forward(self, x):
        # Compute attention scores
        attn_scores = torch.matmul(x, x.transpose(-1, -2))
        attn_weights = F.softmax(attn_scores, dim=-1)
        
        # Apply attention weights to the input
        context = torch.matmul(attn_weights, x)
        
        return context