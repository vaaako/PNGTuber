# PNGTuber

# About
The PNGTuber is designed to change frames dynamically based
 on the audio input from a microphone

I made for fun and because just this funcionality is enough for me

![showcase](media/showcase.png)

# How to use
## Install the requirements
```bash
pip install -r requirements.txt # You may have to use "pip3" instead

# OR

python3 -m pip install -r requirements.txt
```

## Running
```sh
python3 main.py [limit=40] # Optional argument, default value = 40
```

- `limit` - The pitch change threshold for frame shifts. You can adjust the limit value based on your preferences (**Recommended:** *30-50*)

>You may want to change Window **title** and **size** in the code

### Controls
- `LMB` - Move the window
- `RMB` - Close the window



# Credits
The default PNGs are from [this itch.io page](https://vtuber-studio-dev.itch.io/pngtuber-avatar-cute-frog)