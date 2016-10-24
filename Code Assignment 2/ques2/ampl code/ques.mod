set P;

param a1 {j in P};
param a2 {j in P};
param a3 {j in P};

param b;

param c {j in P};
param u {j in P};

var X {j in P};
maximize Total_Profit: sum {j in P} c[j] * X[j];

subject to One: sum {j in P} a1[j] * X[j] <= b;
subject to Two: sum {j in P} a2[j] * X[j] <= b;
subject to Three: sum {j in P} a3[j] * X[j] <= b;

subject to Limit {j in P}: 0 <= X[j] <= u[j];