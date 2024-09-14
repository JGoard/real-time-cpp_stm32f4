/******************************************************************************************
  Filename    : Clock.h
  
  Core        : ARM Cortex-M33 / RISC-V Hazard3
  
  MCU         : RP2350
    
  Author      : Chalandi Amine
 
  Owner       : Chalandi Amine
  
  Date        : 04.09.2024
  
  Description : Clock initialization header file for RP2350
  
******************************************************************************************/
#ifndef __RP2350_CLOCK_H__
#define __RP2350_CLOCK_H__

//=============================================================================
// Includes
//=============================================================================
#include <RP2350.h>

#include <Platform_Types.h>

#if defined(__cplusplus)
extern "C"
{
#endif

//=============================================================================
// Functions prototype
//=============================================================================
void RP2350_ClockInit(void);

#if defined(__cplusplus)
}
#endif

#endif /*__RP2350_CLOCK_H__*/
