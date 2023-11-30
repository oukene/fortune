"""Constants for the Detailed Hello World Push integration."""
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

# This is the internal name of the integration, it should also match the directory
# name for the integration.
DOMAIN = "fortune"
NAME = "fortune"
VERSION = "1.0.0"

CONF_ZODIAC = "zodiac"
CONF_CONSTELLATION = "constellation"
CONF_REFRESH_INVERVAL = "refresh_interval"

DEFAULT_REFRESH_INTERVAL = 360

KR_NAME = "kr_name"
ICON = "icon"
SEARCH_KEYWORD = KR_NAME

TODAY = 0
TOMORROW = 1
WEEK = 2
MONTH = 3

ENABLE_FORTUNE_LIST = {
    TODAY: "enable_today",
    TOMORROW: "enable_tomorrow",
    WEEK: "enable_week",
    MONTH: "enable_month"
}

FORTUNE_LIST = {
    TODAY: "오늘",
    TOMORROW: "내일",
    WEEK: "이번주",
    MONTH: "이번달"
}

ICON_URL_BASE = "https://search.pstatic.net/common?type=o&size=94x94&quality=90&direct=true&src=http%3A%2F%2Fsstatic.naver.net%2Fkeypage%2Foutside%2Fsign%2Fimg%2F20140305%2Fimg_b_"

BASE_URL = "https://search.naver.com/search.naver?query="

ZODIAC_LIST = {
    "Rat": {
        KR_NAME: "쥐띠운세",
        ICON: "zodiac01.png"
    },
    "Ox": {
        KR_NAME: "소띠운세",
        ICON: "zodiac02.png"
    },
    "Tiger": {
        KR_NAME: "호랑이띠운세",
        ICON: "zodiac03.png"
    },
    "Rabbit": {
        KR_NAME: "토끼띠운세",
        ICON: "zodiac04.png"
    },
    "Dragon": {
        KR_NAME: "용띠운세",
        ICON: "zodiac05.png"
    },
    "Snake": {
        KR_NAME: "뱀띠운세",
        ICON: "zodiac06.png"
    },
    "Horse": {
        KR_NAME: "말띠운세",
        ICON: "zodiac07.png"
    },
    "Lamb": {
        KR_NAME: "양띠운세",
        ICON: "zodiac08.png"
    },
    "Monkey": {
        KR_NAME: "원숭이띠운세",
        ICON: "zodiac09.png"
    },
    "Rooster": {
        KR_NAME: "닭띠운세",
        ICON: "zodiac10.png"
    },
    "Dog": {
        KR_NAME: "개띠운세",
        ICON: "zodiac11.png"
    },
    "Pig": {
        KR_NAME: "돼지띠운세",
        ICON: "zodiac12.png"
    },
}

CONSTELLATION_LIST = {
    "Aquarius": {
        KR_NAME: "물병자리운세",
        ICON: "sign01.png",
    },
    "Pisces": {
        KR_NAME: "물고기자리운세",
        ICON: "sign02.png",
    },
    "Aries": {
        KR_NAME: "양자리운세",
        ICON: "sign03.png",
    },
    "Taurus": {
        KR_NAME: "황소자리운세",
        ICON: "sign04.png",
    },
    "Gemini": {
        KR_NAME: "쌍둥이자리운세",
        ICON: "sign05.png",
    },
    "Cancer": {
        KR_NAME: "게자리운세",
        ICON: "sign06.png",
    },
    "Leo": {
        KR_NAME: "사자자리운세",
        ICON: "sign07.png",
    },
    "Virgo": {
        KR_NAME: "처녀자리운세",
        ICON: "sign08.png",
    },
    "Libra": {
        KR_NAME: "천칭자리운세",
        ICON: "sign09.png",
    },
    "Scorpio": {
        KR_NAME: "전갈자리운세",
        ICON: "sign10.png",
    },
    "Sagittarius": {
        KR_NAME: "궁수자리운세",
        ICON: "sign11.png",
    },
    "Capricorn": {
        KR_NAME: "염소자리운세",
        ICON: "sign12.png",
    },
}



REFRESH_MIN = 60

