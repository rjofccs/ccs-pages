TARGET = main
OBJ = main.o

$(TARGET):$(OBJ)
	@echo "prophet herald"
	$(CC) $^ -o $(TARGET)

$(OBJ):main.c
	$(CC) -c $^ -o $(OBJ)

clean:
	$(RM) *.o $(TARGET)
