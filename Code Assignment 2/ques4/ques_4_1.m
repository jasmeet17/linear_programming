% primal simplex method

eps = 1e-7;

sigma = 10;
niters = 1000;

stop = 0;
k=0;
ms = zeros(niters,1);
ns = zeros(niters,1);
n0s = zeros(niters,1);
iters = zeros(niters,1);
opts = zeros(niters,1);
while k ~= niters
   m = round(10*exp(log(100)*rand()));  
   n = round(10*exp(log(100)*rand()));
 
   A = sigma*(randn(m,n));
%   y = round(sigma*rand(1,m));
%   z = round(sigma*rand(1,n));
%   c = y*A - z;
   b = sigma*abs(randn(m,1));
   c = sigma*randn(1,n);
   A = -A;    % to reflect subtraction from right-hand side
   AA = A;
   bb = b;
   cc = c;
   n0 = sum(cc>0);

   nonbasics = 1:n;
   basics = (n+1:n+m)';
   
   iter = 0;
   opt = 1;
   while max(c) > eps,
      [cj, col] = max(c);

      Acol = A(:,col);
      if sum(Acol<-eps) == 0,
	    opt = -1;  % unbounded
	    'unbounded'
	    break;
      end
%      [t, row0] = max(-Acol./b);
      nums = b.*(Acol<-eps);
      dens = -Acol.*(Acol<-eps);
      [t, row] = min(nums./dens);
%      if row0 ~= row,
%          row0
%	  row
%      end

      j = nonbasics(col);
      i = basics(row);

      Arow = A(row,:);
      a = A(row,col);
      A = A - Acol*Arow/a;
      A(row,:) = -Arow/a;
      A(:,col) = Acol/a;
      A(row,col) = 1/a;

      brow = b(row);
      b = b - brow*Acol/a;
      b(row) = -brow/a;

      ccol = c(col);
      c = c - ccol*Arow/a;
      c(col) = ccol/a;

      basics(row) = j;
      nonbasics(col) = i;
      iter = iter+1;
      if iter > 100*(m+n),
      	  opt = 0;  % iter limit
          break;
      end
   end
   if iter>0 & opt~=0,
      k = k+1
      ms(k) = m;
      ns(k) = n;
      n0s(k) = n0;
      iters(k) = iter;
      opts(k) = opt;
   elseif iter == 0,   % too easy
      AA
      bb
      cc
   else 	% cycling
      m, n, iter, opt
      % Save degenerate part for checking later
      A0 = AA(b==0,:);
      b0 = b(b==0);
      [m0, n] = size(A0);
%      [x,fval,exitflag] = linprog(cc,[-AA ; -eye(n)], [bb ; zeros(n,1)] );
%      break;
   end
end


iter
k


all = [ms ns iters opts];
save -ascii 'all' all;

% To make plots, call makeplots.m
% This file can be found at http://www.princeton.edu/~rvdb/LPbook/complexity/makeplots.m
% makeplots

figure(1);
hold off;
plot(min(ms(opts>0),ns(opts>0)), iters(opts>0),'b+');
hold on;
plot(min(ms(opts<0),ns(opts<0)), iters(opts<0),'gx');
title('Empirical Performance of the Simplex Method');
xlabel('min( m, n )');
ylabel('number of pivots');
legend('Problems with an optimal solution','Problems that are unbounded',...
		'Location','Northwest');