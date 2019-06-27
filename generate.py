import math, functools

chars = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$¢€£¥%^&*()-–—=≠[]\\;\'‘’,./_+{}|:"“”<≤≥>?`~×⋅÷±°′″'

class line:

    def __init__(self, p1, p2):

        if p1[0] < p2[0]:
            self.left = p1
            self.right = p2
        else:
            self.left = p2
            self.right = p1

        self.leftx = self.left[0]
        self.rightx = self.right[0]
        self.lefty = self.left[1]
        self.righty = self.right[1]

        self.ymin = min(self.lefty, self.righty)
        self.ymax = max(self.lefty, self.righty)

        self.width = self.rightx - self.leftx
        self.height = self.righty - self.lefty
        
        if self.leftx == self.rightx:
            self.slope = float('inf')
            self.yint = float('nan')
        else:
            self.slope = self.height / self.width
            self.yint = -1 * self.slope * self.leftx + self.lefty

    def yOfX(self, x):
        return self.slope * x + self.yint

    def string(self, xo):
        return 'l{},{},{},{},'.format(roundDec(self.leftx - xo), roundDec(self.rightx - xo), roundDec(self.height), roundDec(self.lefty - 0.25))

    def __repr__(self):
        return f'line(({self.leftx}, {self.lefty}), ({self.rightx}, {self.righty}))'

class bezier:

    def __init__(self, p1, p2, p3):

        self.x1 = p1[0]
        self.x2 = p2[0]
        self.x3 = p3[0]
        self.y1 = p1[1]
        self.y2 = p2[1]
        self.y3 = p3[1]

        self.ax = self.x3 - 2 * self.x2 + self.x1
        if self.ax < 1e-10:
            self.ax = 0
        self.bx = 2 * (self.x2 - self.x1)
        if self.bx < 1e-10:
            self.bx = 0
        self.cx = self.x1
        self.ay = self.y3 - 2 * self.y2 + self.y1
        self.by = 2 * (self.y2 - self.y1)
        self.cy = self.y1

        self.extremext = bezier.extremeT(self.ax, self.bx, self.cx)
        self.extremex = bezier.extreme(self.ax, self.bx, self.cx)
        if (self.extremex == None) or not (0 <= self.extremext <= 1):
            self.xmin = min(self.x1, self.x3)
            self.xmax = max(self.x1, self.x3)
        else:
            self.xmin = min(self.x1, self.x3, self.extremex)
            self.xmax = max(self.x1, self.x3, self.extremex)
        self.leftx = self.xmin
        self.rightx = self.xmax

        self.extremeyt = bezier.extremeT(self.ay, self.by, self.cy)
        self.extremey = bezier.extreme(self.ay, self.by, self.cy)
        if (self.extremey == None) or not (0 <= self.extremeyt <= 1):
            self.ymin = min(self.y1, self.y3)
            self.ymax = max(self.y1, self.y3)
        else:
            self.ymin = min(self.y1, self.y3, self.extremey)
            self.ymax = max(self.y1, self.y3, self.extremey)

    @staticmethod
    def extreme(a, b, c):

        if a == 0:
            return None
        
        t = (-1 * b) / (2 * a)

        return c + t * (b + t * a)

    @staticmethod
    def extremeT(a, b, c):

        if a == 0:
            return None
        
        return (-1 * b) / (2 * a)

    def yOfX(self, x):

        if x == self.x1:
            return self.y1
        if x == self.x3:
            return self.y3

        if self.ax == 0:
            t = (x - self.cx) / self.bx
        else:
            discriminant = (self.bx * self.bx - 4 * self.ax * (self.cx - x)) + 1e-7
            if discriminant < 0:
                return float('nan')
            t = (-1 * self.bx + math.sqrt(discriminant)) / (2 * self.ax)

        return self.cy + t * (self.by + t * self.ay)

    def simpleCurves(self):

        if (self.extremext == None) or not(1e-6 <= self.extremext <= 1 - 1e-6):
            if self.x1 < self.x3:
                midx = self.x2
                if midx < self.x1:
                    midx = self.x1
                elif midx > self.x3:
                    midx = self.x3
                return [bezier((self.x1, self.y1), (midx, self.y2), (self.x3, self.y3))]
            else:
                midx = self.x2
                if midx < self.x3:
                    midx = self.x3
                elif midx > self.x1:
                    midx = self.x1
                return [bezier((self.x3, self.y3), (self.x2, self.y2), (self.x1, self.y1))]
        else:
            t = self.extremext
            midx = self.cx + t * (self.bx + t * self.ax)
            midy = self.cy + t * (self.by + t * self.ay)
            mid = (midx, midy)

            ot = 1 - t

            x4 = ot * self.x1 + t * self.x2
            y4 = ot * self.y1 + t * self.y2

            x5 = ot * self.x2 + t * self.x3
            y5 = ot * self.y2 + t * self.y3

            if midx > self.x1:
                return [bezier((self.x1, self.y1), (x4, y4), mid), bezier((self.x3, self.y3), (x5, y5), mid)]
            else:
                return [bezier(mid, (x4, y4), (self.x1, self.y1)), bezier(mid, (x5, y5), (self.x3, self.y3))]

    def string(self, xo):
        return '{},{},{},{},{},{},'.format(roundDec(self.x1 - xo), roundDec(self.x2 - xo), roundDec(self.x3 - xo), roundSf(self.ay), roundSf(self.by), roundDec(self.cy - 0.25))

    def __repr__(self):
        return f'bezier(({self.x1}, {self.y1}), ({self.x2}, {self.y2}), ({self.x3}, {self.y3}))'

