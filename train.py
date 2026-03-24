import torch
import torch.nn as nn
import torch.optim as optim
import time
from torch.utils.data import DataLoader, Dataset
from model import HandwritingRNN

# Dataset Klasse für schnelles Laden
class PenDataset(Dataset):
    def __init__(self, data):
        self.strokes = data['strokes']
        self.texts = data['texts']
    def __len__(self): return len(self.strokes)
    def __getitem__(self, idx): return self.texts[idx][0], self.strokes[idx]

data_load = torch.load('dataset.pt')
dataset = PenDataset(data_load)
# Wir trainieren 1 Satz nach dem anderen, aber mit optimiertem Speicher
train_loader = DataLoader(dataset, batch_size=1, shuffle=True)

model = HandwritingRNN(vocab_size=len(data_load['char_map']))
optimizer = optim.Adam(model.parameters(), lr=0.0005)
criterion_pos, criterion_pen = nn.MSELoss(), nn.BCEWithLogitsLoss()

print(f"Deep-Learning Modus: Aktiviert für {len(dataset)} Sätze.")

for epoch in range(300):
    total_loss = 0
    for char_idx, stroke in train_loader:
        if stroke.size(1) < 2: continue
        optimizer.zero_grad()
        # Input und Target (Slicing)
        inp, target = stroke[:, :-1], stroke[:, 1:]
        output, _ = model(char_idx, inp)
        
        loss = criterion_pos(output[:, :, :2], target[:, :, :2]) + 5.0 * criterion_pen(output[:, :, 2], target[:, :, 2])
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        total_loss += loss.item()
    
    time.sleep(0.1) # Kurze Atempause für die CPU
    if (epoch + 1) % 20 == 0:
        print(f"Epoch {epoch+1}/300 | Durchschnitts-Loss: {total_loss/len(dataset):.5f}")

torch.save(model.state_dict(), 'handwriting_model.pth')
print("Larry ist jetzt ein Meister seiner Klasse!")
