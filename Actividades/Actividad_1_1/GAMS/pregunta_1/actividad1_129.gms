option OptCR = 0.00001;
set
i /1*20/;

Variable
z;

binary variable
x(i);

Parameter
p(i)/
1 107.0
2 105.0
3 81.0
4 112.0
5 72.0
6 115.0
7 66.0
8 67.0
9 70.0
10 114.0
11 60.0
12 111.0
13 87.0
14 107.0
15 98.0
16 95.0
17 65.0
18 104.0
19 79.0
20 74.0
/;

Parameter
b(i)/
1 1967.0
2 1841.0
3 1259.0
4 1347.0
5 1645.0
6 1538.0
7 1812.0
8 1325.0
9 1906.0
10 1782.0
11 1429.0
12 1769.0
13 1053.0
14 1131.0
15 1384.0
16 1461.0
17 1996.0
18 82.0
19 80.0
20 107.0
/;

equations
FO
r1;

FO.. z =e= sum(i, x(i)*b(i));

r1.. sum(i,  x(i)*p(i)) =l= 700;

model pregunta29_cargero /all/;
solve pregunta29_cargero using mip max z;