import os
from pathlib import Path


class LZZDecompressor:
    def __init__(self):
        self.window_size = 4096
        self.min_match_length = 3
        self.buffer = bytearray()

    def _add_to_window(self, byte):
        self.buffer.append(byte)
        if len(self.buffer) > self.window_size:
            self.buffer = self.buffer[-self.window_size:]

    def decompress(self, compressed_data):
        output = bytearray()
        self.buffer.clear()
        i = 0

        while i < len(compressed_data):
            flag = compressed_data[i]
            i += 1

            if flag & 0x80:  # Match
                if i + 1 >= len(compressed_data):
                    break

                offset = ((flag & 0x7F) << 8) | compressed_data[i]
                i += 1
                length = compressed_data[i] + self.min_match_length
                i += 1

                if offset > len(self.buffer):
                    continue

                # Copia byte per byte, aggiungendo al buffer man mano
                for j in range(length):
                    if offset <= len(self.buffer):
                        byte = self.buffer[-offset]
                        output.append(byte)
                        self._add_to_window(byte)
            else:  # Literal
                output.append(flag)
                self._add_to_window(flag)

        return bytes(output)


def process_directory(input_dir, output_dir):
    decompressor = LZZDecompressor()
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    for item in input_path.rglob('*'):
        if item.is_file():
            relative_path = item.relative_to(input_path)
            output_file = output_path / relative_path

            output_file.parent.mkdir(parents=True, exist_ok=True)

            try:
                with open(item, 'rb') as f:
                    compressed_data = f.read()

                decompressed_data = decompressor.decompress(compressed_data)

                with open(output_file, 'wb') as f:
                    f.write(decompressed_data)

                print(f"Decompresso: {item} -> {output_file}")
            except Exception as e:
                print(f"Errore durante la decompressione di {item}: {str(e)}")


if __name__ == "__main__":
    process_directory("input", "output")