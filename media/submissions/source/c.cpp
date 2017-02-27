#include <bits/stdc++.h>

#define ll long long
#define debug(x) cout<<#x<<": "<<x<<endl
#define pb push_back

using namespace std;

ll ans = 0;
ll visited[123456];

struct Node {
  vector<int> adj;
  ll x, y;

  Node() {
    x = y = 0;
  }
};

ll dfs(Node t[], ll v) {

  visited[v] = 1;

  for(auto next : t[v].adj) {
    if(!visited[next]) {
      ll d = 1 + dfs(t, next);
      if(d >= t[v].x) {
	t[v].y = t[v].x;
	t[v].x = d;
      }
      if(d >= t[v].y and d < t[v].x)
	t[v].y = d;

      ans = max(ans, t[v].y + t[v].x);
    }
  }

  return t[v].x;
}

int main() {

  ll n;
  cin>>n;

  Node t[n];

  for(ll i = 0; i < n - 1; i++) {
    ll x, y;
    cin>>x>>y;
    x--; y--;

    t[x].adj.pb(y);
    t[y].adj.pb(x);
  }

  dfs(t, 0);

  if(ans % 2 == 0) {
    ans = ans / 2;
  }

  else {
    ans = (ans + 1) / 2;
  }

  cout<<ans<<endl;

  return 0;
}

