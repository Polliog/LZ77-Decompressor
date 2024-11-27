# LZZ Decompressor

Python implementation of LZZ decompression algorithm with recursive directory processing.

## Features

- Sliding window decompression (4KB buffer)
- Match encoding with 13-bit offset and 8-bit length
- Minimum match length of 3 bytes
- Recursive directory processing
- Path structure preservation

## Usage

```python
# Decompress single file
decompressor = LZZDecompressor()
with open('compressed.bin', 'rb') as f:
    compressed = f.read()
decompressed = decompressor.decompress(compressed)

# Process directory
process_directory('input_dir', 'output_dir')
```

## File Format

Binary format of compressed files:
- Flag byte (MSB=1 for match, MSB=0 for literal)
- For matches:
  - 13-bit offset (7 bits in flag + next byte)
  - 8-bit length (actual length = stored + 3)
- For literals:
  - 7-bit value stored directly in flag byte

## Error Handling

- Buffer overflow protection
- Invalid offset detection  
- Corrupt file handling
- Directory creation checks

## Requirements

- Python 3.6+
- No external dependencies

## License

MIT License