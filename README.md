Pen Font Engine Data Generator
===

A set of Python scripts that convert TrueType and OpenType fonts to font data for Pen Font Engine
[Pen Font Engine on Scratch](https://scratch.mit.edu/projects/318234147/)

Requirements
---

- Python 3.6 or later
- Inkscape

Installation
---

Download and extract the .zip file and move the folder wherever you want.

Usage
---
1. Open `svgcreate.py` using Python
2. Enter the font name
3. Enter the font weight (uses [svg font-weight](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/font-weight), enter nothing for normal weight)
4. Enter the font style (uses [svg font-style](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/font-style), enter nothing for normal style)
5. Open `text.svg` using Inkscape
6. Select everything in the drawing
7. If necessary, select the correct font from the Inkscape font menu
8. Under Path, select "Object to Path" and wait for the operation to finish
9. Save `text.svg` in Inkscape
10. Open `generate.py` using Python
11. Enter the font name to be used in Pen Font Engine
12. Open `output.txt` and select and copy all text
13. In Pen Font Engine, paste the text into the block labeled "Import Font | Data" and run the block

Using `width.txt`
---

Sometimes (such as when converting an italic font), it may be necessary to use the character widths of a different font when converting a font.

1. Paste the converted font data for the font with the widths you want to use into `width.txt`
2. Follow the steps above to generate the font data for the desired font. When asked whether to use `width.txt` in `generate.py`, enter `y`.