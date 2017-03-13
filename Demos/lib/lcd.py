import lib.lcddriver as lcddriver

def clear_lcd():
    lcd = lcddriver.lcd()
    #clear the lcd

    lcd.lcd_clear()

def startup_lcd():
    lcd = lcddriver.lcd()
    #clear the lcd

    lcd.lcd_clear()
    #writing each line
    lcd.lcd_display_string("Turnip the Beets", 1)
    lcd.lcd_display_string("is initalizing...", 2)

def detected_lcd():
    lcd = lcddriver.lcd()

    #clear the lcd
    lcd.lcd_clear()
    #writing each line
    lcd.lcd_display_string("Detected a", 1)
    lcd.lcd_display_string("weight change!", 2)

def waiting_lcd():
    lcd = lcddriver.lcd()

    #clear the lcd
    lcd.lcd_clear()
    #writing each line
    lcd.lcd_display_string("Waiting...", 1)

def classified_lcd(label, mass):
    lcd = lcddriver.lcd()
    #clear the lcd
    lcd.lcd_clear()
    #writing each line
    lcd.lcd_display_string("Found a:", 1)
    lcd.lcd_display_string("{}".format(label), 2)
    lcd.lcd_display_string("mass:", 3)
    lcd.lcd_display_string("{} g".format(mass), 4)
def analyzing_lcd():
    lcd = lcddriver.lcd()
    #clear the lcd
    lcd.lcd_clear()
    #writing each line
    lcd.lcd_display_string("Analyzing...", 1)

def errorclass_lcd():
    lcd = lcddriver.lcd()
    #clear the lcd
    lcd.lcd_clear()
    #writing each line
    lcd.lcd_display_string("Failed to classify :(", 1)
