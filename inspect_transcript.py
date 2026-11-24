import json

transcript_path = r"C:\Users\AAHAN\.gemini\antigravity\brain\c4f6e75b-ac4a-4d5d-8add-6761cabe56ae\.system_generated\logs\transcript.jsonl"
with open(transcript_path, 'r', encoding='utf-8') as f:
    for i in range(5):
        line = f.readline()
        if not line: break
        d = json.loads(line)
        print(f"Line {i+1} keys:", list(d.keys()))
        if 'role' in d:
            print("role:", d['role'])
        if 'type' in d:
            print("type:", d['type'])
        print("sample:", str(d)[:200])
