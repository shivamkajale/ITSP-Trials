clear;
%T=3,w=2pi/T...
T=3; w=2*pi/T;
dx=1/100;
x=0:dx:T;
f=exp(x).*cos(x).^2;   %function defined here
A0=sum(f)*dx/T;
g=A0;
for k=1:10
    A(k)=2/T*sum(f.*cos(k*w*x))*dx;
    B(k)=2/T*sum(f.*sin(k*w*x))*dx;
    g=g+A(k)*cos(k*w*x)+B(k)*sin(k*w*x);
    plot(x,f,'r',x,g,'m',x,x*0,'k');
    axis([0 T -5 20]);      %axis limits here
    pause(1);
end