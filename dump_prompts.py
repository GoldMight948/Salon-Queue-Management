import json

transcript_path = r"C:\Users\AAHAN\.gemini\antigravity\brain\c4f6e75b-ac4a-4d5d-8add-6761cabe56ae\.system_generated\logs\transcript.jsonl"
prompts = []

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        d = json.loads(line)
        if d.get('type') == 'USER_INPUT':
            prompts.append({
                'created_at': d.get('created_at'),
                'content': d.get('content')
            })

print(f"Total USER_INPUT prompts: {len(prompts)}")
for i, p in enumerate(prompts):
    print(f"\n==================== PROMPT {i+1} ({p['created_at']}) ====================")
    print(p['content'])
