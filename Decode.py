# Afleveret af
#   Magnus Simoni Jahn (majah25) &
#   Kjell Schoke (kjsch25) &
#   Yasmina Mojib (yamoj25)

import sys
from bitIO import BitReader
from Encode import build_huffman_tree


def read_frequencies(reader):
    frequencies = []
    # Læs 256 frekvenser fra filen, en for hver mulig byte-værdi
    for i in range(256):
        freq = reader.readint32bits()
        frequencies.append(freq)
    return frequencies


def decode_file(reader, root, total_bytes, output_file):
    current_node = root         # Start øverst i træet 
    bytes_written = 0           # En tæller der sikrer vi stopper på det rigtige tidspunkt
    
    while bytes_written < total_bytes:
        bit = reader.readbit()
        # 0 betyder gå til venstre, ellers gå til højre 
        if bit == 0:
            current_node = current_node.left
        else:
            current_node = current_node.right
        
        # Når vi rammer en bladnode har vi fundet en byte
        if current_node.byte_value is not None:
            output_file.write(bytes([current_node.byte_value]))
            bytes_written += 1
            current_node = root     # Start forfra fra toppen 


def main():
    infile = sys.argv[1]        # den komprimerede fil
    outfile = sys.argv[2]       # den dekomprimerede fil

    with open(infile, 'rb') as input_file:
        reader = BitReader(input_file)      # Læser filen bit for bit 
        
        # Læser frekvenstabellen, bygger Huffman-træet, finder ud af hvor mange bytes der skal dekodes i alt
        frequencies = read_frequencies(reader)
        root = build_huffman_tree(frequencies)
        total_bytes = sum(frequencies)
        
        # Dekoder resten af filen 
        with open(outfile, 'wb') as output_file:
            decode_file(reader, root, total_bytes, output_file)


if __name__ == '__main__':
    main()