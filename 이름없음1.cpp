#include <stdio.h>

int main(){
	long long int n=0,remain=0,sum=1,t=0,k=0,flag=1;
	long long int num[10000]={0};
	long long int trash[10000]={0};
	long long int min=0;
	
	scanf("%lld",&n);
	scanf("%lld",&num[1]);
	min=num[1];
	
	
	for(int i=2;i<=n;i++){
		
		scanf("%lld",&num[i]);
		
		if(num[i+1]>min){
			min=num[i+1];
		}
	}
	for(long long int i=2;i<=min;i++){
		t=0;
		for(int j=1;j<=n;j++){
			if(j==1){
				remain=num[j]%i;
			}
			
			else {
				if(num[j]%i!=remain){
					t=1;
					break;
				}
			}
			
		}
		if(t==0){
			trash[k]=i;
			k++;
		}
	}

}


