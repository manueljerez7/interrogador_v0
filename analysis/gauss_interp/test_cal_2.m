clear
CASE = 'fb2';
switch CASE
    case 'fb1',
        
        PATH = 'cal_data_fb1_mar24/'
        CAL_TITLE = 'fb1_0'
        TEMP = [80.0, 173.5, 311.3, 437.5, 539.0, 635.0];% 637.0, 641.5];
        FBG_ID = 1;
        OS_INT = [1519, 1529];
        
        OS_NoTRACES = 5; % numero de trazas
        PEAK_METHOD = 1;
        
        
    case 'fb2',
        
        PATH = 'cal_data_fb2_mar24/'
        
        CAL_TITLE = 'fb2_0'
        TEMP = [21.2, 58.0, 101.0, 151.0, 198.7, 257.0, ...
            313.5, 369.5, 438.5, 496.0,  549.0, ...
            613.5, 642.0, 666.0, 702.0];
        FBG_ID = 2;
        OS_INT = [1529, 1540];
        
        OS_NoTRACES = 5; % numero de trazas
        PEAK_METHOD = 1;
end

peak_amp_db = zeros(length(TEMP),1);
peak_loc_nm = zeros(length(TEMP),1);
peak_dev_nm = zeros(length(TEMP),1);
temp_ref = zeros(length(TEMP),OS_NoTRACES);
loc_ref = zeros(length(TEMP),OS_NoTRACES);


for k=1:length(TEMP)
    
    os_filename = strcat(PATH,num2str(TEMP(k),'%.1f'),'_os.csv');
    loc_filename = strcat(PATH,num2str(TEMP(k),'%.1f'),'_loc.csv');
    temp_filename = strcat(PATH,num2str(TEMP(k),'%.1f'),'_temp.csv');
    
    [peak_amp_db_, peak_loc_nm_, peak_dev_nm_ ]= find_peak_opt(os_filename, OS_INT, OS_NoTRACES);
    peak_amp_db(k) = peak_amp_db_(PEAK_METHOD); % params estimation in freq domain
    peak_loc_nm(k) = peak_loc_nm_(PEAK_METHOD);
    peak_dev_nm(k) = peak_dev_nm_(PEAK_METHOD);
    
    temp_ref_tran = csvread(temp_filename);
    temp_ref(k,:) = temp_ref_tran(1:OS_NoTRACES,FBG_ID);
    
    loc_ref_tran = csvread(loc_filename);
    
    loc_ref(k,:) = loc_ref_tran(1:OS_NoTRACES,FBG_ID);
end


figure(10), clf, hold on
plot(loc_ref', temp_ref',...
    'o','MarkerSize',6, 'MarkerEdgeColor',[0.7, 0.7,0.7], ...
    'MarkerFaceColor',[0.7, 0.7,0.7])
plot(peak_loc_nm, TEMP,'.k','MarkerSize',6), hold on

save(CAL_TITLE)

figure(11), clf, hold on
bar(TEMP,abs(TEMP-mean(temp_ref')),'barWidth', 0.2, 'DisplayName','Instrument')

peak_loc_int = linspace(peak_loc_nm(1,1),peak_loc_nm(end,1));
k=1;

for order=2:4
    [p,~,mu]  = polyfit(peak_loc_nm, TEMP,order);
    temp_int = polyval(p,peak_loc_int,[],mu);
    figure(10), plot(peak_loc_int,temp_int)
    
    calibration(k).order = order;
    calibration(k).p = p;
    calibration(k).p = p;
    calibration(k).mu = mu;
    %calibration(k).p_un= p.* (mu(2) .^ (0:-1:-order)) ./ (mu(1).^ (0:-1:-order));
    
    figure(11), bar(TEMP+order*3,abs(TEMP'-polyval(p,peak_loc_nm,[],mu)),...
        'barWidth', 0.2, 'DisplayName',strcat('interp-',num2str(order)))
    k=k+1;
end

figure(11), legend, xlabel('thermopar temp.'), ylabel('estimated temp.')
save(CAL_TITLE)



function [peak_amp_db, peak_loc_nm, peak_dev_nm] = find_peak_opt(file, os_interval, no_traces)
FIGURING = 1;

raw_os = csvread(file);
lambdas = [1500:0.005:1600];  % nm wavelenth

% \lambdas are limited to this interval
os_index = [find(lambdas==os_interval(1),1):1:find(lambdas==os_interval(2),1)];

% \lambda to freq conversion
x = 2.99793e17./lambdas(os_index)';

% replicate freq vector
x = repmat(x,1,no_traces);

% trace value in natural units
y = exp(raw_os(1:no_traces,os_index))';

% Interpolation
% funtion: gaussian: p(1) is amplitude, p(2) location and p(3) deviation
fun = @(p, x)p(1)*exp(-((x-p(2))/(sqrt(2)*p(3))).^2);

% fitting algorithm needs an starting point p0
% proposed: based on mean value
y_mean = mean(y')
[y_max, y_max_pos] = max(y_mean)
y_mean_dev =-x(y_max_pos)+x(find(y_mean>y_max/sqrt(2),1));
p0 = [y_max, x(y_max_pos), y_mean_dev]

% solution bounds

%p0 = [0.05, 197.42e12, 10e9];
%lower_bound = [0.04, 197.35e12, 9e9]
%upper_bound = [0.06, 197.45e12, 12e9]
%p0 = [0.05, 6.5785e-4, 4e-8];
%lower_bound = [0.04, 6.56e-4, 1e-8];
%upper_bound = [0.06, 6.59e-4, 10e-8];
lower_bound = p0*0.85;
upper_bound = p0*1.15;

%optimoptions(@lsqnonlin,'StepTolerance',1e-8)

% fitting
p = lsqcurvefit(fun,p0,x,y,lower_bound, upper_bound);

% evaluation resulst
x_fit = linspace(min(x(:,1)), max(x(:,1)), 1e4);
y_fit = fun(p, x_fit);

if(FIGURING)
    figure(1), clf
    plot(lambdas(os_index),raw_os(1:no_traces,os_index),...
        'o','MarkerSize',4, 'MarkerEdgeColor',[0.8, 0.8,0.8], 'MarkerFaceColor',[0.8, 0.8,0.8])
    
    hold on,
    
    plot(lambdas(os_index),mean(raw_os(1:no_traces,os_index)),'r-', 'LineWidth', 1)
    title('Power vs \lambda (nm)')
    xlabel('nm'), ylabel('Power')
    
    figure(2), clf
    plot(x/1e12,y,'o','MarkerSize',5, 'MarkerEdgeColor',[0.8, 0.8,0.8], 'MarkerFaceColor',[0.8, 0.8,0.8])
    
    hold on,
    plot(x_fit/1e12,y_fit,'k-', 'LineWidth', 1)
    xlabel('THz'), ylabel('Power')
    title('Power vs f (THz)')
    
    
    
end

peak_amp_db = [log(p(1)), log(y_max)];
peak_loc_nm = [3e17/p(2), 3e17/x(y_max_pos) ];

peak_dev_nm = [(p(3)*(peak_loc_nm(1)^2)/3e17), ...
    (y_mean_dev*(peak_loc_nm(2)^2)/3e17) ];

end