def compare(obj1, obj2):
    # Assumes no intersections and simple curves

    EPSILON = 1e-7
    if ((obj2.leftx + EPSILON) >= obj1.rightx) or ((obj1.leftx + EPSILON) >= obj2.rightx):
        return 0

    for x in [obj1.leftx, obj1.rightx, obj2.leftx, obj2.rightx, (obj1.leftx + obj2.rightx) / 2, (obj2.leftx + obj1.rightx) / 2, (obj1.leftx + obj1.rightx) / 2, (obj2.leftx + obj2.rightx) / 2]:
        if (obj1.leftx <= x <= obj1.rightx) and (obj2.leftx <= x <= obj2.rightx):
            diff = obj1.yOfX(x) - obj2.yOfX(x)
            if abs(diff) > 1e-6:
                return diff

    # Just in case, probably will never run
    for lerp in range(1, 100, 1):
        lerpf = lerp / 100.0

        x = lerpf * obj1.rightx + (1 - lerpf) * obj1.leftx
        if (obj1.leftx <= x <= obj1.rightx) and (obj2.leftx <= x <= obj2.rightx):
            diff = obj1.yOfX(x) - obj2.yOfX(x)
            if abs(diff) > 1e-6:
                return diff

        x = lerpf * obj2.rightx + (1 - lerpf) * obj2.leftx
        if (obj1.leftx <= x <= obj1.rightx) and (obj2.leftx <= x <= obj2.rightx):
            diff = obj1.yOfX(x) - obj2.yOfX(x)
            if abs(diff) > 1e-6:
                return diff
    
    return 0

def attemptToNum(s):

    try:
        return float(s)
    except:
        return s

def formatNum(n):

    if n == float('nan'):
        return 'NaN'
    elif n == float('-inf'):
        return '-Infinity'
    elif n == float('inf'):
        return 'Infinity'

    n = float('{:.5g}'.format(n))

    if n == 0:
        return '0'
    if n == int(n):
        n = int(n)

    exp = math.floor(math.log(abs(n), 10))
    man = round(n / float(f'1e{exp}'), 5)

    if man == int(man):
        man = int(man)

    s = f'{man}e{exp}'

    s2 = str(n)

    if s2[0:2] == '0.':
        s2 = s2[1:]
    elif s2[0:3] == '-0.':
        s2 = '-' + s2[2:]

    if len(s) < len(s2):
        return s

    return s2

def roundDec(n):
    return formatNum(round(n, 5))

def roundSf(n):
    # return float('{:.5g}'.format(n))
    return formatNum(n)

def coordsToStr(x, y, scale):
    return '{},{},'.format(x / scale, (1 - y) / scale)

