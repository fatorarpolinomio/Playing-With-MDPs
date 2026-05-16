% 1 2 3 4 5 6
% o         

% dados:
%  D1: 1 2 3
%  D2: 1 2

% MDP : S, A, T, R

S = [1 2 3 4 5 6];
A = [1 2];

% T: S x A -> (S->[0,1])
% T: S x A x S -> [0,1]

T = cell(2,1);

T{1} = [0 1/3 1/3 1/3 0 0;
      0 0 1/3 1/3 1/3 0;
      0 0 0 1/3 1/3 1/3;
      0 0 0 0 2/3 1/3;
      0 0 0 1/3 1/3 1/3;
      0 0 0 0 0 1; 
      ];

T{2} = [0 1/2 1/2 0 0 0;
      0 0 1/2 1/2 0 0;
      0 0 0 1/2 1/2 0;
      0 0 0 0 1/2 1/2;
      0 0 0 0 1/2 1/2;
      0 0 0 0 0 1; 
      ];

% R: S -> R

R = [-1 -1 -1 -1 -1 0]';

gamma = 1;

% Value Iteration

%V <- max { R_a + gamma* T_a * V }

V = zeros(length(S),1);
for i = 1:100
  Q = zeros(length(S),length(A));
  for a  = A
%    Q(:,a) = R + gamma*T{a}*V;
    for s = S
      Q(s,a) = R(s);
      for ss = S
        Q(s,a) = Q(s,a) + gamma*T{a}(s,ss)*V(ss);
      endfor
    endfor
  endfor
  [V, politica] = max(Q,[],2);
endfor

