#include <iostream>


using namespace std;


int main(){

	string vpn1;	

	vpn1 = system("ip link | grep northernblow");

	if (vpn1.length() > 0)
		cout << " ";

    return 0;


}