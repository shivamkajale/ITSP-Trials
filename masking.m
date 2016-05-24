clear;
I=imread('lotus.jpg');         % image name
load blur.shit;                % mask file name
T=blur;                        % mask file name without extension
s=size(T);
p=size(I);
M=I(1:s(1),1:s(2),3);
for i=1:s(1)
    for j=1:s(2)
        M(i,j)=T(i,j);
    end
end

O=I(1:(p(1)-s(1)+1),1:(p(2)-s(2)+1),3);
for i=1:(p(1)-s(1)+1)
    for j=1:(p(2)-s(2)+1)
        for k=1:p(3)
            temp=I(i:i+(s(1)-1),j:j+(s(2)-1),k);
            O(i,j,k)=sum(sum(temp.*M))/(s(1)*s(2));
        end
    end
end
imwrite(O,'out.jpg')

    
    
