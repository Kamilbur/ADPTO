CC = gcc
CFLAGS = -Wall
.RECIPEPREFIX = >

# Path to Python.h file (probably under /usr/lib/)
ifeq ($(OS),Windows_NT)
    $(warning "Windows not supported yet")
    PYTHON_HEADER_PATH = 
else
    # By default Linux here. locate command is necessary.
    # Here I use the default path on my machine to speed up search.
    # If the search of hardcoded path of mine fails then the more
    # general search is performed.
    PYTHON_HEADER_PATH = $(shell dirname $$(locate --regexp /usr/include/python.*/Python.h --limit 1) ||\
                                 dirname $$(locate --regexp /.*/include/python.*/Python.h --limit 1))
endif


SRCS = annealingmodule.c
HEADERS = annealingmodule.h
DEPS = $(SRCS) $(HEADERS)
OBJS = annealingmodule.o

all: $(OBJS)

$(OBJS): $(DEPS)
>   $(CC) -c $< $(CFLAGS) -I. -I $(PYTHON_HEADER_PATH) 

.PHONY: clean

clean:
>   rm -f $(OBJS)
