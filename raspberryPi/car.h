#ifndef SC_CAR
#define SC_CAR
#include "common.h"
#include "mcu.h"

namespace hyd_15th
{

	class Car{
		private:
			//double room_temp;									���� ����
			
		public:
			Car(){		}										//�⺻������
			Mcu controller;										//Mcu class ����
			
//			double get_room_temp(){return room_temp;}			���� get�Լ� ����
//			void set_room_temp(double num){room_temp = num;}	���� set�Լ� ����

			void print();										//�ʿ� �Լ��� ���� ( ���Ǵ� cpp���Ͽ��� ��. )

			
			void setup_raspberry();
			void gpio_setting(); 

	};

}
#endif /* SC_CAR */