def cubicToQuadratic(x, y, c1x, c1y, c2x, c2y, ex, ey, depth):

    c12x = 1.5 * c1x - 0.5 * x
    c34x = 1.5 * c2x - 0.5 * ex
    c12y = 1.5 * c1y - 0.5 * y
    c34y = 1.5 * c2y - 0.5 * ey

    if ((abs(c12x - c34x) < 1e-8) and (abs(c12y - c34y) < 1e-8)) or (depth <= 0):
        cx = (c12x + c34x) / 2
        cy = (c12y + c34y) / 2
        return [((x, y), (cx, cy), (ex, ey))]
    else:
        points = 5 * [None]
        points[0] = ((x + c1x)/2, (y + c1y)/2)
        mid = ((c1x + c2x)/2, (c1y + c2y)/2)
        points[4] = ((c2x + ex)/2, (c2y + ey)/2)
        points[1] = ((points[0][0] + mid[0])/2, (points[0][1] + mid[1])/2)
        points[3] = ((points[4][0] + mid[0])/2, (points[4][1] + mid[1])/2)
        points[2] = ((points[1][0] + points[3][0])/2, (points[1][1] + points[3][1])/2)

        curves = cubicToQuadratic(x, y, points[0][0], points[0][1], points[1][0], points[1][1], points[2][0], points[2][1], depth - 1)
        curves.extend(cubicToQuadratic(points[2][0], points[2][1], points[3][0], points[3][1], points[4][0], points[4][1], ex, ey, depth - 1))
        return curves


def pathRawData(path, ix, iy, scale):

    Xmin = float('inf')
    Xmax = float('-inf')
    Ymin = float('inf')
    Ymax = float('-inf')

    path = path.split(' ')
    out = ''

    x, y = ix, iy
    sx, sy = None, None
    moveLine = False

    i = 0
    length = len(path)
    while i < length:
        
        if path[i].lower() in ['m', 'l', 'h', 'v', 'q', 'c', 'z']:
            cmd = path[i]
        else:
            i -= 1
            if cmd == 'm':
                cmd = 'l'
            elif cmd == 'M':
                cmd = 'L'

        if cmd == 'M':
            x, y = [float(n) for n in path[i+1].split(',')]
            x += ix
            y += iy
            sx, sy = x, y
            i += 2
        elif cmd == 'm':
            coords = [float(n) for n in path[i+1].split(',')]
            x += coords[0]
            y += coords[1]
            sx, sy = x, y
            i += 2

        elif cmd in ['L', 'l']:
            nx, ny = [float(n) for n in path[i+1].split(',')]
            if cmd == 'L':
                nx += ix
                ny += iy
            else:
                nx += x
                ny += y
            out += coordsToStr(x, y, scale)
            out += coordsToStr(nx, ny, scale)
            x, y = nx, ny
            i += 2
        
        elif cmd in ['H', 'h']:
            nx = float(path[i+1])
            if cmd == 'H':
                nx += ix
            else:
                nx += x
            out += coordsToStr(x, y, scale)
            out += coordsToStr(nx, y, scale)
            x = nx
            i += 2

        elif cmd in ['V', 'v']:
            ny = float(path[i+1])
            if cmd == 'V':
                ny += iy
            else:
                ny += y
            out += coordsToStr(x, y, scale)
            out += coordsToStr(x, ny, scale)
            y = ny
            i += 2

        elif cmd in ['Q', 'q']:
            out += 'b,'
            cx, cy = [float(n) for n in path[i+1].split(',')]
            ex, ey = [float(n) for n in path[i+2].split(',')]
            if cmd == 'Q':
                cx += ix
                cy += iy
                ex += ix
                ey += iy
            else:
                cx += x
                cy += y
                ex += x
                ey += y

            b = bezier((x, y), (cx, cy), (ex, ey))
            Xmin = min(Xmin, b.xmin)
            Xmax = max(Xmax, b.xmax)
            Ymin = min(Ymin, b.ymin)
            Ymax = max(Ymax, b.ymax)

            out += coordsToStr(x, y, scale)
            out += coordsToStr(cx, cy, scale)
            out += coordsToStr(ex, ey, scale)
            x, y = ex, ey
            i += 3

        elif cmd in ['C', 'c']:
            c1x, c1y = [float(n) for n in path[i+1].split(',')]
            c2x, c2y = [float(n) for n in path[i+2].split(',')]
            ex, ey = [float(n) for n in path[i+3].split(',')]
            if cmd == 'Q':
                c1x += ix
                c1y += iy
                c2x += ix
                c2y += iy
                ex += ix
                ey += iy
            else:
                c1x += x
                c1y += y
                c2x += x
                c2y += y
                ex += x
                ey += y

            curves = cubicToQuadratic(x, y, c1x, c1y, c2x, c2y, ex, ey, 2)
            for curve in curves:
                out += 'b,'
                out += coordsToStr(curve[0][0], curve[0][1], scale)
                out += coordsToStr(curve[1][0], curve[1][1], scale)
                out += coordsToStr(curve[2][0], curve[2][1], scale)
                b = bezier((curve[0][0], curve[0][1]), (curve[1][0], curve[1][1]), (curve[2][0], curve[2][1]))
                Xmin = min(Xmin, b.xmin)
                Xmax = max(Xmax, b.xmax)
                Ymin = min(Ymin, b.ymin)
                Ymax = max(Ymax, b.ymax)
            
            x, y = ex, ey
            i += 4

        elif cmd in ['Z', 'z']:
            if not (x == sx and y == sy):
                out += coordsToStr(x, y, scale)
                out += coordsToStr(sx, sy, scale)
            x, y = sx, sy
            i += 1

        Xmin = min(Xmin, x)
        Xmax = max(Xmax, x)
        Ymin = min(Ymin, y)
        Ymax = max(Ymax, y)

    Xmin /= scale
    Xmax /= scale
    Ymin, Ymax = (1 - Ymax) / scale, (1 - Ymin) / scale

    if len(out) > 0:
        out = out[0:-1]

        tokens = [attemptToNum(i) for i in out.split(',')]

        data = []
        i = 0
        while i < len(tokens):

            if tokens[i] == 'b':
                b = bezier((tokens[i+1], tokens[i+2]), (tokens[i+3], tokens[i+4]), (tokens[i+5], tokens[i+6]))
                if not(roundDec(b.x1) == roundDec(b.x2) == roundDec(b.x3)):
                    data.append(b)
                i += 7
            else:
                l = line((tokens[i], tokens[i+1]), (tokens[i+2], tokens[i+3]))
                if roundDec(l.width) != '0':
                    data.append(l)
                i += 4

    else:
        data = []

    return {
        'compact': out,
        'data': data,
        'Xmin': Xmin,
        'Xmax': Xmax,
        'Ymin': Ymin,
        'Ymax': Ymax
    }

