#include <bits/stdc++.h>

#define ll long long
#define de(x) cout<<#x<<": "<<x<<endl
#define MAX 100000

using namespace std;

int main() {

    int i=1;
    ll k,n;
    cin>>k>>n;
    map<ll,ll> l;
    l[1]=i;
    ll j;
    for(j=2;j*j<=k;j++){
        if(k%j==0){
            i++;
            l[i]=j;
        }
    }

    if(n>i*2){
        cout<<-1<<endl;
    }
    else if((j-1)*(j-1)==k && n==i*2){
        cout<<-1<<endl;
    }
    else if(n<=i){
        cout<<l[n]<<endl;
    }
    else{
        n-=i;
        while(i>0){
        if(k/l[i]!=l[i]){
            n--;
            if(n==0){
                cout<<k/l[i]<<endl;
            }
        }
        i--;
        }
    }

}
