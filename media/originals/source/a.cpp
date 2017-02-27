#include <bits/stdc++.h>

#define ll long long
#define debug(x) cout<<#x<<": "<<x<<endl

using namespace std;

int main() {
  
  int t;
  cin>>t;

  while(t--) {
    string s;
    cin>>s;

    int a[500];
    memset(a, 0, sizeof a);
    
    int maxi = 0;
    
    for(int i = 0; i < s.size(); ++i) {
      a[s[i]]++;
      maxi = max(maxi, a[s[i]]);
    }

    cout<<s.size() - maxi<<endl;
  }
  
  return 0;
}
