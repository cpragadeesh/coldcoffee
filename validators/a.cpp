#include <iostream>
#include <fstream>

using namespace std;

int main(int argc, char *argv[]) {

	ifstream f(argv[1]);

	int a, b;
	f>>a>>b;

	if(a == 1 and b == 2) {
		return 0;
	}

	return 1;
}
