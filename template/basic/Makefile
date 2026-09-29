CC ?= clang
CFLAGS ?= -Wall -Wextra -Wpedantic -std=c11 -Iinclude
LDFLAGS ?=

SRC_DIR := src
BUILD_DIR := build
TARGET := $(BUILD_DIR)/main

SRCS := $(wildcard $(SRC_DIR)/*.c)
OBJS := $(patsubst $(SRC_DIR)/%.c,$(BUILD_DIR)/%.o,$(SRCS))

# Deteksi sistem operasi
ifeq ($(OS),Windows_NT)
    TARGET := $(TARGET).exe
    ifeq ($(SHELL),sh.exe)
        MKDIR = mkdir -p $(BUILD_DIR)
        RM = rm -rf $(BUILD_DIR)
    else ifeq ($(findstring /sh,$(SHELL)),/sh)
        MKDIR = mkdir -p $(BUILD_DIR)
        RM = rm -rf $(BUILD_DIR)
    else
        MKDIR = if not exist $(BUILD_DIR) mkdir $(BUILD_DIR)
        RM = if exist $(BUILD_DIR) rmdir /s /q $(BUILD_DIR)
    endif
else
    MKDIR = mkdir -p $(BUILD_DIR)
    RM = rm -rf $(BUILD_DIR)
endif

.PHONY: all run clean

all: $(TARGET)

$(TARGET): $(OBJS)
	@$(MKDIR)
	$(CC) $(OBJS) -o $@ $(LDFLAGS)

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	@$(MKDIR)
	$(CC) $(CFLAGS) -c $< -o $@

run: $(TARGET)
	@$(TARGET)

clean:
	@$(RM)