def sortLines(data):

    if len(data) < 2:
        return data

    if len(data) == 2:
        if compare(data[0], data[1]) > 0:
            return data[::-1]
        else:
            return data[:]

    pivot = data[0]
    lower = []
    higher = []
    equal = []

    for i in range(1, len(data)):

        obj = data[i]
        diff = compare(obj, pivot)
        if diff < 0:
            lower.append(obj)
        elif diff > 0:
            higher.append(obj)
        elif diff == 0:
            equal.append(obj)

    # Inefficient, too lazy to optimize
    while len(equal) > 0:

        newItems = 0
        i = 0
        while i < len(equal):
            obj1 = equal[i]
            for obj2 in higher:
                if compare(obj1, obj2) > 0:
                    higher.append(obj1)
                    del equal[i]
                    newItems += 1
                    break
            else:
                i += 1

        if newItems == 0:
            break

    for obj in equal:
        lower.append(obj)

    return sortLines(lower) + [pivot] + sortLines(higher)

def sign(x):

    if x == 0:
        return 0
    if x < 0:
        return -1
    if x > 0:
        return 1

def testSort(data):

    length = len(data)
    for i in range(0, length - 1):
        for j in range(i + 1, length):
            obj1 = data[i]
            obj2 = data[j]

            if sign(compare(obj1, obj2)) != (-1 * sign(compare(obj2, obj1))):
                print("Comparison failure: {} {}".format(compare(obj1, obj2), compare(obj2, obj1)))

            if compare(obj1, obj2) > 0:
                print("Sorting failure: {}".format(compare(obj1, obj2)))

