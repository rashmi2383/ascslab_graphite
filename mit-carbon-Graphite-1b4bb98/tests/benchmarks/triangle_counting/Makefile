
TARGET = triangle_counting_lock triangle_counting_atomic
#TARGET := triangle_counting_lock triangle_counting_atomic
##OBJECTS := $(TARGET).o

THREADS ?= 8
SIZE ?= 16384
DEGREE ?= 16
APP_FLAGS ?= $(THREADS) $(SIZE) $(DEGREE)

LIBS += -lpthread -lrt

CXXFLAGS = -g --std=c++0x -O3
#CXXFLAGS += #-Wall -Werror

include ../../Makefile.tests


all: $(TARGET)

triangle_counting_lock: triangle_counting_lock.cc
triangle_counting_atomic: triangle_counting_atomic.cc

##clean:
##	rm -f $(TRGS) *.o *.dot

%: %.cc ;
	$(CXX) $(CXXFLAGS) $< -o $@ $(LIBS)

