from PIL import Image
import pyexiv2


def resize_image(src_path, dst_path, size):
    # resize image
    image = Image.open(src_path)
    width, length = size
    if image.size[0] < image.size[1]:
        width, length = length, width
    image.thumbnail((width, length), Image.ANTIALIAS)
    image.save(dst_path, "JPEG")

    # copy EXIF data
    src_meta = pyexiv2.ImageMetadata(src_path)
    src_meta.read()
    dst_meta = pyexiv2.ImageMetadata(dst_path)
    dst_meta.read()
    src_meta.copy(dst_meta)

    # set EXIF image size info to resized size
    dst_meta["Exif.Photo.PixelXDimension"].value = image.size[0]
    dst_meta["Exif.Photo.PixelYDimension"].value = image.size[1]
    dst_meta.write()


def batch_resize(src_dir, dst_dir, size):
    import os
    from os.path import join, splitext, exists

    if not exists(dst_dir):
        os.mkdir(dst_dir)
    for root, dirs, files in os.walk(src_dir):
        for fname in files:
            base, ext = splitext(fname)
            if ext.lower() == '.jpg':
                src_path = join(root, fname)
                dst_path = join(dst_dir, fname)
                print src_path, '==>', dst_path
                resize_image(src_path, dst_path, size)


def options():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='src_dir',
                      help="source directoy")
    parser.add_option('-o', '--output', dest='dst_dir',
                      help="destinate directoy")
    parser.add_option('-s', '--size', dest='size',
                      help="resized of images in pixels")

    opts, args = parser.parse_args()
    if opts.src_dir and opts.dst_dir and opts.size:
        return {
            'src_dir': opts.src_dir,
            'dst_dir': opts.dst_dir,
            'size': int(opts.size),
        }
    else:
        parser.print_help()
        exit()


if __name__ == "__main__":
    opt = options()
    src_dir = opt.get('src_dir')
    dst_dir = opt.get('dst_dir')
    size = opt.get('size')
    batch_resize(src_dir, dst_dir, (size, size))
