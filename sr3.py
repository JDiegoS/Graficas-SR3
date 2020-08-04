#Juan Diego Solorzano 18151
#SR3

import struct
from objt import Obj

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(c):
    return struct.pack('=h', c)

def dword(c):
    return struct.pack('=l', c)

def glCreateWindow(width, height):
        win = Render(width, height)
        return win

class Render(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clearC = bytes([0, 0, 0])
        self.color = bytes([255, 255, 255])
        self.xw = 0
        self.yw = 0
        self.widthw = width
        self.heightw = height
        self.framebuffer = []
        self.poin = True
        self.rangem = False
        self.glClear()

    def glInit(self, width, height):
        return
    
    #Area para pintar
    def glViewPort(self, x, y, width, height):
        self.xw = x
        self.yw = y
        self.widthw = width
        self.heightw = height

    #Pintar imagen   
    def glClear(self):
        self.framebuffer = [
            [self.clearC for x in range(self.width)]
            for y in range(self.height)
        ]

    #Color para pintar imagen
    def glClearColor(self, r, g, b):
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        self.clearC = bytes([b, g, r])
        self.glClear()

    #Crear archivo de la imagen
    def glFinish(self, filename):
        f = open(filename, 'bw')

        # File header (14 bytes)
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # Image header (40 bytes)
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # Pixel data (width x height x 3 pixels)
        for x in range(self.height):
          for y in range(self.width):
            f.write(self.framebuffer[x][y])

        f.close()

    #Pintar punto
    def glVertex(self, x, y):
        #Modificar si se tienen valores entre -1 y 1
        if self.poin:
            xn = (x + 1)*(self.widthw/2) + self.xw
            yn = (y + 1)*(self.heightw/2) + self.yw
            xn = int(xn)
            yn = int(yn)
        else:
            xn = x
            yn = y

        try:
            self.framebuffer[yn][xn] = self.color
        except:
            pass

    #Color del punto
    def glColor(self, r, g, b):
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        self.color = bytes([b, g, r])

    #Pintar una linea de un punto a otro. Se optimizo el algoritmo evitando el uso de round y divisiones
    def glLine(self, x1, y1, x2, y2):
        #Cambiar valores
        self.poin = False

        #Modificar si se pidieron valores entre -1 y 1
        if self.rangem:
            x1n = int((x1 + 1)*(self.width/2))
            x2n = int((x2 + 1)*(self.width/2))
            y1n = int((y1 + 1)*(self.height/2))
            y2n = int((y2 + 1)*(self.height/2))

        else:
            
            x1n = x1
            y1n = y1
            x2n = x2
            y2n = y2
            

        dy = abs(y2n - y1n)
        dx = abs(x2n - x1n)
        emp = dy > dx

        if emp:
            x1n, y1n = y1n, x1n
            x2n, y2n = y2n, x2n

        if x1n > x2n:
            x1n, x2n = x2n, x1n
            y1n, y2n = y2n, y1n

        dy = abs(y2n - y1n)
        dx = abs(x2n - x1n)
        #Variable para ver cuando subir de y
        offset = 0
        threshold = dx
        y = y1n
        #Pintar puntos
        for x in range(x1n, x2n + 1):
            if emp:
                self.glVertex(y, x)
            else:
                self.glVertex(x, y)

            offset += dy * 2
            if offset >= threshold:
                #Sumar si linea va para arriba, restar si va para abajo
                y += 1 if y1n < y2n else -1
                threshold += 2 * dx

    def load(self, filename, translate, scale):
        model = Obj(filename)
        
        for face in model.faces:
            #Cuantas caras tiene el modelo
            vcount = len(face)
            
            for j in range(vcount):
                vi1 = face[j][0]
                vi2 = face[(j + 1) % vcount][0]

                v1 = model.vertices[vi1 - 1]
                v2 = model.vertices[vi2 - 1]

                #Solo acepta enteros. Sumar el translate y multiplicar por scale para ajustar al display
                x1 = round((v1[0] + translate[0]) * scale[0])
                y1 = round((v1[1] + translate[1]) * scale[1])
                x2 = round((v2[0] + translate[0]) * scale[0])
                y2 = round((v2[1] + translate[1]) * scale[1])
                self.glLine(x1, y1, x2, y2)

bitmap = Render(800, 600)
bitmap.load('Mario.obj', translate=[5, 2], scale=[80, 80])
bitmap.glFinish('out2.bmp')

