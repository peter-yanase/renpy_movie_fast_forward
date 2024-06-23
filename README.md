# renpy_movie_fast_forward

A script that enables fast forwarding full screen movies in Ren'Py

## How to Use

1. Install OpenCV by running `pip install opencv-python`.
2. Create the `videos` folder inside your `game` folder.
3. Dump all your videos inside `videos`.
4. Copy `renpy_movie_fast_forward.py` into your game folder.
5. Run `renpy_movie_fast_forward.py`.

(You can delete `renpy_movie_fast_forward.py` after it finished generating `fast_forward.rpy` as it will not be used anymore.)

Example usage inside your script:

```
$ff_cutscene("my_video.webm")  # You can call a cut-scene like this

call my_video_ff   # Or like this
```

This software will only work if:

- You do not use periods in your file names.
- All your video files are in the same format.
