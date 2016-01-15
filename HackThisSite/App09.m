%% play button

[wavPlay, fs] = wavread('play.wav');

Ts=1/fs;
figure, stem(wavPlay);
% measure half period (n1 to n2) on graph
n1 = 1164; n2 = 1404;
Thalf1 = (n2-n1)*Ts; % actual time
f1 = 1/(2*Thalf1); % = 100
% in the same way
f2 = 500;
f3 = 1000;

%% buttons 123
% follow the same approach and find

ff1 = 200;
ff2 = 600;
ff3 = 1100;
