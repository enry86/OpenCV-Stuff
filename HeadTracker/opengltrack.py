#!/usr/bin/python

from pyglet.gl import *
from math import sin,cos,tan
import pyglet
import ocvtrack
import cube
import sys

cx = 0.0
ratio = 0.0
tracker = None
track = True
cubes = list()

def init():
    #OpenGL initialization
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.01, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glEnable(GL_NORMALIZE)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    # Define a simple function to create ctypes arrays of floats:
    def vec(*args):
        return (GLfloat * len(args))(*args)

    #Adding some light to the scene
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, vec(0.3,0.3,0.3,1));
    glLightfv(GL_LIGHT0, GL_POSITION, vec(1, 1, 0, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(0.9, 0.9, 0.9, 1))
    glLightfv(GL_LIGHT1, GL_POSITION, vec(0, 1, -1.5, 0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(.5, .5, .5, 1))


def setPerspective ():
    global ratio, cx, tracker, track
    emph_factor = 1
    fov = 1.5
    near = 0.1

    #Acquire head position
    if track:
        hx,hy = tracker.getLastFace()
        hx *= emph_factor
        hy *= emph_factor
    else:
        hx,hy = (0,0)

    #Setting the frustum of the camera
    top = near * tan(fov/2)
    right =  top
    left = -right
    bottom = -top

    top += (hy) * near
    bottom += (hy) * near
    left += (hx) * near
    right += (hx) * near

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(left, right, bottom, top, near, 10000.)
    glTranslatef(hx, hy ,0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def on_resize (width, height):
    global ratio
    ratio = float(width) / float(height)

    glViewport(0, 0, width, height)

    setPerspective()
    return pyglet.event.EVENT_HANDLED

def on_draw ():
    global cubes
    depth = 2
    setPerspective()
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glColor3f (1,1,1)
    glTranslatef(0,0,-1)
    glBegin(GL_LINES)
    glVertex3f (-1.0, -1.0, -depth)
    glVertex3f (-1.0, -1.0, 0.0)
    glVertex3f (1.0, 1.0, -depth)
    glVertex3f (1.0, 1.0, 0.0)
    glVertex3f (1.0, -1.0, -depth)
    glVertex3f (1.0, -1.0, 0.0)
    glVertex3f (-1.0, 1.0, -depth)
    glVertex3f (-1.0, 1.0, 0.0)

    #drawing the grid
    for z in range(depth + 1):
        glVertex3f (-1.0, -1.0, -z)
        glVertex3f (-1.0, 1.0, -z)
        glVertex3f (-1.0, 1.0, -z)
        glVertex3f (1.0, 1.0, -z)
        glVertex3f (1.0, 1.0, -z)
        glVertex3f (1.0, -1.0, -z)
        glVertex3f (1.0, -1.0, -z)
        glVertex3f (-1.0, -1.0, -z)
    glEnd()
    glBegin(GL_TRIANGLES)
    glVertex3f (0.0, 0.5, -2.0)
    glVertex3f (-0.5, -0.5, -2.0)
    glVertex3f (0.5, -0.5, -2.0)
    glEnd ()

    #draw cubes on the scene
    for c in cubes:
        c.draw()

def main(track):
    global tracker,cubes

    #Instantiate FaceTracker
    if track:
        tracker = ocvtrack.FaceTracker()
        tracker.start()

    cubes.append (cube.Cube([-0.25, -1, -1],[0.5, 0.1, 0.3],[0.9, 0.3, 0.3]))
    cubes.append (cube.Cube([-0.8, -0.5, -1.8],[0.3, 0.1, 2],[0.9, 0.3, 0.5]))
    cubes.append (cube.Cube([0.3, 0.1, -1],[0.2, 0.2, 0.2],[0.1, 0.9, 1]))

    try:
        # Try and create a window with multisampling (antialiasing)
        config = Config(sample_buffers=1, samples=4,
                    depth_size=16, double_buffer=True,)
        win = pyglet.window.Window(resizable=True, config=config)
    except pyglet.window.NoSuchConfigException:
        # Fall back to no multisampling for old hardware
        win = pyglet.window.Window(resizable=True)

    win.on_resize=on_resize
    init()

    win.set_visible()
    clock=pyglet.clock.Clock()

    #update loop
    while not win.has_exit:
        win.dispatch_events()

        on_draw()

        win.flip()
        clock.tick()
    tracker.stop()



if __name__ == '__main__':
    opt = ''
    if len(sys.argv) == 2:
        opt = sys.argv[1]
    if opt == '-t':
        track = False
    main(track)
