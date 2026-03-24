import json
import torch
import numpy as np

def prepare():
    with open('handwriting_data.jsonl', 'r') as f:
        lines = f.readlines()

    all_strokes = []
    all_texts = []
    chars = sorted(list(set("".join([json.loads(l)['text'] for l in lines]) + " ")))
    char_to_idx = {ch: i for i, ch in enumerate(chars)}

    for line in lines:
        data = json.loads(line)
        text_indices = [char_to_idx[ch] for ch in data['text']]
        
        strokes = data['strokes']
        pts = []
        prev_x, prev_y = strokes[0]['x'], strokes[0]['y']
        
        for p in strokes:
            # Wir speichern: [delta_x, delta_y, pen_up_status]
            dx = p['x'] - prev_x
            dy = p['y'] - prev_y
            pts.append([dx, dy, p['s']])
            prev_x, prev_y = p['x'], p['y']
        
        all_strokes.append(torch.tensor(pts, dtype=torch.float32))
        all_texts.append(torch.tensor(text_indices, dtype=torch.long))

    torch.save({'strokes': all_strokes, 'texts': all_texts, 'char_map': char_to_idx}, 'dataset.pt')
    print(f"Fertig! {len(all_strokes)} Sätze konvertiert und in dataset.pt gespeichert.")

if __name__ == "__main__":
    prepare()
