# Dungeons and Dragons bot
# Tracks world state and periodically updates to party to increase immersiveness and role-playing 

# Weather can be sunny, partly sunny, partly cloudy, cloudy, raining, snowing, hailing, thunderstorming, blizzard, hurricane (0-9); wind is based on Beaufort numbers (https://www.rochesterfirst.com/weather/weather-blog/breezy-gusty-and-windy-whats-the-difference/)
# Time will track the gameclock and date
# Map will track locations of places of interest, players, and NPCs

class World:
    def __init__(self, w=tuple(), t=int(0), m=0):
        self.weather = w
        self.time = int(t)
        self.map = m

        self.weather_sky_dict = {0:"It's sunny.", 1:"It's partly sunny.", 2:"It's partly cloudy.", 3:"It's cloudy.", 4:"It's raining", 5:"It's snowing :3", 6:"It's hailing!!", 7:"It's thunderstorming!!", 8:"THERE'S A BLIZZARD!!!", 9:"THERE'S A HURRICANE", 10:"It's foggy."}
        self.weather_wind_dict = {0:"The wind is calm.", 1:"There's a light breeze."}
        self.time_list = [['January', 'February', 'March', 'April', 'May', 'June','July', 'August', 'September', 'October', 'November', 'December'],
                          ['zero',"First","Second","Third","Fourth","Fifth","Sixth","Seventh","Eighth","Ninth","Tenth","Eleventh","Twelfth","Thirteenth","Fourteenth","Fifteenth","Seventeenth","Eighteenth","Nineteenth","Twentieth","Twenty First","Twenty Second","Twenty Third","Twenty Fourth","Twenty Fifth","Twenty Sixth","Twenty Seventh","Twenty Eighth","Twenty Ninth","Thirtieth","Thirty First","Thirty Second"]
                        ]

    # Pass tuple (sky int, wind int)
    def m_weather(self, w):
        sky=w[0]
        wind=w[1]        

        # Sunny to cloudy works in a chain, and then weather effects can happen when it's cloudy
        # Wind is average (0-6)

        # If it's cloudy, it can turn into either rain or snow
        # Wind can pick up (0-8)

        # If it's raining and cold, it can turn into hail
        # No wind change

        # If it's sunny or partly sunny shortly after rain, a rainbow can appear
        # Wind can die down (0-6)
        
        print(self.weather_sky_dict[sky])
        print(self.weather_wind_dict[wind])


    def time():
        pass

    def map():
        pass

"""
TODO
clock
map
sun and moon phases
finish weather_m
"""