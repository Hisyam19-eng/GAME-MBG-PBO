"""
Image loading utility functions
Demonstrates: Reusability, DRY (Don't Repeat Yourself) principle
"""
import pygame
import os


def get_assets_path(*paths):
    """
    Get absolute path to assets folder with optional subdirectories
    
    Args:
        *paths: Variable number of path components (e.g., 'images', 'backgrounds', 'home.png')
    
    Returns:
        str: Absolute path to the asset
    """
    # Get src directory (where this file is located)
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Go up one level to project root, then into assets
    assets_dir = os.path.join(os.path.dirname(current_dir), 'assets')
    
    # Join with any additional paths provided
    return os.path.join(assets_dir, *paths) if paths else assets_dir


def load_image(image_path, convert_alpha=True, scale=None, fallback_color=None):
    """
    Load an image with optional scaling and fallback
    
    Args:
        image_path: Path to image file (can be relative to assets or absolute)
        convert_alpha: Whether to convert image with alpha channel (default True)
        scale: Optional tuple (width, height) to scale image to
        fallback_color: Optional RGB tuple for fallback colored surface if load fails
    
    Returns:
        pygame.Surface: Loaded (and optionally scaled) image, or fallback surface
    
    Raises:
        Exception: If image fails to load and no fallback_color is provided
    """
    try:
        # Load image
        if convert_alpha:
            image = pygame.image.load(image_path).convert_alpha()
        else:
            image = pygame.image.load(image_path).convert()
        
        # Scale if requested
        if scale:
            width, height = scale
            image = pygame.transform.scale(image, (width, height))
        
        return image
    
    except Exception as e:
        print(f"Error loading image '{image_path}': {e}")
        
        # Create fallback surface if color provided
        if fallback_color and scale:
            fallback = pygame.Surface(scale)
            fallback.fill(fallback_color)
            return fallback
        
        # Re-raise exception if no fallback
        raise


def load_image_fit(image_path, max_width, max_height, convert_alpha=True, maintain_aspect=True):
    """
    Load image and scale to fit within given dimensions (like CSS object-fit: contain)
    
    Args:
        image_path: Path to image file
        max_width: Maximum width
        max_height: Maximum height
        convert_alpha: Whether to convert with alpha channel (default True)
        maintain_aspect: Whether to maintain aspect ratio (default True)
    
    Returns:
        tuple: (pygame.Surface, actual_width, actual_height) - scaled image and its dimensions
    
    Raises:
        Exception: If image fails to load
    """
    # Load original image
    if convert_alpha:
        image = pygame.image.load(image_path).convert_alpha()
    else:
        image = pygame.image.load(image_path).convert()
    
    original_width, original_height = image.get_size()
    
    if maintain_aspect:
        # Calculate scale ratio to fit within bounds
        width_ratio = max_width / original_width
        height_ratio = max_height / original_height
        scale_ratio = min(width_ratio, height_ratio)
        
        # Calculate new dimensions
        new_width = int(original_width * scale_ratio)
        new_height = int(original_height * scale_ratio)
    else:
        # Stretch to fill
        new_width = max_width
        new_height = max_height
    
    # Scale with smooth algorithm
    scaled_image = pygame.transform.smoothscale(image, (new_width, new_height))
    
    return scaled_image, new_width, new_height


def load_background_image(image_name, screen_width, screen_height, fallback_color=(50, 50, 100)):
    """
    Load background image from assets/images/backgrounds/
    
    Args:
        image_name: Name of the image file
        screen_width: Target width to scale to
        screen_height: Target height to scale to
        fallback_color: RGB tuple for fallback if load fails
    
    Returns:
        pygame.Surface: Loaded and scaled background
    """
    try:
        image_path = get_assets_path('images', 'backgrounds', image_name)
        return load_image(image_path, convert_alpha=False, scale=(screen_width, screen_height))
    except Exception as e:
        print(f"Error loading background '{image_name}': {e}")
        # Create fallback surface
        fallback = pygame.Surface((screen_width, screen_height))
        fallback.fill(fallback_color)
        return fallback


def load_ui_image(image_name, max_width, max_height):
    """
    Load UI image (like buttons) from assets/images/ui/ with aspect ratio maintained
    
    Args:
        image_name: Name of the image file
        max_width: Maximum width constraint
        max_height: Maximum height constraint
    
    Returns:
        tuple: (pygame.Surface, actual_width, actual_height)
    
    Raises:
        Exception: If image fails to load
    """
    image_path = get_assets_path('images', 'ui', image_name)
    return load_image_fit(image_path, max_width, max_height, convert_alpha=True, maintain_aspect=True)
