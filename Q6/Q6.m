clc;
clear all;

im=double(imread('lenna.noise.jpg'));
im1=im./255;
im=im1;

% anisotropic filter, k=2, num of iterations= 20, lambda=.05, 4
% connectivity
fn=[0 1 0; 0 -1 0; 0 0 0];
fs=[0 0 0; 0 -1 0; 0 1 0];
fe=[0 0 0; 0 -1 1; 0 0 0];
fw=[0 0 0; 1 -1 0; 0 0 0];

for i=1:20
    
    
    im_n=imfilter(im, fn);
    im_s=imfilter(im, fs);
    im_e=imfilter(im, fe);
    im_w=imfilter(im, fs);

    k=2;
    cn=1./(1+(im_n/k).^2);
    cs=1./(1+(im_s/k).^2);
    ce=1./(1+(im_e/k).^2);
    cw=1./(1+(im_w/k).^2);

    im=im + .05* (cn.*im_n + cs.*im_s + ce.*im_e + cw.*im_w);
    
end
figure(1)
subplot(1,2,1), imshow(im1)
title('Original image')
subplot(1,2,2), imshow(im)
title('Filtered with anisotropic filter')

%isotropic filter
f=[0 1 0; 1 -4 1; 0 1 0];
for i=1:20
im1=im1+imfilter(im1,f)./5;
figure(2)
subplot(1,2,2),imshow(im1)
title('Filtered with isotropic filter')
subplot(1,2,1), imshow(im)
title('Filtered with anisotropic filter')
end



