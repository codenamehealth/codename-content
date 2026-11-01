import sys; sys.path.insert(0,'../pixellab')
import jobs
ups=jobs.upload(['vit_style.png']); st=ups['vit_style.png']
J=[('hall','create_image_pro',{'description':'inside a grand castle hallway leading to the boss room, side view, stone brick back wall with tall arched windows showing night sky, red carpet runner on a stone floor, wall torches with warm light, hanging blue banners, JRPG background, no characters','width':360,'height':640,'no_background':False,'style_image_url':st,'style_copy':['color_palette','outline','shading','detail']},'hall')]
print(jobs.run_many(J,1))
