data=xlsread('.\result\tot_draw.xlsx')
data(1,:)=[]
b = bar3(data,0.5);
%b=surf(data)