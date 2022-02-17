from webwalking import WebWalking
from windowcapture import ShopRegion

walk1 = WebWalking('walking_lists\\123.pkl', 'map\\desert1.png')

walk1.walk(debugger=True)