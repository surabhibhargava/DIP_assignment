clc;
clear all;

img=double(imread('window.jpg'));
%img=img./255;
A=zeros(376,501);
for i=2:375
    for j=2:500
        A(i,j)=img(i,j)./255;
    end
end
B=zeros(375,500);
for i=2:375
    for j=2:500
        B(i,j)=(-1*A(i-1,j-1))-(1*A(i+1,j-1))-(2*A(i,j-1))+(2*A(i,j+1))+(A(i-1,j+1))+(A(i+1,j+1));
    end
end
C=zeros(375,500);
for i=2:375
    for j=2:500
        C(i,j)=(-1*A(i-1,j-1))-(1*A(i-1,j+1))-(2*A(i-1,j))+(2*A(i+1,j))+(A(i+1,j+1))+(A(i+1,j-1));
    end
end
figure(1)
imshow(B)
title('horizontal gradient')
figure(2)
imshow(C)
title('vertical gradient')

D=abs(B)+abs(C);
figure(3)
imshow(D)
title('edge map')
        
        
            

