# utils/sprite.py
import streamlit as st
import io
from PIL import Image
import base64

def extract_sprite(sprite_sheet_path, row_num=1, sprite_width=80, sprite_height=90) -> list:
    """
    Extract sprites from a sprite sheet. 
    The x_offset is 64 pixels.
    The y_offset is  pixels.
    Arguments:
    - sprite_sheet_path (str): The path to the sprite sheet.
    - row_num (int): The row number of the sprite (1-based).
    - sprite_width (int): The width of the sprite.
    - sprite_height (int): The height of the sprite.
    Returns:
    - list: A list of sprites.
    """
    # constants
    x_offset = 60
    x_padding = 112
    y_offset = 40
    # y_padding = 112

    # Open the sprite sheet
    sprite_sheet = Image.open(sprite_sheet_path)
    
    left = x_offset + col * (sprite_width + x_padding)
    top = y_offset
    right = left + sprite_width
    bottom = top + sprite_height
        
    frame = sprite_sheet.crop((left, top, right, bottom))
    
    return frame

def extract_sprites(sprite_sheet_path, row_num=1, sprite_width=80, sprite_height=90) -> list:
    """
    Extract sprites from a sprite sheet. 
    The x_offset is 64 pixels.
    The y_offset is  pixels.
    Arguments:
    - sprite_sheet_path (str): The path to the sprite sheet.
    - row_num (int): The row number of the sprite (1-based).
    - sprite_width (int): The width of the sprite.
    - sprite_height (int): The height of the sprite.
    Returns:
    - list: A list of sprites.
    """
    # constants
    x_offset = 60
    x_padding = 112
    y_offset = 40
    # y_padding = 112

    # Open the sprite sheet
    sprite_sheet = Image.open(sprite_sheet_path)
    
    # Extract first row sprites
    frames = []
    for col in range(6): # 6
        left = x_offset + col * (sprite_width + x_padding)
        top = y_offset
        right = left + sprite_width
        bottom = top + sprite_height
        
        frame = sprite_sheet.crop((left, top, right, bottom))
        frames.append(frame)
    
    return frames

def animate_sprite(frames, delay=100):
    """
    Create an animated GIF from sprite frames.
    
    :param frames: List of PIL Image frames
    :param delay: Delay between frames in milliseconds
    :return: Animated GIF bytes
    """
    # Save frames as animated GIF
    byte_io = io.BytesIO()
    frames[0].save(
        byte_io, 
        format='GIF', 
        save_all=True, 
        append_images=frames[1:], 
        duration=delay, 
        loop=0
    )
    return byte_io

def add_character_sprite(sprite_sheet_path, position='bottom-right', width=100):
    frames = extract_sprites(sprite_sheet_path, row_num=1)

    gif_bytes = animate_sprite(frames)
    # Encode the GIF bytes to base64
    encoded_string = base64.b64encode(gif_bytes.getvalue()).decode()
    
    sprite_css = f"""
    <style>
    .character-sprite {{
        position: fixed;
        {_position_css(position)};
        z-index: 1000;
        width: {width}px;
        transition: transform 0.3s ease;
    }}
    .character-sprite:hover {{
        transform: scale(1.1);
    }}
    </style>
    <img src="data:image/gif;base64,{encoded_string}" 
         alt="Character Sprite" 
         class="character-sprite">
    """
    
    st.markdown(sprite_css, unsafe_allow_html=True)

def _position_css(position):
    positions = {
        'bottom-right': 'bottom: 20px; right: 20px;',
        'bottom-left': 'bottom: 20px; left: 20px;',
        'top-right': 'top: 20px; right: 20px;',
        'top-left': 'top: 20px; left: 20px;'
    }
    return positions.get(position, positions['bottom-right'])

def display_character_with_progress(sprite_sheet_path, exp_percentage, life_percentage, level, position='bottom-right'):
    
    frames = extract_sprites(sprite_sheet_path, row_num=1)
    
    gif_bytes = animate_sprite(frames)
    encoded_string = base64.b64encode(gif_bytes.getvalue()).decode()

    html = f"""
    <style>
        .container {{
            position: fixed;
            {_position_css(position)};
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 180px;  /* Same width as the avatar circle */
            text-align: center;
        }}
        .circle-container {{
            display: flex;
            width: 180px;  /* Larger than the image */
            height: 180px;  /* Larger than the image */
            border-radius: 50%;
            overflow: hidden;
            background-color: #f0f0f0;
            background: conic-gradient(#00A36C 0%, #00A36C {life_percentage}%, white {life_percentage}%, white 100% );
            justify-content: center;
            align-items: center;
        }}

        .avatar-container {{
            position: relative;
            width: 160px;
            height: 160px;
            border-radius: 50%;
            overflow: hidden;
            background-color: #f0f0f0;
        }}
        
        .circle-img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .life-percentage {{
            margin-top: 5px;
            font-size: 14px;
            color: #333;
            font-weight: bold;
        }}

        .exp-bar-container {{
            width: 180px;  /* Same width as the avatar circle */
            height: 10px;
            background-color: #e0e0e0;
            border-radius: 5px;
            margin-top: 10px;
        }}

        .exp-bar {{
            height: 100%;
            width: {exp_percentage}%;
            background-color: #ffc000;
            border-radius: 5px;
        }}

        .stats-text {{
            font-size: 16px;
            color: black;
            font-weight: bold;
        }}

        
    </style>
    
    <div class="container">
    <div class="circle-container">
        <div class="avatar-container">
            <img src="data:image/png;base64,{encoded_string}" class="circle-img">
        </div>
    </div>
    <div class="stats-text">
        <p>HP: {int(life_percentage)}%</p>
    </div>
    <div class="exp-bar-container">
        <div class="exp-bar"></div>
    </div>
    <div class="stats-text">
        <p>Level: {level} | EXP: {int(exp_percentage)}%</p>
    </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)