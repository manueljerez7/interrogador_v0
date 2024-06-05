TEMP = [21.2, 58.0, 101.0, 151.0, 198.7, 257.0, ...
            313.5, 369.5, 438.5, 496.0,  549.0, ...
            613.5, 642.0, 666.0, 702.0];

diff_fbg=[2.7, 1.5, 6.7, 11.6, 14.1, 14.6, 12.2, 12.1, 11.4, 10.6, 10.3, 8.9, 7.3, 4.8, 3.7];
diff_c2=[10.3, 4.8, 1.3, 6.6, 8.7, 7.7, 2.8, 0.0, 3.8, 6.1, 6.1, 3.8, 1.8, 0.7, 5.0];
diff_c3=[2.0, 1.1, 0.9, 2.6, 2.6, 1.0, 2.4, 2.4, 1.6, 0.4, 1.2, 2.3, 1.6, 0.3, 0.9];
diff_c4=[0.4, 0.8, 0.3, 0.7, 0.9, 0.4, 1.6, 0.5, 0.4, 0.5, 0.6, 0.2, 0.3, 1.4, 0.5];

figure(11), clf, hold on
bar(TEMP,diff_fbg,'barWidth', 0.4, 'DisplayName','Original')
figure(11), bar(TEMP+2*3,diff_c2,'barWidth', 0.4, 'DisplayName',strcat('interp-',num2str(2)))
figure(11), bar(TEMP+3*3,diff_c3,'barWidth', 0.4, 'DisplayName',strcat('interp-',num2str(3)))
figure(11), bar(TEMP+4*3,diff_c4,'barWidth', 0.4, 'DisplayName',strcat('interp-',num2str(4)))
figure(11), title('Results: Method 1'), legend, xlabel('Thermopar temp. [ºC]'), ylabel('Estimated temp. absolute error [ºC]')

