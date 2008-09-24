[a, fs]  = wavread('voice-womanKP-01.wav');

ra = resample(a, 1, 2);
fs = fs * 0.5;

frame = ra(4001:4001+512);

periodogram(frame, [], 'onesided', 2048, fs);
hold on;
pyulear(frame, 12, 2048, fs, 'onesided');
