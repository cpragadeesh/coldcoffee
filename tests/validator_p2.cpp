#include <iostream>
#include <fstream>

using namespace std;

int main(int argc, char *argv[]) {

	string input = argv[1];
	string output = argv[2];

	ifstream ifile, ofile;

	ifile.open(input);
	ofile.open(output);

	int n;
	int a, b;
	int res;

	ifile>>n;
	for(int i = 1; i <= n; ++i) {
		ifile>>a>>b;
		ofile>>res;

		if(res != a + b + 1) {
			return i;
		}
	}

	return 0;
}
