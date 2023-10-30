

#include<iostream>
#include<string>
#include<vector>

using namespace std;

class ChinPoPomon
{
private:
	const char *type;
	string nickname;
	int curr_level;
	int curr_xp;
	void init_level_xp()	{
		this->curr_level = (rand() % 1000);
		this->curr_xp = (rand() % 1000);
	}
public:
	ChinPoPomon():nickname(NULL), type(NULL)	{
		init_level_xp();
	}
	ChinPoPomon(const char *type, string nickname)	{
		this->type = type;
		this->nickname = nickname;
	}
	void view_stats()	{
		cout << "Type: " << this->type << endl;
		cout << "Current Level: " << this->curr_level << endl;
		cout << "Current XP: " << this->curr_xp << endl;
		this->speak();

	}
	void speak()	{
		cout << this->nickname << ", " << this->nickname << "!" << endl;
	}
};


string my_name;
ChinPoPomon *my_pocket[6];


void init()	{
	srand(time(0));
	setvbuf(stdout, NULL, _IONBF, 0);
}

void print_menu()	{
	cout << "=====ChinPoPomon Lab=====" << endl;
	cout << "1. Create ChinPoPomon" << endl;
	cout << "2. Enter pc" << endl;
	cout << "3. Restart game" << endl;
	cout << "4. Turnoff game" << endl;
	cout << "=========================" << endl;
	cout << "Choice: ";
}

void print_pc_menu()	{
	cout << "=======Tommy's PC=======" << endl;
	cout << "1. Deposit ChinPoPomon" << endl;
	cout << "2. Withdraw ChinPoPomon" << endl;
	cout << "3. View stats of ChinPoPomon" << endl;
	cout << "4. Exit PC" << endl;
	cout << "========================" << endl;
	cout << "PC Choice: ";
}

const char* choose_type()	{
	cout << "1. Brute" << endl;
	cout << "2. Agile" << endl;
	cout << "3. Intelligent" << endl;
	cout << "4. Sneaky" << endl;
	cout << "Type Choice: ";
	int choice;
	cin >> choice;
	switch(choice)	{
		case 1:
			return "Brute";
		case 2:
			return "Agile";
		case 3:
			return "Intelligent";
		case 4:
			return "Sneaky";
		default:
			return "None";
	}
}

void create_ChinPoPomon(vector<ChinPoPomon*> &pc)	{
	string nickname;
	const char* type;
	cout << "Prof. Kinny: This is the ChinPoPomon Lab" << endl;
	cout << "Prof. Kinny: Here you can create a ChinPoPomon, give it and name and a type!" << endl;
	cout << "Prof. Kinny: First things first, what type of ChinPoPomon do you want?" << endl;
	type = choose_type();
	cout << "Prof. Kinny: What do you wish to name this ChinPoPomon?" << endl;
	cout << "Name: ";
	cin >> nickname;
	cout << "Prof. Kinny: What a wonderful name!" << endl;
	ChinPoPomon *new_ChinPoPomon = new ChinPoPomon(type, nickname);
	bool in_pocket = false;
	for(int i = 0; i < 6; i++)	{
		if(my_pocket[i] == NULL)	{
			my_pocket[i] = new_ChinPoPomon;
			in_pocket = true;
			break;
		}
	}
	if(!in_pocket)	{
		cout << "Prof. Kinny: It seems you have no more space in your pocket, so this one will go into the pc" << endl;
		pc.push_back(new_ChinPoPomon);
	}
	cout << "Prof. Kinny: Congrats you have successfully created a ChinPoPomon!\n" << endl;
}

void deposit_ChinPoPomon(vector<ChinPoPomon*> &pc)	{
	int choice;
	cout << "Choose pocket index: ";
	cin >> choice;
	if(choice > 5)	{
		cout << "Prof. Kinny: This isn't the time to do that!" << endl;
		return;
	}
	if(my_pocket[choice] != NULL)	{
		bool has_space = false;
		for (int i = 0; i < pc.size(); ++i)	{
			if(pc[choice] == nullptr)	{
				pc[choice] = my_pocket[choice];
				has_space = true;
				break;
			}
		}
		if(!has_space)
			pc.push_back(my_pocket[choice]);
		my_pocket[choice] = NULL;
		cout << "ChinPoPomon deposited successfully." << endl;
		return;
	}
	cout << "Prof. Kinny: This isn't the time to do that!" << endl;
	return;
}

void withdraw_ChinPoPomon(vector<ChinPoPomon*> &pc)	{
	int choice;
	cout << "Choose pc index: " << endl;
	cin >> choice;
	if(choice < pc.size())	{
		bool in_pocket = false;
		for (int i = 0; i < 6; ++i)	{
			if(my_pocket[i] == NULL)	{
				my_pocket[i] = pc[choice];
				pc[choice] = nullptr;
				in_pocket = true;
				cout << "ChinPoPomon withdrew successfully." << endl;
				break;
			}
		}
		if(!in_pocket)	{
			cout << "Pocket full" << endl;
		}
		return;
	}
	cout << "Prof. Kinny: This isn't the time to do that!" << endl;
	return;
}

void view_stats(vector<ChinPoPomon*> &pc)	{
	int choice;
	cout << "Choose pc index: " << endl;
	cin >> choice;
	if(choice < pc.size())	{
		pc[choice]->view_stats();
		return;
	}
	cout << "Prof. Kinny: This isn't the time to do that!" << endl;
	return;
}

void enter_pc(vector<ChinPoPomon*> &pc)	{
	cout << "Prof. Kinny: This is Tommy's PC" << endl;
	cout << "Prof. Kinny: You can interact with all your ChinPoPomon here\n" << endl;
	int choice;
	while(1)	{
		print_pc_menu();
		cin >> choice;
		switch(choice)	{
			case 1:
				deposit_ChinPoPomon(pc);
				break;
			case 2:
				withdraw_ChinPoPomon(pc);
				break;
			case 3:
				view_stats(pc);
				break;
			case 4:
				return;
			default:
				cout << "Prof. Kinny: This isn't the time to do that!" << endl;
				break;
		}
	}
}

bool play_game()	{
	vector<ChinPoPomon*> pc;
	int choice;
	while(1)	{
		print_menu();
		cin >> choice;
		switch(choice)	{
			case 1:
				create_ChinPoPomon(pc);
				break;
			case 2:
				enter_pc(pc);
				break;
			case 3:
			case 4:
				for (int i = 0; i < 6; ++i)
					my_pocket[i] = NULL;
				for (int i = 0; i < pc.size(); ++i)
					delete pc[i];	// Prevent memory leaks
				if(choice == 3)
					return true;
				return false;
			default:
				cout << "Prof. Kinny: This isn't the time to do that!" << endl;
				break;
		}
	}
}

int main(int argc, char const *argv[])
{
	init();
	do
	{
		cout << "Prof. Kinny: Hello, what is your name? ";
		cin >> my_name;
		cout << "Prof. Kinny: Hello, " << my_name << "!" << endl;
		cout << "Prof. Kinny: Welcome to the ChinPoPomon Lab!\n" << endl;
	} while (play_game());
	return 0;
}