import torch
import torch.nn as nn

class HandwritingRNN(nn.Module):
    def __init__(self, vocab_size, hidden_size=512, n_layers=3):
        super(HandwritingRNN, self).__init__()
        self.hidden_size = hidden_size
        self.n_layers = n_layers
        
        self.encoder = nn.Embedding(vocab_size, 128)
        # LSTM mit Dropout gegen Overfitting (die Spiralen)
        self.lstm = nn.LSTM(128 + 3, hidden_size, n_layers, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_size, 3)
        
    def forward(self, char_idx, strokes, hidden=None):
        char_emb = self.encoder(char_idx)
        # Kontext für die gesamte Sequenz wiederholen
        char_emb = char_emb.unsqueeze(1).repeat(1, strokes.size(1), 1)
        x = torch.cat([char_emb, strokes], dim=-1)
        output, hidden = self.lstm(x, hidden)
        output = self.fc(output)
        return output, hidden
