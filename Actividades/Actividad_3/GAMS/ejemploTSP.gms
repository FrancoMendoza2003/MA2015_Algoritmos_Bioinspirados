$title TSP
Sets
i index /1*5/;
alias (i,j);
sets offdiag1(i,j)
     offdiag2(i,j);
offdiag1(i,j)=yes;
offdiag1(i,i)=no;
offdiag2(i,j)=offdiag1(i,j);
offdiag2(i,'1')=no;
offdiag2('1',j)=no;

table
t(i,j)
  1  2  3  4  5
1 99 2  3  1  4
2 2  99 2  1  3
3 3  2  99 4  2
4 1  1  4  99 3
5 4  3  2  3  99 ;


Scalar n;
n=card(i);

Variables f, y;

binary variable x;

Equations
ohr1(j)
ohr2(i)
anti(i,j)
ucel;

ucel.. f=e=sum((i,j),t(i,j)*x(i,j));
ohr1(j).. sum(i,x(i,j)$offdiag1(i,j))=e=1;
ohr2(i).. sum(j,x(i,j)$offdiag1(i,j))=e=1;
anti(offdiag2(i,j)).. y(i)-y(j)+n*x(i,j)=l=n-1;

model TSP2 /all/;
Solve TSP2 using mip minimizing f;
display x.l, f.l;