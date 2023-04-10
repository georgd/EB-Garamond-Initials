from fontTools.ttLib import TTFont
from fontTools.colorLib import builder as colr_builder
import argparse

argparser = argparse.ArgumentParser(description=
    "Generate a color font from a given font where the color layer glyphs have a suffix .bg (background layer) and .fg (foreground layer).")
argparser.add_argument(
    'input',
    help='Input font source, e.g. "/some/path/Bla.sfdir"')
argparser.add_argument(
    'output',
    help='Output font file, e.g. "/some/path/Bla.otf"')
args = argparser.parse_args()

# Open the font file
font = TTFont(args.input)

# create two color palettes
palette1 = [(0,0,0,1), (1,0,0,1)]
palette2 = [(0.7,0.5,0.2,1), (0,0,1,1)]
cpal=colr_builder.buildCPAL([palette1, palette2])


font['CPAL'] = cpal

# create the COLR table
# Define the list of suffixes for the layer glyphs

# Create a list of glyph names and corresponding layer glyph names
glyphs = {}
for glyph_name in font.getGlyphOrder():
    if glyph_name.endswith(".bg"):
        base_glyph_name, layer_suffix = glyph_name.rsplit(".", 1)
        glyphs[base_glyph_name] = [(base_glyph_name  + "." + "bg", 0),(base_glyph_name + "." + "fg", 1)]
colr_table = colr_builder.buildCOLR(glyphs)

# add the COLR table to the font
font['COLR'] = colr_table
# Save the modified font file
font.save(args.output)

