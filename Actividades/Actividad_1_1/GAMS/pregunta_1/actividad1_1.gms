option OptCR = 0.00001;

set
i /1*10/;

Variable
z;

binary variable
x(i);

Parameter
p(i)/
1  100
2  155
3  50
4  112
5  70
6  80
7  60
8  118
9  110
10 55
/;

Parameter
b(i)/
1 174100
2 251410
3 50800
4 141568
5 91350
6 111120
7 107820
8 156940
9 171490
10 86790
/;



equations
FO
r1;

FO.. z =e= sum(i, x(i)*b(i));

r1.. sum(i,  x(i)*p(i)) =l= 700;

model pregunta1_cargero /all/;
solve pregunta1_cargero using mip max z;