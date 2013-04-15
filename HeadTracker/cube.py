#!/usr/bin/python

from pyglet.gl import *

class Cube:
    def __init__(self, pos, size, col):
        self.col = col
        self.pos = pos
        self.size = size
        self.verts = list ()
        self.norms = list ()

        self.norms.append ([0,0,1])
        self.verts.append ([pos[0], pos[1], pos[2]])
        self.verts.append ([pos[0] + size[0], pos[1], pos[2]])
        self.verts.append ([pos[0] + size[0], pos[1] + size[1], pos[2]])
        self.verts.append ([pos[0], pos[1] + size[1], pos[2]])

        self.norms.append ([0,0,-1])
        self.verts.append ([pos[0], pos[1], pos[2] + size[2]])
        self.verts.append ([pos[0] + size[0], pos[1], pos[2] + size[2]])
        self.verts.append ([pos[0] + size[0], pos[1] + size[1], pos[2] + size[2]])
        self.verts.append ([pos[0], pos[1] + size[1], pos[2] + size[2]])

        self.norms.append ([-1,0,0])
        self.verts.append ([pos[0], pos[1], pos[2]])
        self.verts.append ([pos[0], pos[1], pos[2] + size[2]])
        self.verts.append ([pos[0], pos[1] + size[1], pos[2] + size[2]])
        self.verts.append ([pos[0], pos[1] + size[1], pos[2]])

        self.norms.append ([1,0,0])
        self.verts.append ([pos[0] + size[0], pos[1], pos[2]])
        self.verts.append ([pos[0] + size[0], pos[1], pos[2] + size[2]])
        self.verts.append ([pos[0] + size[0], pos[1] + size[1], pos[2] + size[2]])
        self.verts.append ([pos[0] + size[0], pos[1] + size[1], pos[2]])

        self.norms.append ([0,-1,0])
        self.verts.append ([pos[0], pos[1], pos[2]])
        self.verts.append ([pos[0] + size[0], pos[1], pos[2]])
        self.verts.append ([pos[0] + size[0], pos[1], pos[2] + size[2]])
        self.verts.append ([pos[0], pos[1], pos[2] + size[2]])

        self.norms.append ([0,1,0])
        self.verts.append ([pos[0], pos[1] + size[1], pos[2]])
        self.verts.append ([pos[0] + size[0], pos[1] + size[1], pos[2]])
        self.verts.append ([pos[0] + size[0], pos[1] + size[1], pos[2] + size[2]])
        self.verts.append ([pos[0], pos[1] + size[1], pos[2] + size[2]])


    def draw(self):
        glPushMatrix()
        glColor3f(self.col[0], self.col[1], self.col[2])
        glBegin(GL_QUADS)
        vertex = 0
        face = 0
        for v in self.verts:
            if vertex % 4 == 0:
                n = self.norms[face]
                glNormal3f (n[0], n[1], n[2])
                face += 1
            glVertex3f(v[0], v[1], v[2])
            vertex += 1
        glEnd()
        glPopMatrix()
