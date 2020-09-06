/*********************************************
 * OPL 12.9.0.0 Model
 * Author: 24100
 * Creation Date: 2020年4月15日 at 下午7:37:13
 *********************************************/
{string} Products = ...; //7种产品的编号
{string} Machines = ...; //5类机器的名称
int Num_months =...; //月份数
range Months = 1..Num_months;

float Time_consume[Machines][Products] = ...; //每种产品需要花费每种机器的工时
int Market_lim[Months][Products] = ...; //每个月每种产品最多销售多少
int Value[Products] = ...; //每种产品单价
int Num_machines[Machines] = ...; //每一类机器的数量
int Num_maint[Machines] = ...; //6个月里面需要维修的机器数目
float Stroe_cost = ...; //单件产品库存开销
int Start_store = ...; //开始时库存
int End_store = ...; //6月底要求库存
int Max_store = ...; //每种产品每月最大库存量
int Work_hours = ...; //每台机器一个月工作时长:16*24=384

dvar int+ Produce[Products][Months]; //待求的每月产量，非负整数
dvar int+ Sell[p in Products][m in Months] in 0..Market_lim[m][p]; //待求的每月销量，非负整数
dvar int+ Store[Products][0..Num_months] in 0..Max_store; //每月的库存量
dvar int+ Maint[i in Machines][m in Months] in 0..Num_machines[i];

dexpr float Profit = sum (p in Products, m in Months) Value[p] * Sell[p][m]; //销售额
dexpr float Cost = sum (p in Products, m in Months) Stroe_cost * Store[p][m]; //成本
maximize //最大化净利润
	Profit - Cost;

subject to
{
	//每台机器在6个月里面至少都要维修
	forall(i in Machines)
	  sum(m in Months) Maint[i][m] >= Num_maint[i];

	//每个月，每一种商品所花的工时不应该超过该月机器的总工时
	forall(m in Months, i in Machines)
	    sum(p in Products) Time_consume[i][p] * Produce[p][m] + Work_hours * Maint[i][m] <= Work_hours * Num_machines[i];
	 
	//本月库存 = 上月库存 + 本月生产 - 本月销售
	forall(p in Products, m in Months)
	  Store[p][m] == Store[p][m-1] + Produce[p][m] - Sell[p][m];
	  
	//初始库存，结束时库存
	forall(p in Products)
	  {
	  	Store[p][0] == Start_store;
	  	Store[p][Num_months] == End_store;
	  }
}