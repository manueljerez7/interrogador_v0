clear,close all
figure
temp = readtable('cal_data_fb2_mar24\705.1_temp.csv').Var1';
s = 1:length(temp);
temp_avg=mean(temp);
plot(s,temp,'LineWidth',1)
hold on
plot(s,temp_avg*ones(length(temp),1),'r.','LineWidth',2)
legend('Temperature measured by thermocouple','Mean temperature')
ylabel('Temperature [ºC]')
xlabel('Sample')
title('Temperature evolution')