import I2C_LCD_driver
from time import *

mylcd = I2C_LCD_driver.lcd()

fontdata1 = [      
        [ 0b00100, 
          0b00100, 
          0b00100, 
          0b00100, 
          0b00100, 
          0b11111, 
          0b01110, 
          0b00100 ],
]

mylcd.lcd_load_custom_chars(fontdata1)
mylcd.lcd_write(0x80)
mylcd.lcd_write_char(0)