#include "stm32f10x.h" // Device header
#include "Delay.h"

int main(void)
{
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);

	GPIO_InitTypeDef _gpio;
	_gpio.GPIO_Mode = GPIO_Mode_Out_PP;
	_gpio.GPIO_Pin = GPIO_Pin_0 | GPIO_Pin_1;
	_gpio.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOB, &_gpio);

	while (1)
	{
		// GPIO_WriteBit(GPIOA, GPIO_Pin_0, (BitAction)0);
		// Delay_ms(500);
		// GPIO_WriteBit(GPIOA, GPIO_Pin_0, (BitAction)1);
		// Delay_ms(500);

		GPIO_ResetBits(GPIOB, GPIO_Pin_1);
		Delay_ms(500);
		GPIO_SetBits(GPIOB, GPIO_Pin_1);
		Delay_ms(500);

		GPIO_WriteBit(GPIOB, GPIO_Pin_0, Bit_RESET);
		Delay_ms(500);
		GPIO_WriteBit(GPIOB, GPIO_Pin_0, Bit_SET);
		Delay_ms(500);
	}
}
