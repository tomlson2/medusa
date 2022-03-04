import time
import random
from numpy import array
from vision import Vision
from regions import InventoryRegion, ScreenRegion


'''
about ~26k xp/hr ~6 hours 25 to 55
zoom 2 (middle), brightness 2, north, full up
go to western fruit stall in hosidious eastern house
stand on the top tile of the fruit stall
have inventory open and drop mode on
'''


inventory = InventoryRegion()
screen = ScreenRegion()
stall_region = array([(830,530,40,70)])

apple = Vision('Needle\\thieving\\fruit_stall\\apple.png')
bannana = Vision('Needle\\thieving\\fruit_stall\\bannana.png')
golo = Vision('Needle\\thieving\\fruit_stall\\golo.png')
jangerberries = Vision('Needle\\thieving\\fruit_stall\\jangerberries.png')
lemon = Vision('Needle\\thieving\\fruit_stall\\lemon.png')
lime = Vision('Needle\\thieving\\fruit_stall\\lime.png')
papaya = Vision('Needle\\thieving\\fruit_stall\\papaya.png')
pineapple = Vision('Needle\\thieving\\fruit_stall\\pineappple.png')
redberries = Vision('Needle\\thieving\\fruit_stall\\redberries.png')
strange = Vision('Needle\\thieving\\fruit_stall\\strange.png')
strawberry = Vision('Needle\\thieving\\fruit_stall\\strawberry.png')

fruit_list = [apple, bannana, golo, jangerberries, lemon, lime, papaya, pineapple, redberries, strange, strawberry]
start_time = time.time()
fruit_counter = 0


print('-------starting fruit stall thieving-------')
print('counting food in inventory...')
for i in range(len(fruit_list)):
    fruit_counter += inventory.amount(fruit_list[i], threshold=0.7)
    time.sleep(0.1)
print(f'food count: {fruit_counter}')

while True:
    print('thieving stalls...')
    while fruit_counter < 28:
        screen.click_region(stall_region)
        fruit_counter += 1
        chance = random.randrange(1,80)
        if chance > 70:
            time.sleep(random.normalvariate(1.5, 0.03))
        time.sleep(random.normalvariate(3.2, 0.02))
        
    print('dropping junk...')
    inventory.drop_list_vert(fruit_list)
    fruit_counter = 0
    
    # time
    current_time = (time.time() - start_time)
    current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
    print(f"run time: {current_time_format}")
    
    time.sleep(1.2)