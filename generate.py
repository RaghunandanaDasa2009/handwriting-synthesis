import torch
import numpy as np
import matplotlib.pyplot as plt
from model import HandwritingRNN

data = torch.load('dataset.pt')
char_map = data['char_map']
model = HandwritingRNN(vocab_size=len(char_map))
model.load_state_dict(torch.load('handwriting_model.pth'))
model.eval()

def generate(char_to_write, length=100):
    idx = char_map.get(char_to_write, 0)
    char_idx = torch.tensor([idx])
    
    current_stroke = torch.tensor([[[0.0, 0.0, 1.0]]])
    strokes = []
    hidden = None
    
    with torch.no_grad():
        for _ in range(length):
            output, hidden = model(char_idx, current_stroke, hidden)
            next_pt = output.squeeze().numpy()
            
            # Temperatur-Trick: Wir dämpfen die Vorhersage leicht (Stabilität)
            next_pt[:2] *= 0.8 
            
            strokes.append(next_pt)
            current_stroke = torch.tensor(next_pt).view(1, 1, 3)
    
    strokes = np.array(strokes)
    x, y = np.cumsum(strokes[:, 0]), np.cumsum(-strokes[:, 1])
    
    plt.figure(figsize=(8, 2))
    plt.plot(x, y, 'r-', linewidth=2)
    plt.axis('equal')
    plt.title(f"KI schreibt: {char_to_write}")
    plt.savefig('output_larry_v3.png')
    print(f"Check mal 'output_larry_v3.png' für den Buchstaben {char_to_write}!")

generate('H')
