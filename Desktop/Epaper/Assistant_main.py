# -*- coding:utf-8 -*-

from weather import *
from news import *
from display import *
import json
import ast
import calendar
import time
import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os

lat = "52.2" #Enter your own
lon = "21.0" #Enter your own
api_key_weather = "" #Enter your own
api_key_news = "" #Enter your own
debug = 0
if debug ==0:
    import epd7in5_V2
else:
    pass

def map_resize(val, in_mini, in_maxi, out_mini, out_maxi):
    if in_maxi - in_mini != 0:
        out_temp = (val - in_mini) * (out_maxi - out_mini) // (in_maxi - in_mini) + out_mini
    else:
        out_temp = out_mini
    return out_temp


def main():
    ##################################################################################################################
    # FRAME
    display.draw_black.rectangle((5, 5, 795, 475), fill=255, outline=0, width=2)  # INNER FRAME
    display.draw_black.line((527, 5, 527, 350), fill=0, width=1)  # VERTICAL SEPARATION
    display.draw_black.line((350, 5, 350, 475), fill=0, width=1)  # VERTICAL SEPARATION slim
    display.draw_black.line((350, 350, 795, 350), fill=0, width=1)  # HORIZONTAL SEPARATION
    display.draw_black.line((5, 268, 350, 268), fill=0, width=1)  # HORIZONTAL SEPARATION

    # UPDATED AT
    display.draw_black.text((10, 8), "Data " + weather.current_time(), fill=0, font=font12)

    ###################################################################################################################
    # CURRENT WEATHER
    display.draw_icon(20, 50, "r", 75, 75,
                      weather.weather_description(weather.current_weather())[0])  # CURRENT WEATHER ICON
    display.draw_black.text((120, 25), weather.current_temp(), fill=0, font=font48)  # CURRENT TEMP
    display.draw_black.text((235, 25), weather.current_hum(), fill=0, font=font48)  # CURRENT HUM
    display.draw_black.text((241, 13), "Wilgotność", fill=0, font=font16)  # LABEL "HUMIDITY"
    display.draw_black.text((130, 76), weather.current_wind()[0] + " " + weather.current_wind()[1], fill=0, font=font16)

    display.draw_icon(120, 105, "b", 35, 35, "sunrise")  # SUNRISE ICON
    display.draw_black.text((160, 110), weather.current_sunrise(), fill=0, font=font16)  # SUNRISE TIME
    display.draw_icon(220, 105, "b", 35, 35, "sunset")  # SUNSET ICON
    display.draw_black.text((260, 110), weather.current_sunset(), fill=0, font=font16)  # SUNSET TIME

    ###################################################################################################################
    # HOURLY FORECAST
    display.draw_black.text((30, 143), "+3h", fill=0, font=font16)  # +3h LABEL
    display.draw_black.text((150, 143), "+6h", fill=0, font=font16)  # +6h LABEL
    display.draw_black.text((270, 143), "+12h", fill=0, font=font16)  # +12h LABEL
    # 3H
    display.draw_icon(25, 165, "r", 50, 50,
                      weather.weather_description(weather.hourly_forecast()["+3h"]["id"])[0])  # +3H WEATHER ICON
    display.draw_black.text((25, 216), weather.weather_description(weather.hourly_forecast()["+3h"]["id"])[1], fill=0,
                            font=font12)  # WEATHER DESCRIPTION +3h
    display.draw_black.text((35, 227), weather.hourly_forecast()["+3h"]["temp"], fill=0, font=font16)  # TEMP +3H
    display.draw_black.text((35, 243), weather.hourly_forecast()["+3h"]["pop"], fill=0, font=font16)  # POP +3H
    # +6h
    display.draw_icon(145, 165, "r", 50, 50,
                      weather.weather_description(weather.hourly_forecast()["+6h"]["id"])[0])  # +6H WEATHER ICON
    display.draw_black.text((145, 216), weather.weather_description(weather.hourly_forecast()["+6h"]["id"])[1], fill=0,
                            font=font12)  # WEATHER DESCRIPTION +6h
    display.draw_black.text((155, 227), weather.hourly_forecast()["+6h"]["temp"], fill=0, font=font16)  # TEMP +6H
    display.draw_black.text((155, 243), weather.hourly_forecast()["+6h"]["pop"], fill=0, font=font16)  # POP +6H
    # +12h
    display.draw_icon(265, 165, "r", 50, 50,
                      weather.weather_description(weather.hourly_forecast()["+12h"]["id"])[0])  # +12H WEATHER ICON
    display.draw_black.text((265, 216), weather.weather_description(weather.hourly_forecast()["+12h"]["id"])[1], fill=0,
                            font=font12)  # WEATHER DESCRIPTION +12h
    display.draw_black.text((275, 227), weather.hourly_forecast()["+12h"]["temp"], fill=0, font=font16)  # TEMP +12H
    display.draw_black.text((275, 243), weather.hourly_forecast()["+12h"]["pop"], fill=0, font=font16)  # POP +12H

    ###################################################################################################################
    # DAILY FORECAST
    # +24h
    display.draw_black.text((380, 5), "Warszawa", fill=0, font=font24)
    display.draw_black.text((360, 30), weather.daily_forecast()["+24h"]["date"], fill=0, font=font16)  # +24H DAY
    display.draw_icon(380, 50, "r", 50, 50,
                      weather.weather_description(weather.daily_forecast()["+24h"]["id"])[0])  # +24H WEATHER ICON
    display.draw_black.text((442, 50), weather.daily_forecast()["+24h"]["min"], fill=0, font=font14)
    display.draw_black.text((478, 50), " min.", fill=0, font=font14)  # +24H MIN TEMPERATURE
    display.draw_black.text((442, 65), weather.daily_forecast()["+24h"]["max"], fill=0, font=font14)
    display.draw_black.text((478, 65), " maks.", fill=0, font=font14)  # +24H MAX TEMPERATURE
    display.draw_black.text((442, 80), weather.daily_forecast()["+24h"]["pop"], fill=0, font=font14)
    display.draw_black.text((478, 80), " opady", fill=0, font=font14)  # +24H RAIN PROBABILITY

    # +48h
    display.draw_black.text((360, 105), weather.daily_forecast()["+48h"]["date"], fill=0, font=font16)  # +48H DAY
    display.draw_icon(380, 125, "r", 50, 50,
                      weather.weather_description(weather.daily_forecast()["+48h"]["id"])[0])  # +48H WEATHER ICON
    display.draw_black.text((442, 125), weather.daily_forecast()["+48h"]["min"], fill=0, font=font14)
    display.draw_black.text((478, 125), " min.", fill=0, font=font14)  # +48H MIN TEMPERATURE
    display.draw_black.text((442, 140), weather.daily_forecast()["+48h"]["max"], fill=0, font=font14)
    display.draw_black.text((478, 140), " maks.", fill=0, font=font14)  # +48H MAX TEMPERATURE
    display.draw_black.text((442, 155), weather.daily_forecast()["+48h"]["pop"], fill=0, font=font14)
    display.draw_black.text((478, 155), " opady", fill=0, font=font14)  # +48H RAIN PROBABILITY

    # +72h
    display.draw_black.text((360, 180), weather.daily_forecast()["+72h"]["date"], fill=0, font=font16)  # +72H DAY
    display.draw_icon(380, 200, "r", 50, 50,
                      weather.weather_description(weather.daily_forecast()["+72h"]["id"])[0])  # +72H WEATHER ICON
    display.draw_black.text((442, 200), weather.daily_forecast()["+72h"]["min"], fill=0, font=font14)
    display.draw_black.text((478, 200), " min.", fill=0, font=font14)  # +72H MIN TEMPERATURE
    display.draw_black.text((442, 215), weather.daily_forecast()["+72h"]["max"], fill=0, font=font14)
    display.draw_black.text((478, 215), " maks.", fill=0, font=font14)  # +72H MAX TEMPERATURE
    display.draw_black.text((442, 230), weather.daily_forecast()["+72h"]["pop"], fill=0, font=font14)
    display.draw_black.text((478, 230), " opady", fill=0, font=font14)  # +72H RAIN PROBABILITY

    # +96h
    display.draw_black.text((360, 255), weather.daily_forecast()["+96h"]["date"], fill=0, font=font16)  # +96H DAY
    display.draw_icon(380, 275, "r", 50, 50,
                      weather.weather_description(weather.daily_forecast()["+96h"]["id"])[0])  # +96H WEATHER ICON
    display.draw_black.text((442, 275), weather.daily_forecast()["+96h"]["min"], fill=0, font=font14)
    display.draw_black.text((478, 275), " min.", fill=0, font=font14)  # +96H MIN TEMPERATURE
    display.draw_black.text((442, 290), weather.daily_forecast()["+96h"]["max"], fill=0, font=font14)
    display.draw_black.text((478, 290), " maks.", fill=0, font=font14)  # +96H MAX TEMPERATURE
    display.draw_black.text((442, 305), weather.daily_forecast()["+96h"]["pop"], fill=0, font=font14)
    display.draw_black.text((478, 305), " opady", fill=0, font=font14)  # +96H RAIN PROBABILITY


    ###################################################################################################################
    #Calendar 
    mod_c_s_x = 20
    mod_c_s_y = 325
    def draw_cal_mod(cal_s_x_0, cal_s_y):
        cal_month = datetime.datetime.now().month
        cal_year = datetime.datetime.now().year
        cal_day = datetime.datetime.now().day
        cal_n_m = calendar.month_name[cal_month]
        cal_text = calendar.TextCalendar(calendar.MONDAY)
        cal_list = cal_text.monthdayscalendar(cal_year, cal_month)
        cal_s_x = cal_s_x_0

        display.draw_black.text((cal_s_x + 80, cal_s_y-58),str(cal_day)+' ' +str(cal_n_m) + ' ' + str(cal_year),
                  font=font24, fill=0)
        display.draw_black.text((cal_s_x, cal_s_y-25), 'PON    WT       ŚR      CZW        PT      SOB    NIEDZ',
                  font=font14, fill=0)

        for cal_x in range(len(cal_list)):
            for cal_y in (0, 1, 2, 3, 4, 5, 6):
                if cal_list[cal_x][cal_y] != 0:

                    if cal_list[cal_x][cal_y] == cal_day:
                        display.draw_black.rectangle((cal_s_x-5, cal_s_y, cal_s_x+22, cal_s_y+20), fill=0)
                        display.draw_black.text((cal_s_x, cal_s_y), str(
                            cal_list[cal_x][cal_y]), font=font14, fill=1, align='right')
                    else:
                        display.draw_black.text((cal_s_x, cal_s_y), str(
                            cal_list[cal_x][cal_y]), font=font14, fill=0, align='right')
                cal_s_x = cal_s_x + 50
            cal_s_x = cal_s_x_0
            cal_s_y = cal_s_y + 24
    draw_cal_mod(mod_c_s_x, mod_c_s_y)
    ####################################################################################################################
    #TO-DO-LIST
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creddir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'credentials')
    with open(os.path.join(creddir, 'dash_id.json'), "r") as rdash_id:
        data = json.load(rdash_id)
    gsheetjson = str(data["Tasklist"]["gsheet_json"])
    sheetname = str(data["Tasklist"]["sheetname"])

    def get_tasklist(gsheetjson, sheetname, creddir):
        """Pull down the tasklist columns from the given google sheet."""
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            str(os.path.join(creddir, str(gsheetjson))), scope)
        client = gspread.authorize(creds)
        sheet = client.open(str(sheetname))
        sheet_instance = sheet.get_worksheet(0)
        csv_a_vals = sheet_instance.col_values(1)[:30]
        csv_b_vals = sheet_instance.col_values(2)[:30]
        return csv_a_vals, csv_b_vals


    def draw_tasklist_mod(t_s_x, t_s_y, csv_a_vals, csv_b_vals, color):
        """Display the tasklist."""
        display.draw_black.text((t_s_x+90, t_s_y), "Do zrobienia (Arkusz google)",
                  font=font18, fill=color)
        t_s_y = t_s_y+32
        t_s_y_0 = t_s_y
        x = 1
        y = 1
        for i in range(1, len(csv_a_vals)):
            if str(csv_a_vals[i]) != "":
                if x <= 7:
                    display.draw_black.text((t_s_x, t_s_y), '- ' +
                              str(csv_a_vals[i]), font=font15, fill=color)
                    t_s_y = t_s_y + 25
                    x = x+1
        t_s_y = t_s_y_0
        for i in range(1, len(csv_b_vals)):
            if str(csv_b_vals[i]) != "":
                if y <= 7:
                    display.draw_black.text((t_s_x+225, t_s_y), '- ' +
                              str(csv_b_vals[i]), font=font15, fill=color)
                    t_s_y = t_s_y + 25
                    y = y+1


    def run_tasklist_mod(gsheetjson, sheetname, creddir, mod_tl_s_x, mod_tl_s_y, color):
        """Get and display the tasklist."""
        csv_a_values = []
        csv_b_values = []
        csv_a_values, csv_b_values = get_tasklist(gsheetjson, sheetname, creddir)
        draw_tasklist_mod(mod_tl_s_x, mod_tl_s_y, csv_a_values, csv_b_values, 0)
        csv_a_values.clear()
        csv_b_values.clear()
        
    mod_tl_s_x = 355
    mod_tl_s_y = 353
    run_tasklist_mod(gsheetjson, sheetname, creddir,mod_tl_s_x, mod_tl_s_y,  0)
    print('Tasklist loaded')

    ###################################################################################################################
    display.draw_black.text((585, 5), "Wiadomości", fill=0, font=font24)
    for i in range(5):
        if len(news.selected_title()) == 1:
            display.draw_black.text((532, 40), news.selected_title()[0], fill=0, font=font14)
            break
        else:
            if len(news.selected_title()[i]) <= 3 :
                for j in range(len(news.selected_title()[i])):
                    display.draw_black.text((532, 40 + j * 15 + i * 60), news.selected_title()[i][j], fill=0, font=font14)
            else:
                for j in range(2):
                    display.draw_black.text((532, 40 + j * 15 + i * 60), news.selected_title()[i][j], fill=0, font=font14)
                display.draw_black.text((532, 40 + 2 * 15 + i * 60), news.selected_title()[i][2] + "[...]", fill=0, font=font14)
      
    ###################################################################################################################
    print("Updating screen...")
    display.im_black.show()  
    print("\tPrinting...")

    time.sleep(2)
    epd.display(epd.getbuffer(display.im_black))
    time.sleep(2)	
    return True


if __name__ == "__main__":
    global been_reboot
    been_reboot=1
    while True:
        try:
            weather = Weather(lat, lon, api_key_weather)
            news = News()
            break
        except:
            current_time = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
            print("INITIALIZATION PROBLEM- @" + current_time)
            time.sleep(2)
    epd = epd7in5_V2.EPD()
    while True:
        # Defining objects
        current_time = time.strftime("%d/%m/%Y %H:%M", time.localtime())
        print("Begin update @" + current_time)
        print("Creating display")
        display = Display()
        # Update values
        weather.update()
        print("Weather Updated")
        news.update(api_key_news)
        print("News Updated")        
        print("Main program running...")
        epd.init()
        epd.Clear()
        main()
        print("Going to sleep...")
        epd.init()
        epd.sleep()
        print("Sleeping ZZZzzzzZZZzzz")
        print("Done")
        print("------------")
        time.sleep(600)

