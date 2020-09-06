#include<bits/stdc++.h>
#define rep(i,A,B) for(int i=(A);i<=(B);i++)
using namespace std;
#define mn 2000000
typedef pair<string,string> pss;
char a[mn],b[mn];
int ch[100],n,m,CNT;
const int dist[5][5]={{0,1,2,1,3},{1,0,1,5,1},{2,1,0,9,1},{1,5,9,0,1},{3,1,1,1,0}};
int f[2][mn],g[2][mn];
int dp1(int n,int m,char* A,char* B){
    f[0][0]=0;
    rep(i,1,m)f[0][i]=f[0][i-1]+dist[0][ch[B[i]]];
    rep(i,1,n){
        f[i&1][0]=f[~i&1][0]+dist[ch[A[i]]][0];
        rep(j,1,m){
            f[i&1][j]=f[~i&1][j-1]+dist[ch[A[i]]][ch[B[j]]];
            f[i&1][j]=min(f[i&1][j],min(f[~i&1][j]+dist[ch[A[i]]][0],f[i&1][j-1]+dist[0][ch[B[j]]]));
        }
    }
    return f[n&1][m];
}
int dp2(int n,int m,char* A,char* B){
    g[0][0]=0;
    rep(i,1,m)g[0][i]=g[0][i-1]+dist[0][ch[B[m-i+1]]];
    rep(i,1,n){
        g[i&1][0]=g[~i&1][0]+dist[ch[A[n-i+1]]][0];
        rep(j,1,m){
            g[i&1][j]=g[~i&1][j-1]+dist[ch[A[n-i+1]]][ch[B[m-j+1]]];
            g[i&1][j]=min(g[i&1][j],min(g[~i&1][j]+dist[ch[A[n-i+1]]][0],g[i&1][j-1]+dist[0][ch[B[m-j+1]]]));
        }
    }
    return g[n&1][m];
}
int dp(int n,int m,char* A,char* B,pss&res){
    if(n==0){
        int cost=0;
        string rsA,rsB;
        rep(j,1,m){
            cost+=dist[0][ch[B[j]]];
            rsA+="-";rsB+=B[j];
        }
        res=make_pair(rsA,rsB);
        return cost;
    }
    if(n==1){
        int cost=dp1(n,m,A,B);
        string rsA,rsB;
        rep(j,1,m){
            rsA+="-";rsB+=B[j];
        }
        for(int j=m;j>=0;j--){
            if(f[1][j]==f[0][j]+dist[ch[A[1]]][0]){
                rsA.insert(j,1,A[1]);
                rsB.insert(j,1,'-');
                break;
            }
            if(f[1][j]==f[0][j-1]+dist[ch[A[1]]][ch[B[j]]]){
                rsA[j-1]=A[1];
                break;
            }
        }
        res=make_pair(rsA,rsB);
        //cout<<rsA<<" "<<rsB<<" "<<cost<<endl;
        return cost;
    }
    int cost=(1<<29), p=-1, i=n/2;
    dp1(i,m,A,B);dp2(n-i,m,A+i,B);
    rep(j,0,m){
        int c1=f[i&1][j], c2=g[(n-i)&1][m-j];
        if(c1+c2<cost){
            cost=c1+c2;p=j;
        }
    }
    //if((CNT++)%20000==0)printf("%d %d %d\n",CNT,n,m);
    //printf("%d %d %d %d\n",n,m,cost,p);
    pss res1,res2;
    dp(i,p,A,B,res1);
    dp(n-i,m-p,A+i,B+p,res2);
    res=make_pair(res1.first+res2.first, res1.second+res2.second);
    return cost;
}
int main(){
    freopen("Data-P2a.txt","r",stdin);
    gets(a+1);fclose(stdin);
    freopen("Data-P2b.txt","r",stdin);
    gets(b+1);fclose(stdin);
    gets(a+1);gets(b+1);
    n=strlen(a+1);m=strlen(b+1);
    //printf("%d %d\n",n,m);
    ch['A']=1;ch['T']=2;ch['G']=3;ch['C']=4;
    pss res;
    int cost=dp(n,m,a,b,res);
    freopen("1.output","w",stdout);
    cout<<cost<<"\n"<<res.first<<"\n"<<res.second<<endl;
    //printf("%d %d\n",cost,sizeof(pth));
    //rep(i,0,n){rep(j,0,m)
    //    printf("%d ",f[i][j]);puts("");}
    //printf("%d\n",f[n][m]);
    return 0;
}