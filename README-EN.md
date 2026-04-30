### English README

# Secure Key Generator (multi-pass-generator)

A tool for bulk generation of cryptographically secure passwords with flexible parameter configuration for each block. Allows creating hundreds of unique combinations in a single run with automatic export to structured folders.

## Features

- Bulk generation of multiple independent password blocks in a single run
- Support for Latin, Cyrillic, and Armenian alphabets (lowercase and uppercase)
- Cryptographically secure generation based on the `secrets` module
- Automatic creation of structured folders with dual file formats (numbered and unnumbered)
- Dark and light interface themes
- Bilingual interface (English/Russian)
- Fully offline operation with no data transmission over the network
- Ability to build into a standalone EXE file without Python installation

## Requirements

- Python 3.6 or higher
- Pillow library (for application icon support)

## Installation from Source

1. Clone the repository:
   `git clone <repository-url>`
2. Navigate to the project directory:
   `cd multi-pass-generator`
3. Create and activate a virtual environment:
   `python -m venv venv`
   `venv\Scripts\activate` (Windows) 
4. Install dependencies:
   `pip install -r requirements.txt`
5. Run the application:
   `python main.py`

## Usage

1. Configure block parameters: specify password count, length, and select desired character sets.
2. Add additional blocks using the "Add Block" button if needed.
3. Click "Generate" and select the target directory.
4. Results will be automatically saved in the `generated_keys/` structure.

## Output Format

For each block, a separate directory is created containing:
- `keys.txt` — password list without numbering
- `keys_numbered.txt` — password list with sequential numbering
- `README.txt` — configuration log and generation timestamp

## Building Standalone Executable (Windows)

To create a portable version, use the built-in script: `build.py` 

## Security

- Generation relies on the cryptographically secure `secrets` module
- No internet connection required
- Data is not transmitted to external servers and is not logged
