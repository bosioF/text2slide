USAGE_MSG="Usage: python src/main.py input.txt <Quality> <OutputFileName> OR --help"
HELP_MSG="""\
Usage: python src/main.py input.txt <Quality> <OutputFileName> OR --help (to open this menu)

Quality flags:
-ql\t480p 15fps
-qm\t720p 60fps
-qh\t1080p 60fps
-qp\t1440p 60fps
-qk\t2160p 60fps

Available colors:

Basic:
    BLACK, WHITE, RED, GREEN, BLUE, YELLOW, ORANGE, PINK, PURPLE, TEAL, GOLD, MAROON, GRAY, GREY

Variants (use with base names):
    *_A, *_B, *_C, *_D, *_E
    Example: RED_A, GREEN_E, BLUE_C, GOLD_D

Shades:
    DARK_GRAY, DARK_GREY, DARKER_GRAY, DARKER_GREY, DARK_BLUE, DARK_BROWN,
    LIGHT_GRAY, LIGHT_GREY, LIGHTER_GRAY, LIGHTER_GREY, LIGHT_BROWN, LIGHT_PINK

Grays:
    GRAY_A, GRAY_B, GRAY_C, GRAY_D, GRAY_E, GRAY_BROWN,
    GREY_A, GREY_B, GREY_C, GREY_D, GREY_E, GREY_BROWN

Logo colors:
    LOGO_BLACK, LOGO_WHITE, LOGO_RED, LOGO_GREEN, LOGO_BLUE

Pure RGB:
    PURE_RED (#FF0000), PURE_GREEN (#00FF00), PURE_BLUE (#0000FF)

Use any color name as shown above. Names are case-sensitive."""