def processRawData(rawData, xOffset, string=True):

    data = []
    num = 0
    for item in rawData:
        if type(item) == line:
            if roundDec(item.width) != '0':
                data.append(item)
                num += 1
        else:
            expanded = item.simpleCurves()
            for b in expanded:
                if not(roundDec(b.x1) == roundDec(b.x2) == roundDec(b.x3)):
                    data.append(b)
                    num += 1
                else:
                    print('got here')

    '''
    data = sorted(data, key=lambda x: x.leftx)
    data = sorted(data, key=functools.cmp_to_key(compare))
    '''

    if len(data) > 1:
        data = sortLines(data)
        # testSort(data)

    if string:
        data = ''.join([i.string(xOffset) for i in data])

    return {'num': num, 'data': data}

def letterData(data):
    out = []
    left = 0
    while True:
        left = data.find(' d="', left)
        if left == -1:
            return out
        left += 4
        right = data.find('"', left)
        out.append(data[left:right])

if __name__ == '__main__':

    f = open('text.svg', 'r', encoding='utf-8')
    svg = f.read()
    f.close()

    f = open('width.txt', 'r', encoding='utf-8')
    widths = f.read()
    f.close()

    if len(widths) < 2:
        italics = False
    else:
        if input('Do you want to use character widths from width.txt? (Y/N) ') in ['y', 'Y', 'yes', 'Yes', 'YES']:
            italics = True
            data = widths.split('\n')[1:-1]
            widths = [float(line[3:line.find(' ', 3)]) for line in data]
        else:
            italics = False

    letters = []
    left = 0
    while True:
        left = svg.find('<g', left)
        if left == -1:
            break
        left += 2
        right = svg.find('</g>', left)

        letters.append(letterData(svg[left:right]))

    first = letters[0]
    line1 = pathRawData(first[0], 0, 0, 1)
    H = pathRawData(first[1], 0, 0, 1)
    line2 = pathRawData(first[2], 0, 0, 1)

    second = letters[1]
    line3 = pathRawData(second[0], 0, 0, 1)
    X = pathRawData(second[1], 0, 0, 1)
    line4 = pathRawData(second[2], 0, 0, 1)

    scale = H['Ymax'] - H['Ymin']
    xOffset = 0.6 * H['Xmin'] + 0.4 * X['Xmin']
    space = 0.6 * (line2['Xmin'] - H['Xmax']) / scale + 0.4 * (line4['Xmin'] - X['Xmax']) / scale

    out = '{' + input('Font name: ') + ':\n'

    chars = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$¢€£¥%^&*()-–—=≠[]\\;\'‘’,./_+{}|:"“”<≤≥>?`~×⋅÷±°′″'
    i = 0
    for l in letters[2:len(chars)+2]:
        
        c = chars[i]
        # print(c)

        if italics:
            width = widths[i]
        else:
            width = pathRawData(l[1 if len(l) == 2 else 2], 0, 0, scale)['Xmin'] - xOffset / scale - space

        width = roundDec(width)
        
        pathConverted = pathRawData(l[1], -1 * xOffset, 0, scale)

        renderXmin = roundDec(pathConverted['Xmin'])
        renderWidth = roundDec(float(roundDec(pathConverted['Xmax'])) - float(renderXmin))
        extremeYDist = roundDec(max(abs(float(roundDec(pathConverted['Ymin'])) - 0.25), abs(float(roundDec(pathConverted['Ymax'])) - 0.25)))
        Ymin = roundDec(pathConverted['Ymin'] - 0.25)
        Ymax = roundDec(pathConverted['Ymax'] - 0.25)
        processedData = processRawData(pathConverted['data'], float(renderXmin))
        num = processedData['num']

        if len(l) == 2:
            out += '|{} {} 0 0 0 0 0 0 |\n'.format(c, width)
        else:
            out += '|{} {} {} {} {} {} {} {} {}|\n'.format(c, width, renderXmin, renderWidth, extremeYDist, Ymin, Ymax, num, processedData['data'])

        i += 1

    out += '}'

    f = open('output.txt', 'w', encoding='utf-8')
    f.write(out)
    f.close()