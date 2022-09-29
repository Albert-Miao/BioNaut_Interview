# BioNaut_Interview

generate_ball.py : Generate a video of bouncing balls given the following parameters
    
    Ball parameters:
    --color: Provide a color in BGR.
    --starting_height: Height of starting position in pixels.
    --radius: Radius of ball.
    --deformation: Constant from 0 to 1 to determine how much the ball deforms on impact.
    --additional_ball: Include an additional ball after running this command. Accepts all Ball parameters.

    Video parameters:
    --count_frames: Judge duration by frames rather than number of bounces.
    --duration: Number of bounces or number of frames.
    --acceleration: Accleration of balls in px/s**2.
    --resolution: Resolution of the target video.
    --fps: Frames per second.
    --output_dir: Output directory to output videos to.
    --title: Title of the video.
    --background_color: Color of the background.

track_ball.py : Given a video, track the bouncing balls.

    Parameters:
    --path: Path to video to read.
    --tolerance: What colors to consider part of the same entity.
    --background_color: background color of the video.
    --output_dir: Output directory.
    --save_name: Name to save tracking video under.

To answer development questions, I've recorded my thoughts on the wiki section of this Github repo. Large picture:

The generate_ball code creates every ball submitted in the arguments with the Ball class, which records the position, 
velocity, deformation, and the color of a given ball. Each ball is stored under BallManager, which simulates the 
physics of each ball every time the nextFrame method is called. Finally, the information of BallManager is passed to 
the ScreenWriter class in order to save each frame as part of the video.

The track_ball code doesn't rely on any classes since it's mostly for visualization. We include a helper method 
detect_distinct_contours to find each shape created by a unique color in the image. Making this run quickly is 
difficult, but we shortcut most of the work by including a standard background for the videos, so that the code only has 
to run on the actually colored objects by filtering out the background.

I made a couple of physics assumptions, with reasoning:
1) There is no energy loss throughout the video. This means that:
   1) Horizontal velocity is constant, as to make predicting the horizontal scale easier.
   2) Deformation releases no energy into the ground, meaning impact speed is reversed exactly on bounce.
2) During deformation, acceleration on the ball upwards is constant. Removes the need for a third position derivative.
3) The major axis * the minor axis will be the same value throughout, which roughly preserves the volume of the solid.

Major failure case is providing the tracking a purposefully confusing video, such as giving it balls of the same color
or providing incorrect background information. Other than that, asserts have been placed to avoid incorrect parameters.