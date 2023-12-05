$title TSP
Sets
i index /1*7/;
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
    1   2   3   4   5   6   7
1   99  12  10  99  99  99  12
2   12  99  8   12  99  99  99
3   10  8   99  11  3   99  9
4   99  12  11  99  11  10  99
5   99  99  3   11  99  6   7
6   99  99  99  10  6   99  9
7   12  99  9   99  7   9   99;



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