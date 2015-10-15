clc;
clear all;

image1=double(imread('unenhanced.tif'));
min_pixel=min(image1(:));
max_pixel=max(image1(:));
new_image=zeros(291,240);
for i=1:291
    for j=1:240
        new_image(i,j)=(255/(max_pixel-min_pixel)).*(image1(i,j)-min_pixel);
    end
end
frequency=zeros(255,1);
Y=uint8(new_image);
for i=1:291
   for j=1:240
       frequency(Y(i,j)+1,1)=frequency(Y(i,j)+1,1)+1;
   end
end
x=[1:1:255];
z=frequency(x,1);
new_image=new_image.*(1/255);
figure(1)
subplot(2,1,1),subimage(new_image)
title('contrast stretch')
subplot(2,1,2),bar(z)
title('contrast stretch - histogram')

%% transform = r^y where y>1 since the image looks washed out %%%%
for i=1:291
    for j=1:240
        powerLaw_image(i,j)=((1/255).*image1(i,j)).^ 2;
    end
end
frequency=zeros(255,1);
Y=uint8(255.*powerLaw_image);
for i=1:291
   for j=1:240
       frequency(Y(i,j),1)=frequency(Y(i,j),1)+1;
   end
end
x=[1:1:255];
z=frequency(x,1);
figure(2)
subplot(2,1,1),subimage(powerLaw_image)
title('power law transform')
subplot(2,1,2),bar(z)
title('histogram for power law transform')
  
 %% histogram equalization %%%
frequency=zeros(255,1);
for i=1:291
   for j=1:240
       frequency(image1(i,j),1)=frequency(image1(i,j),1)+1;
   end
end

probability=frequency./(291*240);
cdf=zeros(255,1);
cdf(1)=probability(1);
for i=2:255
   cdf(i)=probability(i)+cdf(i-1);
end
eq_img=zeros(291,240);
for i=1:291
    for j=1:240
        eq_img(i,j)=cdf(image1(i,j));
    end
end
frequency=zeros(255,1);
Y=uint8(255.*eq_img);
for i=1:291
   for j=1:240
       frequency(Y(i,j)+1,1)=frequency(Y(i,j)+1,1)+1;
   end
end
x=[1:1:255];
z=frequency(x,1);
figure(3)
subplot(2,1,1),subimage(eq_img)
title('equalized image')
subplot(2,1,2),bar(z)
title('equalized histogram')

% subplot(2,1,1),subimage(eq_img);
% title('equalized image');
% subplot(2,1,2),imhist(eq_img);
% title('equalized image-histogram');

    