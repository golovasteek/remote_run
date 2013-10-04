""" Small easter egg: communicate with user using -qqq option.
Try `rr -qqq`, `rr -qqqq` etc. 
(like `aptitude -vvv moo`)
"""

import zlib
import base64
import sys

img1 = (b'eNp1UjtuwzAM3XWKBy6OAUnc4xsUPYIAaerQpRcgcvbyI8dOjMgIGT2+R1AkgZfDgg+HJb0'
       b'hgna69Q77nIotnXAHm5N7LVQI40F6G1TKouTgamhRR1Rqb+r0f+1Z3QZqyqy9MpQ7eZ7TEJ'
       b'UUIspYgQdZVYmRC+py1JbdKjD+qiXEmho2ntHl8tbNHpEgO2OnzOa0iWhH+GjG+XxVe2A2C'
       b'j3BOw65VXdXUa7oaxK8pomsP3aTUYr1KaF1nBKEYXT2OvRqjbM2Woqb/n55Q1k4BVdAHLjF'
       b'2TsSE5UIg821zszxetexW6e0qCsiEJlTFRfLnm0GYt4e2AVzWaR7W2XSv59L5EI1gQ/ax+J'
       b'Cae/bd9Pxq3bUy1rqGjY36TJYmib9A8UbhDY=')

img2 = (b'eNptk8GOhCAMhu8+ReOlkEi5M/E19kTSZrOPQebZ9y+jDDqjEaT9/FtKJZqvDY8kXnl/qK+'
        b'Wi5daFU5PS2LJHrndvFWMWPiZ+pxv3lBtU90Tq26c4+xVhEwS6K9q/qXYV/oGMsOCmZFaS'
        b'kL9HUHqMgBkzRT2HkejT3tEDkQDejHYH7JXBOwDbNtMhT6Km+jnEMf86FK44oS1UlxsO8Q'
        b'2FyulTZi/52ZFroUgKdyq+weWMXxwhalZnbDWI98wQRaxeycM3E0OYpE+MKpXOYhl+oJRn'
        b'eWQf6YLFo/KoZAn6BDT6R11s6iHDaACOr7UYKNu1Y/aT1F4ys3Ez5aAnZ3lHLDcj2w1s7U'
        b'fUwU2UWTwdTgMreglJ/DmkKq+g9i5T3TBCA9iIXQ1AFvXlZlTslefIRgWsMBunZAlqN9oD'
        b'EHD4mey9yawQgsLGkaj38s/PTGd4Q==')

def show(img):
    print(zlib.decompress(base64.b64decode(img)).decode('ascii'), file=sys.stderr)

def many_q(count):
    if count == 3:
        print('Tsss...', file=sys.stderr)
    elif count == 4:
        print('Qu-qu!', file=sys.stderr)
    elif count == 5:
        print('Why do you thing I shall be so quiet?', file=sys.stderr)
    elif count == 6:
        print('Moooo!\n', file=sys.stderr)
        show(img1)
    elif count in (7, 8, 9):
        print('Ok, stop it.', file=sys.stderr)
    else:
        print('Boooo!\n', file=sys.stderr)
        show(img2)
    exit(1)
