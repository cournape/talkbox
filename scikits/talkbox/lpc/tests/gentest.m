% Matlab script to generate test data

x = reshape(linspace(1, 88, 88), 11, 8).';

x1_0 = levinson(x.', 0);
x1_1 = levinson(x.', 1);
x1_5 = levinson(x.', 5);
x1_10 = levinson(x.', 10);

x0_0 = levinson(x, 0).';
x0_1 = levinson(x, 1).';
x0_5 = levinson(x, 5).';
x0_7 = levinson(x, 7).';

save('lpc5.mat', 'x0_0', 'x0_1', 'x0_5', 'x0_7');
save('lpc5.mat', 'x1_0', 'x1_1', 'x1_5', 'x1_10', '-append');
save('lpc5.mat', 'x', '-append');
