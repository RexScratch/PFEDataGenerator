chars = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$¢€£¥%^&*()-–—=≠[]\\;\'‘’,./_+{}|:"“”<≤≥>?`~×⋅÷±°′″'

font = input("Font: ")
if font == '':
    font = 'sans-serif'

weight = input("Weight: ")
if weight == '':
    weight = 'normal'

style = input("Style: ")
if style == '':
    style = 'normal'

svg = '<?xml version="1.0" encoding="UTF-8"?><svg width="1" height="1" viewBox="0 0 1 1" xmlns="http://www.w3.org/2000/svg">'

for c in 'HX' + chars:
    if c == '&':
        c = '&amp;'
    elif c == '<':
        c = '&lt;'
    svg += '<text font-family="{}" font-weight="{}" font-style="{}" x="0" y="1" fill="#000" stroke="none" text-anchor="start" font-size="1px" letter-spacing="0">|{}|</text>'.format(font, weight, style, c)

svg += '<text font-family="{}" font-weight="{}" font-style="{}" x="0" y="2" fill="#000" stroke="none" text-anchor="start" font-size="1px" letter-spacing="0">{}</text>'.format(font, weight, style, font)
svg += '</svg>'
f = open('text.svg', 'w', encoding='utf-8')
f.write(svg)
f.close()