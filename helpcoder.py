input_file = 'player.py'  # Входной файл с комментариями
output_file = 'helpcoder242.py'  # Выходной файл без комментариев

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        stripped_line = line.strip()
        if not stripped_line.startswith('#') and stripped_line != '':
            outfile.write(line)