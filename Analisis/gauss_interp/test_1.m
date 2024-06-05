clear 

FOLDER = '540-645_rampa/';
FILE = '540.0';
 
s1=make_hist(strcat(FOLDER, FILE, '_loc.csv'),10);
s2=make_hist(strcat(FOLDER, FILE, '_peaks.csv'),11);
s3=make_hist(strcat(FOLDER, FILE, '_temp.csv'),12);
s4=make_spectrum(strcat(FOLDER, FILE, '_os.csv'),13);

function [out] = make_hist(file, fig)
    NOBINS = 100;
    raw = csvread(file);
    figure(fig), clf
        histogram(raw(:,1),NOBINS,'FaceColor', 'red')
        hold on
        histogram(raw(:,2),NOBINS,'FaceColor', 'green')
        legend('Sensor-1', 'Sensor-2')
        hold off
		out = raw;
end


function [out] = make_spectrum(file, fig)
    raw = csvread(file);
    
    lambdas = [1500:0.005:1600];
    mean_value = mean(raw);
    
    % Plot the data points
    figure(fig),  clf, plot(lambdas, raw,'k.','MarkerSize',4, ...
        'MarkerEdgeColor',[0.9, 0.9,0.9], 'MarkerFaceColor',[0.8, 0.8,0.8]);
    hold on, plot(lambdas,mean_value,'k'), hold off
	out = raw;
    
   
end



