magicpy
=======
An autostereogram (MagicEye) image generator written in Python.

Description
-----------
Takes a grayscale depthmap (where white is closest, black is farthest), and generates a [random dot autostereogram](http://en.wikipedia.org/wiki/Autostereogram) (MagicEye) image of the same size.

By default, a random pattern 1/8 the size of the depthmap is repeated and offset to create the effect. There seems to be an art to choosing the right pattern size.

If you string together multiple stereograms, you can make [cool "MagicEye" movies!](http://synesthesiam.com/code.php#stereograms)

Examples
--------
    # Use default settings (1/8 sized pattern)
    $ python magicpy.py shark.png -o magic-shark.png

    # Make random pattern 1/10 of the depthmap size
    $ python magicpy.py -p 10 shark.png -o magic-shark.png

![shark.png](synesthesiam.github.com/magicpy/shark.png)
![magic-shark.png](synesthesiam.github.com/magicpy/magicshark.png)


glmagic
=======
An OpenGL-based depth map generator (used to make frames for a stereogram movie).

Description
-----------
Renders frames from an OpenGL scene to a series of depthmaps that can be converted and combined into a stereogram movie.
