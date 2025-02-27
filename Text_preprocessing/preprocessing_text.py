import string


def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        kata_dasar = [line.strip() for line in file if line.strip()]
    return kata_dasar

def sort_dict_by_freq(data, descending=True):
    return dict(sorted(data.items(), key=lambda item: item[1]['freq'], reverse=descending))

berita = input('masukan berita: ')
if (len(berita) < 1):
   print('masukan berita')
   exit
berita_token = ' '.join(word.strip(string.punctuation) for word in berita.split()).split()
stopwords = load_text('stopwords.txt')
kata_dasar_list = load_text('kata_dasar.txt')

processed_berita = {}

def isNumber(kata):
  angka = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
  for num in angka:
    if (num in kata):
      return True
  return False

def stem_kata(kata):
    awalan = ['peng', 'pem','meng', 'men', "me", "di", "ke", "se", "ber", "ter", "per", "pe"]
    akhiran = ["kan", "an"]

    original_kata = kata
    prefix_res = '';
    suffix_res = '';

    for prefix in awalan:
        if kata.startswith(prefix):
            kata = kata[len(prefix):]
            prefix_res = prefix
            break  

    for suffix in akhiran:
        if kata.endswith(suffix):
            kata = kata[:-len(suffix)]
            suffix_res = suffix
            break  

    if original_kata in kata_dasar_list:
      return {
            'prefix' : '',
            'suffix' : '',
            'res' : original_kata
        } 

    else:
        return {
            'prefix' : prefix_res,
            'suffix' : suffix_res,
            'res' : kata.strip(string.punctuation)
        } 


for index, substr in enumerate(berita_token):
    # print(index, substr)
    if (substr in processed_berita.keys()):
        processed_berita[substr]['freq'] += 1
    else:
      data = {
          'loc' : index + 1,
          'freq' : 1,
          'keterangan' : 'sementara'
      }

      if (isNumber(substr)):
        if ('angka' in processed_berita):
          processed_berita['angka']['freq'] += 1
          processed_berita['angka']['keterangan'] += ' ,' + substr
        else:
          data['freq'] = 1
          data['keterangan'] = substr
          processed_berita['angka'] = data
        continue
 
      if (substr in stopwords):
        data['keterangan'] = 'stopword'
        processed_berita[substr] = data
        continue
      
      if (substr.lower() in stopwords):
        data['keterangan'] = 'stopword'
        processed_berita[substr.lower()] = data
        continue
      
      original_kata = stem_kata(substr)
      if (original_kata['res'] in processed_berita.keys()):
          processed_berita[original_kata['res']]['freq'] += 1
          continue

      data['keterangan'] = ('Steming ( ' if  len(original_kata['prefix']) == 0 and len(original_kata['suffix']) > 0 else '' ) + ( f"Steming ( {original_kata['prefix']}-" if len(original_kata['prefix']) > 0 else '') + ('-' if len(original_kata['prefix']) < 1 and len(original_kata['suffix']) > 0  else '') + ( f"{original_kata['suffix']}" if len(original_kata['suffix']) > 0 else '') + ( ' )' if len(original_kata['prefix']) or len(original_kata['suffix']) else '')
      processed_berita[original_kata['res']] = data

def tampilkan_dalam_table(data):
    # Tentukan header tabel
    
    headers = ["No", "Kata", "Frekuensi", "Keterangan"]
    
    # Tentukan lebar kolom
    col_widths = [5, 15, 12, 15]

    # Fungsi untuk mencetak baris dengan format
    def print_row(row_data):
        row = ""
        for i, item in enumerate(row_data):
            row += str(item).ljust(col_widths[i])
        print(row)

    # Cetak header
    print("-" * sum(col_widths))
    print_row(headers)
    print("-" * sum(col_widths))

    # Cetak isi tabel
    for i, item in enumerate(data, start=1):
        print_row([data[item]['loc'], item, data[item]['freq'], data[item]['keterangan']])

    # Cetak garis akhir
    print("-" * sum(col_widths))

processed_berita = sort_dict_by_freq(processed_berita)
tampilkan_dalam_table(processed_berita)

for i in processed_berita:
    # print(i)
    print(processed_berita[i]['loc'])

print()
for i in processed_berita:
    # print(i)
    print(i)

print()
for i in processed_berita:
    # print(i)
    print(processed_berita[i]['freq'])

print()
for i in processed_berita:
    # print(i)
    print(processed_berita[i]['keterangan'])

# print(processed_berita)