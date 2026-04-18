# RAW SYNC
### Hey there, you're here so I'm guessing you're curious about the code (or the abundance of bananas 🍌)!
This is my first public python project, so here goes
## How to Use this
You can run it normally as well, the code will prompt you and guide you through the process :)
 Available Flags:
--src: Path to your SD card or source folder.

--dst: Path to your laptop's organized folder.

--dry: Simulation mode. See what would happen without moving files.

--folder: Custom name for the RAW subfolder (Default: raws).

--d_ext: Custom destination extensions (e.g., --d_ext jpg png).

--s_ext: Custom source extensions (e.g., --s_ext nef arw).
## What is this?
Raw Sync is basically a simple to use CLI (Command Line Interface) which I created to import corresponding RAW files after loooong editing sessions. For example when you have more than 30 edited images on your laptop, manually finding the corresponding RAW files can be an arduous and time taking process. This tool automates it by cross-checking names of images without extensions and copying the raw files to your laptop.
## Installation
git clone https://github.com/MonkeyWithaLaptop/RawHeist.git
## Requirements
No dependencies needed! Just Python 3.6+.
## Why this Exists

This project began on a dreary evening, tired from the day I sat down to edit some more images.

As I imported more files my eyes went to my latest folder - 54 .af files. 
Some of these shots were genuine bangers I'd want to keep for contests. 
Then I checke the RAW files in the folder - 0.

I groaned in despair as it dawned on me, combing through 1000s of different images in my sd card finding and matching all of the raw counterparts to my edited files would be a pain. 

30 minutes minimum.

'Wish there were a script for this' I said to myself.

'Maybe there is one!' My inner voice chimed, but my searches bore no fruit,

'Someone should really make one' I groaned once more

'You're a CSE student, why don't you do it?' 

And thus my inner voice landed on something solid, a project worth making, not for others, but for my own lazy ass.

So, Ladies and Gentelemen, remember this script was made in 6 hours because i wanted to avoid 30 minutes of hard labour! And if I'm completely honest, I don't know how the math checks out.
