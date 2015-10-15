clear all
clc

im1 = imread('givenhist.jpg');
imshow(im1)
imhist(im1)
given_hist = imhist(im1);
normalized_givenhist = given_hist/sum(given_hist);
f = zeros(2,256);
for i=1:256
    f(1,i) = round(255*(sum(normalized_givenhist(1:i))));
end

im2 = imread('sphist.jpg');
sphist = imhist(im2);
normalized_sphist = sphist/sum(sphist);
Gz = zeros(1,256);
for i=1:256
    Gz(i) = round(255*(sum(normalized_sphist(1:i))));
end

for i=1:256
    val = zeros(1,256);
    val = abs(Gz - f(1,i)); 
    [M,I] = min(val);
    f(2,i) = I;
end

final = zeros(1,256);
for i=1:256
   final(i) = sum(given_hist(f(2,:) == i)); 
end

figure(1)
imhist(im2)
title('given histogram')
figure(2)
bar(final,'b','LineWidth',0.1,'LineStyle',':')
title('histogram after transformation')
