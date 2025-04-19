import pygame
import sys
from gettext import gettext as _

# Initialize all pygame modules
pygame.init()

# Set up the display window with a default size
screen = pygame.display.set_mode((800, 600))  # Change size as needed
pygame.display.set_caption("Pippy")  # Set the title of the window

def pause():
    """Display a 'Paused' screen with overlay and wait for user interaction to resume."""

    # Get the current window caption and surface for restoration later
    caption, icon_caption = pygame.display.get_caption()
    old_screen = screen.convert_alpha().copy()  # Save the current screen with alpha transparency

    # Colors for the overlay
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Create a dimmed version of the current screen
    dimmed = screen.copy()
    dimmed.set_alpha(128)  # Set transparency to 50%
    screen.fill(BLACK)  # Fill screen with black
    screen.blit(dimmed, (0, 0))  # Overlay the dimmed version

    # Prepare the "PAUSED" message
    font = pygame.font.Font(None, 36)  # Load default font at 36px size
    msg = _("PAUSED")
    msg_surf = font.render(msg, True, BLACK, WHITE)  # Render the text

    # Center the message on the screen
    rect = msg_surf.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
    screen.fill(WHITE, rect.inflate(rect.width, rect.height))  # Draw a white background behind the message
    screen.blit(msg_surf, rect)  # Draw the message on top
    pygame.display.flip()  # Update the screen with the changes

    # Wait for any event to resume
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # If the user closes the window, exit the program
            pygame.quit()
            sys.exit()

    # Restore the previous screen
    pygame.display.set_caption(caption, icon_caption)
    screen.blit(old_screen, (0, 0))
    pygame.display.flip()

# Time of the last user event (used for idle detection)
_last_event_time = pygame.time.get_ticks()

# Global clock object for controlling FPS
_default_clock = pygame.time.Clock()

def next_frame(max_fps=20, idle_timeout=20, clock=None, pause_func=pause):
    """
    Limits the game's frame rate and detects idle time.
    
    If the game has been idle for longer than `idle_timeout` seconds,
    the pause screen is triggered to prevent battery drain.
    """
    global _last_event_time, _default_clock

    # Use the provided clock or the default one
    if clock is None:
        clock = _default_clock

    # Limit the frame rate to `max_fps` frames per second
    clock.tick(max_fps)

    # Check if any events (keyboard/mouse/etc.) are in the queue
    if pygame.event.peek():
        _last_event_time = pygame.time.get_ticks()  # Reset idle timer
    elif (pygame.time.get_ticks() - _last_event_time) >= idle_timeout * 1000:
        # If idle for longer than timeout, trigger pause
        pause_func()
        _last_event_time = pygame.time.get_ticks()  # Reset idle timer after pause

    return True  # Indicate that frame was successfully processed
