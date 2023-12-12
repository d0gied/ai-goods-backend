# Makefile для скачивания файла с Dropbox и его сохранения в директорию

# Задайте URL файла на Dropbox
FILE_URL := https://www.dl.dropboxusercontent.com/scl/fi/g2wbeizhpohcj5ob0ol95/model.onnx?rlkey=isuhi9c1trc5hzhpuj4lk0mjv

# Задайте путь к директории, куда нужно поместить файл
TARGET_DIR := ./ml/models/weights

# Имя файла, извлекаемое из URL
FILE_NAME := $(notdir $(FILE_URL))

# split name by ?
FILE_NAME := $(firstword $(subst ?, ,$(FILE_NAME)))

.PHONY: all
all: $(TARGET_DIR)/$(FILE_NAME)

$(TARGET_DIR)/$(FILE_NAME): | $(TARGET_DIR) 
	curl -L $(FILE_URL) -o $@

$(TARGET_DIR):
	mkdir -p $@

	

