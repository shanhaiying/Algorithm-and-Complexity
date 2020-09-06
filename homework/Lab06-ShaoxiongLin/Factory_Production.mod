/*********************************************
 * OPL 12.9.0.0 Model
 * Author: 24100
 * Creation Date: 2020��4��15�� at ����7:37:13
 *********************************************/
{string} Products = ...; //7�ֲ�Ʒ�ı��
{string} Machines = ...; //5�����������
int Num_months =...; //�·���
range Months = 1..Num_months;

float Time_consume[Machines][Products] = ...; //ÿ�ֲ�Ʒ��Ҫ����ÿ�ֻ����Ĺ�ʱ
int Market_lim[Months][Products] = ...; //ÿ����ÿ�ֲ�Ʒ������۶���
int Value[Products] = ...; //ÿ�ֲ�Ʒ����
int Num_machines[Machines] = ...; //ÿһ�����������
int Num_maint[Machines] = ...; //6����������Ҫά�޵Ļ�����Ŀ
float Stroe_cost = ...; //������Ʒ��濪��
int Start_store = ...; //��ʼʱ���
int End_store = ...; //6�µ�Ҫ����
int Max_store = ...; //ÿ�ֲ�Ʒÿ���������
int Work_hours = ...; //ÿ̨����һ���¹���ʱ��:16*24=384

dvar int+ Produce[Products][Months]; //�����ÿ�²������Ǹ�����
dvar int+ Sell[p in Products][m in Months] in 0..Market_lim[m][p]; //�����ÿ���������Ǹ�����
dvar int+ Store[Products][0..Num_months] in 0..Max_store; //ÿ�µĿ����
dvar int+ Maint[i in Machines][m in Months] in 0..Num_machines[i];

dexpr float Profit = sum (p in Products, m in Months) Value[p] * Sell[p][m]; //���۶�
dexpr float Cost = sum (p in Products, m in Months) Stroe_cost * Store[p][m]; //�ɱ�
maximize //��󻯾�����
	Profit - Cost;

subject to
{
	//ÿ̨������6�����������ٶ�Ҫά��
	forall(i in Machines)
	  sum(m in Months) Maint[i][m] >= Num_maint[i];

	//ÿ���£�ÿһ����Ʒ�����Ĺ�ʱ��Ӧ�ó������»������ܹ�ʱ
	forall(m in Months, i in Machines)
	    sum(p in Products) Time_consume[i][p] * Produce[p][m] + Work_hours * Maint[i][m] <= Work_hours * Num_machines[i];
	 
	//���¿�� = ���¿�� + �������� - ��������
	forall(p in Products, m in Months)
	  Store[p][m] == Store[p][m-1] + Produce[p][m] - Sell[p][m];
	  
	//��ʼ��棬����ʱ���
	forall(p in Products)
	  {
	  	Store[p][0] == Start_store;
	  	Store[p][Num_months] == End_store;
	  }
}