CC = gcc
TARGET = chall

all: $(TARGET)

$(TARGET): chall.c
	$(CC) $(CFLAGS) -o $(TARGET) chall.c

debug: chall.c
	$(CC) $(CFLAGS) -g -o $(TARGET)_debug chall.c

clean:
	rm -f $(TARGET) $(TARGET)_debug

.PHONY: all debug clean
