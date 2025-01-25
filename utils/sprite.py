# utils/sprite.py
import streamlit as st
import io
from PIL import Image
import base64

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
    for col in range(6):
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