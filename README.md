# CityUBeamer

A LaTeX Beamer template and toolset for automatically converting documents into professional presentations.

## Features

- Professional LaTeX Beamer template with CityU styling
- AI-powered document-to-presentation conversion
- Automatic image handling for remote resources
- Built-in content balancing and formatting rules

## Getting Started

### Prerequisites

- LaTeX distribution (e.g., TeX Live or MiKTeX)
- Python 3.x
- Required LaTeX packages:
  - beamer
  - amsmath
  - graphicx
  - booktabs
  - algorithm
  - algpseudocode
  - transparent

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cityubeamer.git
cd cityubeamer
```

## Usage

### Template Only

To use the Beamer template directly:

1. Copy `template/slide.tex` to your working directory
2. Modify the content while keeping the styling
3. Compile using your preferred LaTeX compiler

### Automatic Document Conversion

1. Prepare your document in markdown format as `document.md`
2. Run the preprocessing script to handle images:
```bash
python preprocessing.py
```
3. Use the AI conversion tool following instructions in `INSTRUCTION.md`
4. Compile the generated `main.tex` file

## Template Features

- 16:9 aspect ratio optimized
- Custom block styling with orange accent colors
- Integrated logo support with transparency
- Section headers in frame titles
- Progress bar footer
- Mathematical equation support
- Table and figure formatting

## Content Guidelines

As specified in `INSTRUCTION.md`:

- Maximum 8 lines of text per frame
- Maximum 2 lines of captions per image
- One image or large table per frame
- Automatic handling of citations in MLA style
- Smart animation insertion for content-heavy slides

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Authors

[Add author information here]
