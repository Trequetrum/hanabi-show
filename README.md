# hanabi-show

### About Hanabi Show

Hanabi Show is a platform for learning how to program by working with basic shapes/animations and hopefully learning to build up complex pictures and animations. To really shine, this would require a lot more polish and documentation. I'm sure some of this could be simplified too.

A beginner-level programming task might be to animate a sun that shoots out little rays, a robot waving to the user, or a firework show (the namesake of this repository). An intermediate animation might involve something that changes directions when it detects a colision (something like a bouncy-ball or rhoomba).

Currently, there's only one `Renderer` (*Tk*) implemented. TK may not be the best choice as it is designed with UI and not with animation in mind. You can't pre-render or update in chunks/batches. I used Tk because I figured I'd start with libraries that python advertises as standard (tkinter used to ship with python). Implementing a renderer (it's just a class) with Pyglet might be a good learning project (somewhere between beginner and intermediate difficulty, if I had to hazard a guess). Writing a renderer using Pyglet's Shapes and Graphics will considerably outperform tkinter.

The two classes worth noting are `Animation` and `Picture`. If you subclass `Animation`, the renderer can render it for you. If you subclass `Picture`, then `AnimationBuilder` should be able to animate any attributes of the new class (and because `AnimationBuilder` is an `Animation`), the rest comes for free again.

See `main.py` and examples.py for some examples! 

### Some Technical Details

Written with python3.10.1 and Tcl/Tk

I don't know Python well enough to know to which extent this is backward compatable.

Tk is a graphical user interface toolkit that can run unchanged across Windows, Mac OS X, Linux, etc. To develop with it, however, you need some form of the distribution downloaded. [Link](https://www.tcl.tk/software/tcltk/)


### If your OS Maintains compatibility with the Ubuntu repositories

With your terminal's current working directory (CWD) in the root folder of this project, the following commands should set up and run this project

- `sudo apt update && sudo apt upgrade -y`
- `sudo add-apt-repository ppa:deadsnakes/ppa`
- `sudo apt install python3.10`
- `sudo apt install python3.10-venv`
- `sudo apt-get install python3.10-tk`
- `python3.10 -m venv .venv`
- `source .venv/bin/activate`
- `python -m pip install --upgrade pip`
- `python -m pip install -r requirements.txt`
- `python main.py`

### Update requirements.txt

- `python -m pip freeze > requirements.txt`
