import json

# Fungsi untuk mengubah latLong menjadi latitude dan longitude terpisah
def process_latlong(data):
    for item in data:
        # Ambil latLong yang ada sebagai string
        latLongStr = item.get('latLong', None)
        
        if latLongStr:
            # Mengubah tanda petik tunggal menjadi petik ganda agar JSON valid
            latLongStr = latLongStr.replace("'", '"')

            try:
                # Parsing latLong string menjadi dictionary
                latLong = json.loads(latLongStr)

                # Mengambil latitude dan longitude terpisah
                item['latitude'] = latLong.get('latitude')
                item['longitude'] = latLong.get('longitude')
                
                # Hapus latLong yang lama
                del item['latLong']
            except json.JSONDecodeError as e:
                print(f"Error parsing latLong: {latLongStr}")
                print(f"Error: {e}")
        else:
            print("latLong is missing or invalid")
    
    return data

# Membaca file JSON input
with open('input.json', 'r') as infile:
    input_data = json.load(infile)

# Proses data untuk mengubah latLong menjadi latitude dan longitude
processed_data = process_latlong(input_data)

# Menyimpan data yang telah diproses ke file JSON baru
with open('real_estate.json', 'w') as outfile:
    json.dump(processed_data, outfile, indent=4)

print("Data telah berhasil diproses dan disimpan sebagai real_estate.json")
