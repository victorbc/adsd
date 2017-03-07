% format long
path = 'D:\Google Drive\ADSD\local - coleta 03_03\';
f = dir([path '\*.csv']);

% numel(f)

cpu = [];
request_time = [];
db_time = [];
memory_usage = [];
total_time = [];

for k = 1:numel(f)
  file = strcat(path,f(k).name);

  table = csvread(char(file),1,2);
  
  cpu_part = table(:,1);
  request_time_part = table(:,2);
  db_time_part = table(:,3);
  memory_usage_part = table(:,4);
  total_time_part = table(:,5);
  
  
  cpu = cat(1, cpu, cpu_part);
  request_time = cat(1, request_time, request_time_part);
  db_time = cat(1, db_time, db_time_part);
  memory_usage = cat(1, memory_usage, memory_usage_part);
  total_time = cat(1, total_time, total_time_part);
   
end


% Dispersão dos dados
stats_cpu = [iqr(cpu),mad(cpu),range(cpu),std(cpu)];
stats_request_time = [iqr(request_time),mad(request_time),range(request_time),std(request_time)];
stats_db_time = [iqr(db_time),mad(db_time),range(db_time),std(db_time)];
stats_memory_usage = [iqr(memory_usage),mad(memory_usage),range(memory_usage),std(memory_usage)];
stats_total_time = [iqr(total_time),mad(total_time),range(total_time),std(total_time)];

% Média
media_cpu = mean(cpu);
media_request_time = mean(request_time);
media_db_time = mean(db_time);
media_memory_usage = mean(memory_usage);
media_total_time = mean(total_time);

% Min
min_cpu = min(cpu);
min_request_time = min(request_time);
min_db_time = min(db_time);
min_memory_usage = min(memory_usage);
min_total_time = min(total_time);

% Max
max_cpu = max(cpu);
max_request_time = max(request_time);
max_db_time = max(db_time);
max_memory_usage = max(memory_usage);
max_total_time = max(total_time);

% Mediana
median_cpu = median(cpu);
median_request_time = median(request_time);
median_db_time = median(db_time);
median_memory_usage = median(memory_usage);
median_total_time = median(total_time);

% Tempo total
soma_total_time = sum(total_time);

% Quartis
quartis_cpu = prctile(cpu,[25 50 75],1);
quartis_request_time = prctile(request_time,[25 50 75],1);
quartis_db_time = prctile(db_time,[25 50 75],1);
quartis_memory_usage = prctile(memory_usage,[25 50 75],1);
quartis_total_time = prctile(total_time,[25 50 75],1);
  
  


% Print de resultados

fprintf('\nCPU:\n')
fprintf('Min:       %d\n', min_cpu);
fprintf('Max:       %d\n', max_cpu);
fprintf('Media:     %d\n', media_cpu);
fprintf('1 Quartil: %d\n', quartis_cpu(1,1));
fprintf('Mediana:   %d\n', quartis_cpu(2,1));
fprintf('3 Quartil: %d\n', quartis_cpu(3,1));
fprintf('Dispersão dos dados: \n   II    -    DMA    -    DA    -    DP \n%s\n', mat2str(stats_cpu,5));


fprintf('\nTempo de Resposta da requisição:\n')
fprintf('Min:       %d\n', min_request_time);
fprintf('Max:       %d\n', max_request_time);
fprintf('Media:     %d\n', media_request_time);
fprintf('1 Quartil: %d\n', quartis_request_time(1,1));
fprintf('Mediana:   %d\n', quartis_request_time(2,1));
fprintf('3 Quartil: %d\n', quartis_request_time(3,1));
fprintf('Dispersão dos dados: \n   II    -    DMA    -    DA    -    DP \n%s\n', mat2str(stats_request_time,5));


fprintf('\nTempo de Resposta do BD:\n')
fprintf('Min:       %d\n', min_db_time);
fprintf('Max:       %d\n', max_db_time);
fprintf('Media:     %d\n', media_db_time);
fprintf('1 Quartil: %d\n', quartis_db_time(1,1));
fprintf('Mediana:   %d\n', quartis_db_time(2,1));
fprintf('3 Quartil: %d\n', quartis_db_time(3,1));
fprintf('Dispersão dos dados: \n   II    -    DMA    -    DA    -    DP \n%s\n', mat2str(stats_db_time,5));

fprintf('\nMemória:\n')
fprintf('Min:       %d\n', min_memory_usage);
fprintf('Max:       %d\n', max_memory_usage);
fprintf('Media:     %d\n', media_memory_usage);
fprintf('1 Quartil: %d\n', quartis_memory_usage(1,1));
fprintf('Mediana:   %d\n', quartis_memory_usage(2,1));
fprintf('3 Quartil: %d\n', quartis_memory_usage(3,1));
fprintf('Dispersão dos dados: \n   II    -    DMA    -    DA    -    DP \n%s\n', mat2str(stats_memory_usage,5));

fprintf('\nTempo total: %d\n',soma_total_time);


