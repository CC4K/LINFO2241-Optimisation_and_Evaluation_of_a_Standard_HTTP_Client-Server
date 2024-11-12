build: main.c ../project/utils/utils.c
	mkdir -p build 
	gcc -o build/main main.c ../project/utils/utils.c -I../project/utils -Wall -Wextra -Werror -std=c99 -pedantic -g

build_old: main.c ../project/utils/utils.c
	mkdir -p build 
	gcc -o build/main main_old.c ../project/utils/utils.c -I../project/utils -Wall -Wextra -Werror -std=c99 -pedantic -g
run: build
	./build/main
run_old: build_old
	./build/main

debug: build
	gdb -ex run -ex "quit" --args ./build/main