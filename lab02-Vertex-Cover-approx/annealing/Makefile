CC = gcc
CFLAGS = -Wall -g
EXTRA_DEBUG_CFLAGS = -D DEBUG_MODULE #-D Py_REF_DEBUG
.RECIPEPREFIX = >

# Path to Python.h file (probably under /usr/lib/)
ifeq ($(OS),Windows_NT)
    $(warning "Windows not supported yet")
    PYTHON_HEADER_PATH = 
else
    # By default Linux here. locate command is necessary.
    PYTHON_HEADER_PATH = $(shell dirname $$(locate --regexp /include/python[0-9]\.[0-9]/Python.h --limit 1))
endif


SHARED_NAME = annealing.so
SRCS = annealingmodule.c
HEADERS = annealingmodule.h
DEPS = $(SRCS) $(HEADERS)
OBJS = annealingmodule.o

all: $(SHARED_NAME)

$(SHARED_NAME): $(OBJS)
>   $(CC) -shared -o $(SHARED_NAME) $(OBJS) -lc

$(OBJS): $(DEPS)
>   $(CC) -fPIC -c $< $(CFLAGS) -I. -I $(PYTHON_HEADER_PATH) 

debug_build: CFLAGS += $(EXTRA_DEBUG_CFLAGS)

debug_build: $(SHARED_NAME)

.PHONY: clean

clean:
>   rm -f $(OBJS) $(SHARED_NAME)

