import json

# Baca file JSON
with open('zillow_data.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# Parse string JSON yang di-escape
cleaned_data = json.loads(raw_data)

# Simpan JSON yang sudah dibersihkan
with open('zillow_data_clean.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

print("File berhasil dibersihkan dan disimpan sebagai 'zillow_data_clean.json'")