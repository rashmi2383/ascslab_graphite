#Example Makefile for the bc benchmark running with the Graphite Simulator

TARGET := bc
OBJECTS := $(TARGET).o 
#LIBS += -lrt

THREADS ?= 256
SIZE ?= 16384
DEGREE ?= 16
APP_FLAGS ?= $(THREADS) $(SIZE) $(DEGREE)

#MACROS := ../splash_support/c.m4.null.POSIX

#CXXFLAGS = -g --std=c++0x -O3
#CXXFLAGS += -Wall -Werror

#clean:
#	rm -f $(TRGS) *.o *.dot

#%.o: %.cc ;
#	$(CXX) $(CXXFLAGS) $< -o $@ $(LIBS)

include ../../Makefile.tests
#include ../splash_support/Makefile.config
