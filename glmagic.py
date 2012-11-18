#!/usr/bin/python

# Copyright (C) 2012 Michael Hansen (mihansen@indiana.edu)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse, math, numpy as np
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLUT import *

snap_index = 1
angle = 0.0

def save_snapshot(args, index, format_str):
    # Grab depth buffer (grayscale)
    pixel_str = glReadPixels(0, 0, args.width, args.height, GL_DEPTH_COMPONENT, GL_UNSIGNED_BYTE)
    depth = Image.fromstring("L", (args.width, args.height), pixel_str)
    data = np.array(depth)

    # Normalize and invert (make white closest)
    data = 255 - ((data - data.min()) * (255/data.max()))
            
    # Save to image file
    depth = Image.fromarray(data, mode="L")
    depth.save(format_str.format(args.prefix, index, args.extension))

def render(args, window, format_str):
    global snap_index, angle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # ===== Render a teapot =====
    glRotate(angle, 1, 1, 1)
    glutSolidTeapot(0.5)
    # ===========================

    glutSwapBuffers()

    if args.snapshots > 0:
        # Save snapshot and advance frame
        save_snapshot(args, snap_index, format_str)
        angle = (angle + args.rotation) % 360
        args.snapshots -= 1
        snap_index += 1
        glutPostRedisplay()
    else:
        glutDestroyWindow(window)


if __name__ == "__main__":

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description = "OpenGL autostereogram (MagicEye) generator")
    parser.add_argument("-s", "--snapshots", type=int, default=36,
            help="Number of snapshots to take")

    parser.add_argument("-r", "--rotation", type=float, default=10.0,
            help="Amount to increase rotation angle by after each shot")

    parser.add_argument("-p", "--prefix", type=str, default="snapshot_",
            help="Prefix for generated stereogram images")

    parser.add_argument("-e", "--extension", type=str, default="png",
            help="File extension for generated stereogram images")

    parser.add_argument("--width", type=int, default=800,
            help="Width of window and output image")

    parser.add_argument("--height", type=int, default=600,
            help="Height of window and output image")

    args = parser.parse_args()

    # Set up GLUT
    glutInit([])
    glutInitWindowSize(args.width, args.height)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    window = glutCreateWindow("glMagic")

    # Format string for snapshot images
    num_zeros = int(math.ceil(math.log10(args.snapshots)))
    format_str = "{{0}}{{1:0{0}d}}.{{2}}".format(num_zeros)

    display = lambda: render(args, window, format_str)
    glutDisplayFunc(display)

    # Set up OpenGL
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    # Make it pretty to look at
    glClearDepth(1.0)
    glShadeModel(GL_SMOOTH)  
    glMatrixMode(GL_PROJECTION)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glMaterialfv(GL_FRONT, GL_AMBIENT, (1, 1, 0, 0))
    glLight(GL_LIGHT0, GL_POSITION, (1, 1, 1, 0))

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glDepthRange(0, 5)

    glutMainLoop()
