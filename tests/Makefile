P4_FLAGS = -mavx2 -mavx512f -msse4 -fno-unroll-loops -fno-tree-vectorize -O2
CFLAGS+= -ggdb -fPIC -Wextra -Werror -Wall -pedantic

build: main.c ../project/utils/utils.c ../project/utils/simd.c
	@mkdir -p build
	@gcc $(CFLAGS) $(P4_FLAGS) -I../project/utils main.c ../project/utils/utils.c ../project/utils/simd.c -o build/main

run: build
	@./build/main

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
