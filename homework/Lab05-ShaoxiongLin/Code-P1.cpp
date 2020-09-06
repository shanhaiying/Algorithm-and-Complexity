#include <bits/stdc++.h>
#define rep(i,A,B) for(int i=(A);i<=(B);i++)
#define mn 4000
using namespace std;
int w[mn],t[mn],dp[mn][mn*2],n,m;
int main()
{
    //freopen("Data-P1.txt", "r", stdin);
    //ios::sync_with_stdio(false);
    //cin.tie(0); cout.tie(0);
    memset(dp,0x3f,sizeof(dp));
    dp[0][0] = 0;
    cin>>n;
    rep(i,1,n) cin>>t[i]>>w[i];
    int nw=0;
    rep(i,1,n){
        nw+=t[i];
        rep(j,0,nw){
            dp[i][j]=dp[i-1][j]+w[i];
            if(j>=t[i])dp[i][j]=min(dp[i][j],dp[i-1][j-t[i]]);
        }
    }
    rep(i,0,nw)
    	if(i>=dp[n][i]){
           cout<<i<<endl;
           break;
        }
    return 0;
}