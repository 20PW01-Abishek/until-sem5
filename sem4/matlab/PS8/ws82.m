syms n x;
f1=-4/pi*x;
f2=4/pi*x;
l=pi/2;

a0=1/l*(int(f1,x,-pi/2,0)+int(f2,x,0,pi/2))
an=1/l*(int(f1,x*cos(n*pi*x/l),-pi/2,0)+int(f2*cos(n*pi*x/l),x,0,pi/2))
bn=1/l*(int(f1,x*sin(n*pi*x/l),-pi/2,0)+int(f2*sin(n*pi*x/l),x,0,pi/2))
[a0/2,eval(subs(an*cos(n*pi*x/l)+bn*sin(n*pi*x/l),n,[1 2 3 4]))]
a0
