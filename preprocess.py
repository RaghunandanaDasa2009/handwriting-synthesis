import json
import matplotlib.pyplot as plt

def process():
    try:
        with open('handwriting_data.jsonl', 'r') as f:
            lines = f.readlines()
        if not lines: return

        data = json.loads(lines[0])
        strokes = data['strokes']
        
        plt.figure(figsize=(12, 3))
        
        # Wir teilen die Punkte in Segmente auf, wann immer ein neuer Strich (s=1) beginnt
        segments = []
        current_seg = []
        
        for p in strokes:
            if p['s'] == 1 and current_seg:
                segments.append(current_seg)
                current_seg = []
            current_seg.append((p['x'], -p['y']))
        
        if current_seg:
            segments.append(current_seg)

        for seg in segments:
            x_vals, y_vals = zip(*seg)
            plt.plot(x_vals, y_vals, 'b-', linewidth=1.5)

        plt.axis('equal')
        plt.title(f"Vorschau: {data['text']}")
        plt.savefig('debug_output.png')
        print("Update erfolgreich! Schau dir 'debug_output.png' nochmal an.")
    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    process()
