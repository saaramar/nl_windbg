# nl_windbg

nl_windbg is a very basic library that implements some functionalities for Windows kerel debugging.
It helps you look at the Nonpaged Pool memory managments stuctures (lookasides, freelists, bitmap),
examine pool shapes, set convenient traces on functions, and execute shellcodes.

## Usage
![alt text](https://github.com/saaramar/nl_windbg/raw/master/basic_example.png "")

nl_windbg use pykd as base interface. For that, you'll have to setup pykd on your host.
The usage is simple:

```kd> .load pykd.pyd```

```kd> !pycmd```

```>>> from nl_windbg import *```

## NOTE

I implemented a little chunks, pte and pde parsering, although of course I personally use
!pool, !pte, etc. It was just on the way.