# ----------------------------
# Makefile Options
# ----------------------------

NAME = GIMME5
VERSION = "2.0.0"
ICON = icon.png
DESCRIPTION = "Gimme 5 "$(VERSION)
COMPRESSED = NO
ARCHIVED = NO

CFLAGS = -Wall -Wextra -Oz -DEXTERN__PROGRAM_VERSION=$(VERSION)
CXXFLAGS = -Wall -Wextra -Oz -DEXTERN__PROGRAM_VERSION=$(VERSION)

# ----------------------------

include $(shell cedev-config --makefile)
