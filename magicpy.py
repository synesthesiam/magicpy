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

import numpy, argparse
from PIL import Image

def gen_pattern(width, height):
    return numpy.random.randint(0, 256, (width, height))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = "Autostereogram (MagicEye) generator")
    parser.add_argument("depthmap", type=str,
            help = "Path to grayscale depth-map (white = close)")

    parser.add_argument("-o", "--output", type=str, default="output.png",
            help="Path to write output image")

    parser.add_argument("-p", "--pattern-div", type=int, default=8,
            help = "Width of generated pattern (width n means 1/n of depth-map width)")

    parser.add_argument("-i", "--invert", action="store_true", help = "Invert depthmap (white = far)")

    args = parser.parse_args()
    invert = -1 if args.invert else 1

    depth_map = Image.open(args.depthmap).convert("RGB")
    depth_data = depth_map.load()

    out_img = Image.new("L", depth_map.size)
    out_data = out_img.load()

    pattern_width = depth_map.size[0] / args.pattern_div
    pattern = gen_pattern(pattern_width, depth_map.size[1])

    # Create stereogram
    for x in xrange(0, depth_map.size[0]):
        for y in xrange(0, depth_map.size[1]):

            if x < pattern_width:
                out_data[x, y] = pattern[x, y]  # Use generated pattern
            else:
                shift = depth_data[x, y][0] / args.pattern_div  # 255 is closest
                out_data[x, y] = out_data[x - pattern_width + (shift * invert), y]

    out_img.save(args.output)

