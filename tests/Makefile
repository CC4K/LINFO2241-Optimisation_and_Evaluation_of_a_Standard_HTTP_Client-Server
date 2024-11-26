# current test files
build: main.c ../project/utils/utils.c
	@mkdir -p build
	@gcc -Wall -Wextra -Werror -std=c99 -pedantic -g -I../project/utils main.c ../project/utils/utils.c -o build/main

run: build
	@./build/main

# old test files
build_old: main.c ../project/utils/utils.c
	mkdir -p build 
	gcc -o build/main main_old.c ../project/utils/utils.c -I../project/utils -Wall -Wextra -Werror -std=c99 -pedantic -g

run_old: build_old
	./build/main

debug: build
	gdb -ex run -ex "quit" --args ./build/main

gprof:
	gcc -pg -o build/main main.c ../project/utils/utils.c -I../project/utils -Wall -Wextra -Werror -std=c99 -pedantic -g
	./build/main
	gprof build/main gmon.out > analysis.txt

perf:
	gcc -o build/main main.c ../project/utils/utils.c -I../project/utils -Wall -Wextra -Werror -std=c99 -pedantic -g
	perf record -g ./build/main

clean:
	rm -rf build
	rm -f gmon.out
	rm -f analysis.txt

# perf report
# fx
