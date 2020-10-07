# -*- coding: utf-8 -*-
"""Color Library

.. :doctest:

This module defines several color formats that can be converted to one or
another.

Formats
-------

HSL:
    3-uple of Hue, Saturation, Lightness all between 0.0 and 1.0

RGB:
    3-uple of Red, Green, Blue all between 0.0 and 1.0

HEX:
    string object beginning with '#' and with red, green, blue value.
    This format accept color in 3 or 6 value ex: '#fff' or '#ffffff'

WEB:
    string object that defaults to HEX representation or human if possible

Usage
-----

Several function exists to convert from one format to another. But all
function are not written. So the best way is to use the object Color.

Please see the documentation of this object for more information.

.. note:: Some constants are defined for convenience in HSL, RGB, HEX

"""

from __future__ import with_statement, print_function

import hashlib
import re
import sys

##
## Some Constants
##

## Soften inequalities and some rounding issue based on float
FLOAT_ERROR = 0.0000005

HEX_TO_XKCD_COLOR_NAMES = {
    ('#acc2d9'): ['cloudy_blue'],
    ('#56ae57'): ['dark_pastel_green'],
    ('#b2996e'): ['dust'],
    ('#a8ff04'): ['electric_lime'],
    ('#69d84f'): ['fresh_green'],
    ('#894585'): ['light_eggplant'],
    ('#70b23f'): ['nasty_green'],
    ('#d4ffff'): ['really_light_blue'],
    ('#65ab7c'): ['tea'],
    ('#952e8f'): ['warm_purple'],
    ('#fcfc81'): ['yellowish_tan'],
    ('#a5a391'): ['cement'],
    ('#388004'): ['dark_grass_green'],
    ('#4c9085'): ['dusty_teal'],
    ('#5e9b8a'): ['grey_teal'],
    ('#efb435'): ['macaroni_and_cheese'],
    ('#d99b82'): ['pinkish_tan'],
    ('#0a5f38'): ['spruce'],
    ('#0c06f7'): ['strong_blue'],
    ('#61de2a'): ['toxic_green'],
    ('#3778bf'): ['windows_blue'],
    ('#2242c7'): ['blue_blue'],
    ('#533cc6'): ['blue_with_a_hint_of_purple'],
    ('#9bb53c'): ['booger'],
    ('#05ffa6'): ['bright_sea_green'],
    ('#1f6357'): ['dark_green_blue'],
    ('#017374'): ['deep_turquoise'],
    ('#0cb577'): ['green_teal'],
    ('#ff0789'): ['strong_pink'],
    ('#afa88b'): ['bland'],
    ('#08787f'): ['deep_aqua'],
    ('#dd85d7'): ['lavender_pink'],
    ('#a6c875'): ['light_moss_green'],
    ('#a7ffb5'): ['light_seafoam_green'],
    ('#c2b709'): ['olive_yellow'],
    ('#e78ea5'): ['pig_pink'],
    ('#966ebd'): ['deep_lilac'],
    ('#ccad60'): ['desert'],
    ('#ac86a8'): ['dusty_lavender'],
    ('#947e94'): ['purpley_grey'],
    ('#983fb2'): ['purply'],
    ('#ff63e9'): ['candy_pink'],
    ('#b2fba5'): ['light_pastel_green'],
    ('#63b365'): ['boring_green'],
    ('#8ee53f'): ['kiwi_green'],
    ('#b7e1a1'): ['light_grey_green'],
    ('#ff6f52'): ['orange_pink'],
    ('#bdf8a3'): ['tea_green'],
    ('#d3b683'): ['very_light_brown'],
    ('#fffcc4'): ['egg_shell'],
    ('#430541'): ['eggplant_purple'],
    ('#ffb2d0'): ['powder_pink'],
    ('#997570'): ['reddish_grey'],
    ('#ad900d'): ['baby_shit_brown'],
    ('#c48efd'): ['liliac'],
    ('#507b9c'): ['stormy_blue'],
    ('#7d7103'): ['ugly_brown'],
    ('#fffd78'): ['custard'],
    ('#da467d'): ['darkish_pink'],
    ('#410200'): ['deep_brown'],
    ('#c9d179'): ['greenish_beige'],
    ('#fffa86'): ['manilla'],
    ('#5684ae'): ['off_blue'],
    ('#6b7c85'): ['battleship_grey'],
    ('#6f6c0a'): ['browny_green'],
    ('#7e4071'): ['bruise'],
    ('#009337'): ['kelley_green'],
    ('#d0e429'): ['sickly_yellow'],
    ('#fff917'): ['sunny_yellow'],
    ('#1d5dec'): ['azul'],
    ('#054907'): ['darkgreen'],
    ('#b5ce08'): ['green/yellow'],
    ('#8fb67b'): ['lichen'],
    ('#c8ffb0'): ['light_light_green'],
    ('#fdde6c'): ['pale_gold'],
    ('#ffdf22'): ['sun_yellow'],
    ('#a9be70'): ['tan_green'],
    ('#6832e3'): ['burple'],
    ('#fdb147'): ['butterscotch'],
    ('#c7ac7d'): ['toupe'],
    ('#fff39a'): ['dark_cream'],
    ('#850e04'): ['indian_red'],
    ('#efc0fe'): ['light_lavendar'],
    ('#40fd14'): ['poison_green'],
    ('#b6c406'): ['baby_puke_green'],
    ('#9dff00'): ['bright_yellow_green'],
    ('#3c4142'): ['charcoal_grey'],
    ('#f2ab15'): ['squash'],
    ('#ac4f06'): ['cinnamon'],
    ('#c4fe82'): ['light_pea_green'],
    ('#2cfa1f'): ['radioactive_green'],
    ('#9a6200'): ['raw_sienna'],
    ('#ca9bf7'): ['baby_purple'],
    ('#875f42'): ['cocoa'],
    ('#3a2efe'): ['light_royal_blue'],
    ('#fd8d49'): ['orangeish'],
    ('#8b3103'): ['rust_brown'],
    ('#cba560'): ['sand_brown'],
    ('#698339'): ['swamp'],
    ('#0cdc73'): ['tealish_green'],
    ('#b75203'): ['burnt_siena'],
    ('#7f8f4e'): ['camo'],
    ('#26538d'): ['dusk_blue'],
    ('#63a950'): ['fern'],
    ('#c87f89'): ['old_rose'],
    ('#b1fc99'): ['pale_light_green'],
    ('#ff9a8a'): ['peachy_pink'],
    ('#f6688e'): ['rosy_pink'],
    ('#76fda8'): ['light_bluish_green'],
    ('#53fe5c'): ['light_bright_green'],
    ('#4efd54'): ['light_neon_green'],
    ('#a0febf'): ['light_seafoam'],
    ('#7bf2da'): ['tiffany_blue'],
    ('#bcf5a6'): ['washed_out_green'],
    ('#ca6b02'): ['browny_orange'],
    ('#107ab0'): ['nice_blue'],
    ('#2138ab'): ['sapphire'],
    ('#719f91'): ['greyish_teal'],
    ('#fdb915'): ['orangey_yellow'],
    ('#fefcaf'): ['parchment'],
    ('#fcf679'): ['straw'],
    ('#1d0200'): ['very_dark_brown'],
    ('#cb6843'): ['terracota'],
    ('#31668a'): ['ugly_blue'],
    ('#247afd'): ['clear_blue'],
    ('#ffffb6'): ['creme'],
    ('#90fda9'): ['foam_green'],
    ('#86a17d'): ['grey/green'],
    ('#fddc5c'): ['light_gold'],
    ('#78d1b6'): ['seafoam_blue'],
    ('#13bbaf'): ['topaz'],
    ('#fb5ffc'): ['violet_pink'],
    ('#20f986'): ['wintergreen'],
    ('#ffe36e'): ['yellow_tan'],
    ('#9d0759'): ['dark_fuchsia'],
    ('#3a18b1'): ['indigo_blue'],
    ('#c2ff89'): ['light_yellowish_green'],
    ('#d767ad'): ['pale_magenta'],
    ('#720058'): ['rich_purple'],
    ('#ffda03'): ['sunflower_yellow'],
    ('#01c08d'): ['green/blue'],
    ('#ac7434'): ['leather'],
    ('#014600'): ['racing_green'],
    ('#9900fa'): ['vivid_purple'],
    ('#02066f'): ['dark_royal_blue'],
    ('#8e7618'): ['hazel'],
    ('#d1768f'): ['muted_pink'],
    ('#96b403'): ['booger_green'],
    ('#fdff63'): ['canary'],
    ('#95a3a6'): ['cool_grey'],
    ('#7f684e'): ['dark_taupe'],
    ('#751973'): ['darkish_purple'],
    ('#089404'): ['true_green'],
    ('#ff6163'): ['coral_pink'],
    ('#598556'): ['dark_sage'],
    ('#214761'): ['dark_slate_blue'],
    ('#3c73a8'): ['flat_blue'],
    ('#ba9e88'): ['mushroom'],
    ('#021bf9'): ['rich_blue'],
    ('#734a65'): ['dirty_purple'],
    ('#23c48b'): ['greenblue'],
    ('#8fae22'): ['icky_green'],
    ('#e6f2a2'): ['light_khaki'],
    ('#4b57db'): ['warm_blue'],
    ('#d90166'): ['dark_hot_pink'],
    ('#015482'): ['deep_sea_blue'],
    ('#9d0216'): ['carmine'],
    ('#728f02'): ['dark_yellow_green'],
    ('#ffe5ad'): ['pale_peach'],
    ('#4e0550'): ['plum_purple'],
    ('#f9bc08'): ['golden_rod'],
    ('#ff073a'): ['neon_red'],
    ('#c77986'): ['old_pink'],
    ('#d6fffe'): ['very_pale_blue'],
    ('#fe4b03'): ['blood_orange'],
    ('#fd5956'): ['grapefruit'],
    ('#fce166'): ['sand_yellow'],
    ('#b2713d'): ['clay_brown'],
    ('#1f3b4d'): ['dark_blue_grey'],
    ('#699d4c'): ['flat_green'],
    ('#56fca2'): ['light_green_blue'],
    ('#fb5581'): ['warm_pink'],
    ('#3e82fc'): ['dodger_blue'],
    ('#a0bf16'): ['gross_green'],
    ('#d6fffa'): ['ice'],
    ('#4f738e'): ['metallic_blue'],
    ('#ffb19a'): ['pale_salmon'],
    ('#5c8b15'): ['sap_green'],
    ('#54ac68'): ['algae'],
    ('#89a0b0'): ['bluey_grey'],
    ('#7ea07a'): ['greeny_grey'],
    ('#1bfc06'): ['highlighter_green'],
    ('#cafffb'): ['light_light_blue'],
    ('#b6ffbb'): ['light_mint'],
    ('#a75e09'): ['raw_umber'],
    ('#152eff'): ['vivid_blue'],
    ('#8d5eb7'): ['deep_lavender'],
    ('#5f9e8f'): ['dull_teal'],
    ('#63f7b4'): ['light_greenish_blue'],
    ('#606602'): ['mud_green'],
    ('#fc86aa'): ['pinky'],
    ('#8c0034'): ['red_wine'],
    ('#758000'): ['shit_green'],
    ('#ab7e4c'): ['tan_brown'],
    ('#030764'): ['darkblue'],
    ('#fe86a4'): ['rosa'],
    ('#d5174e'): ['lipstick'],
    ('#fed0fc'): ['pale_mauve'],
    ('#680018'): ['claret'],
    ('#fedf08'): ['dandelion'],
    ('#fe420f'): ['orangered'],
    ('#6f7c00'): ['poop_green'],
    ('#ca0147'): ['ruby'],
    ('#1b2431'): ['dark'],
    ('#00fbb0'): ['greenish_turquoise'],
    ('#db5856'): ['pastel_red'],
    ('#ddd618'): ['piss_yellow'],
    ('#41fdfe'): ['bright_cyan'],
    ('#cf524e'): ['dark_coral'],
    ('#21c36f'): ['algae_green'],
    ('#a90308'): ['darkish_red'],
    ('#6e1005'): ['reddy_brown'],
    ('#fe828c'): ['blush_pink'],
    ('#4b6113'): ['camouflage_green'],
    ('#4da409'): ['lawn_green'],
    ('#beae8a'): ['putty'],
    ('#0339f8'): ['vibrant_blue'],
    ('#a88f59'): ['dark_sand'],
    ('#5d21d0'): ['purple/blue'],
    ('#feb209'): ['saffron'],
    ('#4e518b'): ['twilight'],
    ('#964e02'): ['warm_brown'],
    ('#85a3b2'): ['bluegrey'],
    ('#ff69af'): ['bubble_gum_pink'],
    ('#c3fbf4'): ['duck_egg_blue'],
    ('#2afeb7'): ['greenish_cyan'],
    ('#005f6a'): ['petrol'],
    ('#0c1793'): ['royal'],
    ('#ffff81'): ['butter'],
    ('#f0833a'): ['dusty_orange'],
    ('#f1f33f'): ['off_yellow'],
    ('#b1d27b'): ['pale_olive_green'],
    ('#fc824a'): ['orangish'],
    ('#71aa34'): ['leaf'],
    ('#b7c9e2'): ['light_blue_grey'],
    ('#4b0101'): ['dried_blood'],
    ('#a552e6'): ['lightish_purple'],
    ('#af2f0d'): ['rusty_red'],
    ('#8b88f8'): ['lavender_blue'],
    ('#9af764'): ['light_grass_green'],
    ('#a6fbb2'): ['light_mint_green'],
    ('#ffc512'): ['sunflower'],
    ('#750851'): ['velvet'],
    ('#c14a09'): ['brick_orange'],
    ('#fe2f4a'): ['lightish_red'],
    ('#0203e2'): ['pure_blue'],
    ('#0a437a'): ['twilight_blue'],
    ('#a50055'): ['violet_red'],
    ('#ae8b0c'): ['yellowy_brown'],
    ('#fd798f'): ['carnation'],
    ('#bfac05'): ['muddy_yellow'],
    ('#3eaf76'): ['dark_seafoam_green'],
    ('#c74767'): ['deep_rose'],
    ('#b9484e'): ['dusty_red'],
    ('#647d8e'): ['grey/blue'],
    ('#bffe28'): ['lemon_lime'],
    ('#d725de'): ['purple/pink'],
    ('#b29705'): ['brown_yellow'],
    ('#673a3f'): ['purple_brown'],
    ('#a87dc2'): ['wisteria'],
    ('#fafe4b'): ['banana_yellow'],
    ('#c0022f'): ['lipstick_red'],
    ('#0e87cc'): ['water_blue'],
    ('#8d8468'): ['brown_grey'],
    ('#ad03de'): ['vibrant_purple'],
    ('#8cff9e'): ['baby_green'],
    ('#94ac02'): ['barf_green'],
    ('#c4fff7'): ['eggshell_blue'],
    ('#fdee73'): ['sandy_yellow'],
    ('#33b864'): ['cool_green'],
    ('#fff9d0'): ['pale'],
    ('#758da3'): ['blue/grey'],
    ('#f504c9'): ['hot_magenta'],
    ('#77a1b5'): ['greyblue'],
    ('#8756e4'): ['purpley'],
    ('#889717'): ['baby_shit_green'],
    ('#c27e79'): ['brownish_pink'],
    ('#017371'): ['dark_aquamarine'],
    ('#9f8303'): ['diarrhea'],
    ('#f7d560'): ['light_mustard'],
    ('#bdf6fe'): ['pale_sky_blue'],
    ('#75b84f'): ['turtle_green'],
    ('#9cbb04'): ['bright_olive'],
    ('#29465b'): ['dark_grey_blue'],
    ('#696006'): ['greeny_brown'],
    ('#adf802'): ['lemon_green'],
    ('#c1c6fc'): ['light_periwinkle'],
    ('#35ad6b'): ['seaweed_green'],
    ('#fffd37'): ['sunshine_yellow'],
    ('#a442a0'): ['ugly_purple'],
    ('#f36196'): ['medium_pink'],
    ('#947706'): ['puke_brown'],
    ('#fff4f2'): ['very_light_pink'],
    ('#1e9167'): ['viridian'],
    ('#b5c306'): ['bile'],
    ('#feff7f'): ['faded_yellow'],
    ('#cffdbc'): ['very_pale_green'],
    ('#0add08'): ['vibrant_green'],
    ('#87fd05'): ['bright_lime'],
    ('#1ef876'): ['spearmint'],
    ('#7bfdc7'): ['light_aquamarine'],
    ('#bcecac'): ['light_sage'],
    ('#bbf90f'): ['yellowgreen'],
    ('#ab9004'): ['baby_poo'],
    ('#1fb57a'): ['dark_seafoam'],
    ('#00555a'): ['deep_teal'],
    ('#a484ac'): ['heather'],
    ('#c45508'): ['rust_orange'],
    ('#3f829d'): ['dirty_blue'],
    ('#548d44'): ['fern_green'],
    ('#c95efb'): ['bright_lilac'],
    ('#3ae57f'): ['weird_green'],
    ('#016795'): ['peacock_blue'],
    ('#87a922'): ['avocado_green'],
    ('#f0944d'): ['faded_orange'],
    ('#5d1451'): ['grape_purple'],
    ('#25ff29'): ['hot_green'],
    ('#d0fe1d'): ['lime_yellow'],
    ('#ffa62b'): ['mango'],
    ('#01b44c'): ['shamrock'],
    ('#ff6cb5'): ['bubblegum'],
    ('#6b4247'): ['purplish_brown'],
    ('#c7c10c'): ['vomit_yellow'],
    ('#b7fffa'): ['pale_cyan'],
    ('#aeff6e'): ['key_lime'],
    ('#ec2d01'): ['tomato_red'],
    ('#76ff7b'): ['lightgreen'],
    ('#730039'): ['merlot'],
    ('#040348'): ['night_blue'],
    ('#df4ec8'): ['purpleish_pink'],
    ('#6ecb3c'): ['apple'],
    ('#8f9805'): ['baby_poop_green'],
    ('#5edc1f'): ['green_apple'],
    ('#d94ff5'): ['heliotrope'],
    ('#c8fd3d'): ['yellow/green'],
    ('#070d0d'): ['almost_black'],
    ('#4984b8'): ['cool_blue'],
    ('#51b73b'): ['leafy_green'],
    ('#ac7e04'): ['mustard_brown'],
    ('#4e5481'): ['dusk'],
    ('#876e4b'): ['dull_brown'],
    ('#58bc08'): ['frog_green'],
    ('#2fef10'): ['vivid_green'],
    ('#2dfe54'): ['bright_light_green'],
    ('#0aff02'): ['fluro_green'],
    ('#9cef43'): ['kiwi'],
    ('#18d17b'): ['seaweed'],
    ('#35530a'): ['navy_green'],
    ('#1805db'): ['ultramarine_blue'],
    ('#6258c4'): ['iris'],
    ('#ff964f'): ['pastel_orange'],
    ('#ffab0f'): ['yellowish_orange'],
    ('#8f8ce7'): ['perrywinkle'],
    ('#24bca8'): ['tealish'],
    ('#3f012c'): ['dark_plum'],
    ('#cbf85f'): ['pear'],
    ('#ff724c'): ['pinkish_orange'],
    ('#280137'): ['midnight_purple'],
    ('#b36ff6'): ['light_urple'],
    ('#48c072'): ['dark_mint'],
    ('#bccb7a'): ['greenish_tan'],
    ('#a8415b'): ['light_burgundy'],
    ('#06b1c4'): ['turquoise_blue'],
    ('#cd7584'): ['ugly_pink'],
    ('#f1da7a'): ['sandy'],
    ('#ff0490'): ['electric_pink'],
    ('#805b87'): ['muted_purple'],
    ('#50a747'): ['mid_green'],
    ('#a8a495'): ['greyish'],
    ('#cfff04'): ['neon_yellow'],
    ('#ffff7e'): ['banana'],
    ('#ff7fa7'): ['carnation_pink'],
    ('#ef4026'): ['tomato'],
    ('#3c9992'): ['sea'],
    ('#886806'): ['muddy_brown'],
    ('#04f489'): ['turquoise_green'],
    ('#fef69e'): ['buff'],
    ('#cfaf7b'): ['fawn'],
    ('#3b719f'): ['muted_blue'],
    ('#fdc1c5'): ['pale_rose'],
    ('#20c073'): ['dark_mint_green'],
    ('#9b5fc0'): ['amethyst'],
    ('#0f9b8e'): ['blue/green'],
    ('#742802'): ['chestnut'],
    ('#9db92c'): ['sick_green'],
    ('#a4bf20'): ['pea'],
    ('#cd5909'): ['rusty_orange'],
    ('#ada587'): ['stone'],
    ('#be013c'): ['rose_red'],
    ('#b8ffeb'): ['pale_aqua'],
    ('#dc4d01'): ['deep_orange'],
    ('#a2653e'): ['earth'],
    ('#638b27'): ['mossy_green'],
    ('#419c03'): ['grassy_green'],
    ('#b1ff65'): ['pale_lime_green'],
    ('#9dbcd4'): ['light_grey_blue'],
    ('#fdfdfe'): ['pale_grey'],
    ('#77ab56'): ['asparagus'],
    ('#464196'): ['blueberry'],
    ('#990147'): ['purple_red'],
    ('#befd73'): ['pale_lime'],
    ('#32bf84'): ['greenish_teal'],
    ('#af6f09'): ['caramel'],
    ('#a0025c'): ['deep_magenta'],
    ('#ffd8b1'): ['light_peach'],
    ('#7f4e1e'): ['milk_chocolate'],
    ('#bf9b0c'): ['ocher'],
    ('#6ba353'): ['off_green'],
    ('#f075e6'): ['purply_pink'],
    ('#7bc8f6'): ['lightblue'],
    ('#475f94'): ['dusky_blue'],
    ('#f5bf03'): ['golden'],
    ('#fffeb6'): ['light_beige'],
    ('#fffd74'): ['butter_yellow'],
    ('#895b7b'): ['dusky_purple'],
    ('#436bad'): ['french_blue'],
    ('#d0c101'): ['ugly_yellow'],
    ('#c6f808'): ['greeny_yellow'],
    ('#f43605'): ['orangish_red'],
    ('#02c14d'): ['shamrock_green'],
    ('#b25f03'): ['orangish_brown'],
    ('#2a7e19'): ['tree_green'],
    ('#490648'): ['deep_violet'],
    ('#536267'): ['gunmetal'],
    ('#5a06ef'): ['blue/purple'],
    ('#cf0234'): ['cherry'],
    ('#c4a661'): ['sandy_brown'],
    ('#978a84'): ['warm_grey'],
    ('#1f0954'): ['dark_indigo'],
    ('#03012d'): ['midnight'],
    ('#2bb179'): ['bluey_green'],
    ('#c3909b'): ['grey_pink'],
    ('#a66fb5'): ['soft_purple'],
    ('#770001'): ['blood'],
    ('#922b05'): ['brown_red'],
    ('#7d7f7c'): ['medium_grey'],
    ('#990f4b'): ['berry'],
    ('#8f7303'): ['poo'],
    ('#c83cb9'): ['purpley_pink'],
    ('#fea993'): ['light_salmon'],
    ('#acbb0d'): ['snot'],
    ('#c071fe'): ['easter_purple'],
    ('#ccfd7f'): ['light_yellow_green'],
    ('#00022e'): ['dark_navy_blue'],
    ('#828344'): ['drab'],
    ('#ffc5cb'): ['light_rose'],
    ('#ab1239'): ['rouge'],
    ('#b0054b'): ['purplish_red'],
    ('#99cc04'): ['slime_green'],
    ('#937c00'): ['baby_poop'],
    ('#019529'): ['irish_green'],
    ('#ef1de7'): ['pink/purple'],
    ('#000435'): ['dark_navy'],
    ('#42b395'): ['greeny_blue'],
    ('#9d5783'): ['light_plum'],
    ('#c8aca9'): ['pinkish_grey'],
    ('#c87606'): ['dirty_orange'],
    ('#aa2704'): ['rust_red'],
    ('#e4cbff'): ['pale_lilac'],
    ('#fa4224'): ['orangey_red'],
    ('#0804f9'): ['primary_blue'],
    ('#5cb200'): ['kermit_green'],
    ('#76424e'): ['brownish_purple'],
    ('#6c7a0e'): ['murky_green'],
    ('#fbdd7e'): ['wheat'],
    ('#2a0134'): ['very_dark_purple'],
    ('#044a05'): ['bottle_green'],
    ('#fd4659'): ['watermelon'],
    ('#0d75f8'): ['deep_sky_blue'],
    ('#fe0002'): ['fire_engine_red'],
    ('#cb9d06'): ['yellow_ochre'],
    ('#fb7d07'): ['pumpkin_orange'],
    ('#b9cc81'): ['pale_olive'],
    ('#edc8ff'): ['light_lilac'],
    ('#61e160'): ['lightish_green'],
    ('#8ab8fe'): ['carolina_blue'],
    ('#920a4e'): ['mulberry'],
    ('#fe02a2'): ['shocking_pink'],
    ('#9a3001'): ['auburn'],
    ('#65fe08'): ['bright_lime_green'],
    ('#befdb7'): ['celadon'],
    ('#b17261'): ['pinkish_brown'],
    ('#885f01'): ['poo_brown'],
    ('#02ccfe'): ['bright_sky_blue'],
    ('#c1fd95'): ['celery'],
    ('#836539'): ['dirt_brown'],
    ('#fb2943'): ['strawberry'],
    ('#84b701'): ['dark_lime'],
    ('#b66325'): ['copper'],
    ('#7f5112'): ['medium_brown'],
    ('#5fa052'): ['muted_green'],
    ('#6dedfd'): ['robin_s_egg'],
    ('#0bf9ea'): ['bright_aqua'],
    ('#c760ff'): ['bright_lavender'],
    ('#ffffcb'): ['ivory'],
    ('#f6cefc'): ['very_light_purple'],
    ('#155084'): ['light_navy'],
    ('#f5054f'): ['pink_red'],
    ('#645403'): ['olive_brown'],
    ('#7a5901'): ['poop_brown'],
    ('#a8b504'): ['mustard_green'],
    ('#3d9973'): ['ocean_green'],
    ('#000133'): ['very_dark_blue'],
    ('#76a973'): ['dusty_green'],
    ('#2e5a88'): ['light_navy_blue'],
    ('#0bf77d'): ['minty_green'],
    ('#bd6c48'): ['adobe'],
    ('#ac1db8'): ['barney'],
    ('#2baf6a'): ['jade_green'],
    ('#26f7fd'): ['bright_light_blue'],
    ('#aefd6c'): ['light_lime'],
    ('#9b8f55'): ['dark_khaki'],
    ('#ffad01'): ['orange_yellow'],
    ('#c69c04'): ['ocre'],
    ('#f4d054'): ['maize'],
    ('#de9dac'): ['faded_pink'],
    ('#05480d'): ['british_racing_green'],
    ('#c9ae74'): ['sandstone'],
    ('#60460f'): ['mud_brown'],
    ('#98f6b0'): ['light_sea_green'],
    ('#8af1fe'): ['robin_egg_blue'],
    ('#2ee8bb'): ['aqua_marine'],
    ('#11875d'): ['dark_sea_green'],
    ('#fdb0c0'): ['soft_pink'],
    ('#b16002'): ['orangey_brown'],
    ('#f7022a'): ['cherry_red'],
    ('#d5ab09'): ['burnt_yellow'],
    ('#86775f'): ['brownish_grey'],
    ('#c69f59'): ['camel'],
    ('#7a687f'): ['purplish_grey'],
    ('#042e60'): ['marine'],
    ('#c88d94'): ['greyish_pink'],
    ('#a5fbd5'): ['pale_turquoise'],
    ('#fffe71'): ['pastel_yellow'],
    ('#6241c7'): ['bluey_purple'],
    ('#fffe40'): ['canary_yellow'],
    ('#d3494e'): ['faded_red'],
    ('#985e2b'): ['sepia'],
    ('#a6814c'): ['coffee'],
    ('#ff08e8'): ['bright_magenta'],
    ('#9d7651'): ['mocha'],
    ('#feffca'): ['ecru'],
    ('#98568d'): ['purpleish'],
    ('#9e003a'): ['cranberry'],
    ('#287c37'): ['darkish_green'],
    ('#b96902'): ['brown_orange'],
    ('#ba6873'): ['dusky_rose'],
    ('#ff7855'): ['melon'],
    ('#94b21c'): ['sickly_green'],
    ('#c5c9c7'): ['silver'],
    ('#661aee'): ['purply_blue'],
    ('#6140ef'): ['purpleish_blue'],
    ('#9be5aa'): ['hospital_green'],
    ('#7b5804'): ['shit_brown'],
    ('#276ab3'): ['mid_blue'],
    ('#feb308'): ['amber'],
    ('#8cfd7e'): ['easter_green'],
    ('#6488ea'): ['soft_blue'],
    ('#056eee'): ['cerulean_blue'],
    ('#b27a01'): ['golden_brown'],
    ('#0ffef9'): ['bright_turquoise'],
    ('#fa2a55'): ['red_pink'],
    ('#820747'): ['red_purple'],
    ('#7a6a4f'): ['greyish_brown'],
    ('#f4320c'): ['vermillion'],
    ('#a13905'): ['russet'],
    ('#6f828a'): ['steel_grey'],
    ('#a55af4'): ['lighter_purple'],
    ('#ad0afd'): ['bright_violet'],
    ('#004577'): ['prussian_blue'],
    ('#658d6d'): ['slate_green'],
    ('#ca7b80'): ['dirty_pink'],
    ('#005249'): ['dark_blue_green'],
    ('#2b5d34'): ['pine'],
    ('#bff128'): ['yellowy_green'],
    ('#b59410'): ['dark_gold'],
    ('#2976bb'): ['bluish'],
    ('#014182'): ['darkish_blue'],
    ('#bb3f3f'): ['dull_red'],
    ('#fc2647'): ['pinky_red'],
    ('#a87900'): ['bronze'],
    ('#82cbb2'): ['pale_teal'],
    ('#667c3e'): ['military_green'],
    ('#fe46a5'): ['barbie_pink'],
    ('#fe83cc'): ['bubblegum_pink'],
    ('#94a617'): ['pea_soup_green'],
    ('#a88905'): ['dark_mustard'],
    ('#7f5f00'): ['shit'],
    ('#9e43a2'): ['medium_purple'],
    ('#062e03'): ['very_dark_green'],
    ('#8a6e45'): ['dirt'],
    ('#cc7a8b'): ['dusky_pink'],
    ('#9e0168'): ['red_violet'],
    ('#fdff38'): ['lemon_yellow'],
    ('#c0fa8b'): ['pistachio'],
    ('#eedc5b'): ['dull_yellow'],
    ('#7ebd01'): ['dark_lime_green'],
    ('#3b5b92'): ['denim_blue'],
    ('#01889f'): ['teal_blue'],
    ('#3d7afd'): ['lightish_blue'],
    ('#5f34e7'): ['purpley_blue'],
    ('#6d5acf'): ['light_indigo'],
    ('#748500'): ['swamp_green'],
    ('#706c11'): ['brown_green'],
    ('#3c0008'): ['dark_maroon'],
    ('#cb00f5'): ['hot_purple'],
    ('#002d04'): ['dark_forest_green'],
    ('#658cbb'): ['faded_blue'],
    ('#749551'): ['drab_green'],
    ('#b9ff66'): ['light_lime_green'],
    ('#9dc100'): ['snot_green'],
    ('#faee66'): ['yellowish'],
    ('#7efbb3'): ['light_blue_green'],
    ('#7b002c'): ['bordeaux'],
    ('#c292a1'): ['light_mauve'],
    ('#017b92'): ['ocean'],
    ('#fcc006'): ['marigold'],
    ('#657432'): ['muddy_green'],
    ('#d8863b'): ['dull_orange'],
    ('#738595'): ['steel'],
    ('#aa23ff'): ['electric_purple'],
    ('#08ff08'): ['fluorescent_green'],
    ('#9b7a01'): ['yellowish_brown'],
    ('#f29e8e'): ['blush'],
    ('#6fc276'): ['soft_green'],
    ('#ff5b00'): ['bright_orange'],
    ('#fdff52'): ['lemon'],
    ('#866f85'): ['purple_grey'],
    ('#8ffe09'): ['acid_green'],
    ('#eecffe'): ['pale_lavender'],
    ('#510ac9'): ['violet_blue'],
    ('#4f9153'): ['light_forest_green'],
    ('#9f2305'): ['burnt_red'],
    ('#728639'): ['khaki_green'],
    ('#de0c62'): ['cerise'],
    ('#916e99'): ['faded_purple'],
    ('#ffb16d'): ['apricot'],
    ('#3c4d03'): ['dark_olive_green'],
    ('#7f7053'): ['grey_brown'],
    ('#77926f'): ['green_grey'],
    ('#010fcc'): ['true_blue'],
    ('#ceaefa'): ['pale_violet'],
    ('#8f99fb'): ['periwinkle_blue'],
    ('#c6fcff'): ['light_sky_blue'],
    ('#5539cc'): ['blurple'],
    ('#544e03'): ['green_brown'],
    ('#017a79'): ['bluegreen'],
    ('#01f9c6'): ['bright_teal'],
    ('#c9b003'): ['brownish_yellow'],
    ('#929901'): ['pea_soup'],
    ('#0b5509'): ['forest'],
    ('#a00498'): ['barney_purple'],
    ('#2000b1'): ['ultramarine'],
    ('#94568c'): ['purplish'],
    ('#c2be0e'): ['puke_yellow'],
    ('#748b97'): ['bluish_grey'],
    ('#665fd1'): ['dark_periwinkle'],
    ('#9c6da5'): ['dark_lilac'],
    ('#c44240'): ['reddish'],
    ('#a24857'): ['light_maroon'],
    ('#825f87'): ['dusty_purple'],
    ('#c9643b'): ['terra_cotta'],
    ('#90b134'): ['avocado'],
    ('#01386a'): ['marine_blue'],
    ('#25a36f'): ['teal_green'],
    ('#59656d'): ['slate_grey'],
    ('#75fd63'): ['lighter_green'],
    ('#21fc0d'): ['electric_green'],
    ('#5a86ad'): ['dusty_blue'],
    ('#fec615'): ['golden_yellow'],
    ('#fffd01'): ['bright_yellow'],
    ('#dfc5fe'): ['light_lavender'],
    ('#b26400'): ['umber'],
    ('#7f5e00'): ['poop'],
    ('#de7e5d'): ['dark_peach'],
    ('#048243'): ['jungle_green'],
    ('#ffffd4'): ['eggshell'],
    ('#3b638c'): ['denim'],
    ('#b79400'): ['yellow_brown'],
    ('#84597e'): ['dull_purple'],
    ('#411900'): ['chocolate_brown'],
    ('#7b0323'): ['wine_red'],
    ('#04d9ff'): ['neon_blue'],
    ('#667e2c'): ['dirty_green'],
    ('#fbeeac'): ['light_tan'],
    ('#d7fffe'): ['ice_blue'],
    ('#4e7496'): ['cadet_blue'],
    ('#874c62'): ['dark_mauve'],
    ('#d5ffff'): ['very_light_blue'],
    ('#826d8c'): ['grey_purple'],
    ('#ffbacd'): ['pastel_pink'],
    ('#d1ffbd'): ['very_light_green'],
    ('#448ee4'): ['dark_sky_blue'],
    ('#05472a'): ['evergreen'],
    ('#d5869d'): ['dull_pink'],
    ('#3d0734'): ['aubergine'],
    ('#4a0100'): ['mahogany'],
    ('#f8481c'): ['reddish_orange'],
    ('#02590f'): ['deep_green'],
    ('#89a203'): ['vomit_green'],
    ('#e03fd8'): ['purple_pink'],
    ('#d58a94'): ['dusty_pink'],
    ('#7bb274'): ['faded_green'],
    ('#526525'): ['camo_green'],
    ('#c94cbe'): ['pinky_purple'],
    ('#db4bda'): ['pink_purple'],
    ('#9e3623'): ['brownish_red'],
    ('#b5485d'): ['dark_rose'],
    ('#735c12'): ['mud'],
    ('#9c6d57'): ['brownish'],
    ('#028f1e'): ['emerald_green'],
    ('#b1916e'): ['pale_brown'],
    ('#49759c'): ['dull_blue'],
    ('#a0450e'): ['burnt_umber'],
    ('#39ad48'): ['medium_green'],
    ('#b66a50'): ['clay'],
    ('#8cffdb'): ['light_aqua'],
    ('#a4be5c'): ['light_olive_green'],
    ('#cb7723'): ['brownish_orange'],
    ('#05696b'): ['dark_aqua'],
    ('#ce5dae'): ['purplish_pink'],
    ('#c85a53'): ['dark_salmon'],
    ('#96ae8d'): ['greenish_grey'],
    ('#1fa774'): ['jade'],
    ('#7a9703'): ['ugly_green'],
    ('#ac9362'): ['dark_beige'],
    ('#01a049'): ['emerald'],
    ('#d9544d'): ['pale_red'],
    ('#fa5ff7'): ['light_magenta'],
    ('#82cafc'): ['sky'],
    ('#acfffc'): ['light_cyan'],
    ('#fcb001'): ['yellow_orange'],
    ('#910951'): ['reddish_purple'],
    ('#fe2c54'): ['reddish_pink'],
    ('#c875c4'): ['orchid'],
    ('#cdc50a'): ['dirty_yellow'],
    ('#fd411e'): ['orange_red'],
    ('#9a0200'): ['deep_red'],
    ('#be6400'): ['orange_brown'],
    ('#030aa7'): ['cobalt_blue'],
    ('#fe019a'): ['neon_pink'],
    ('#f7879a'): ['rose_pink'],
    ('#887191'): ['greyish_purple'],
    ('#b00149'): ['raspberry'],
    ('#12e193'): ['aqua_green'],
    ('#fe7b7c'): ['salmon_pink'],
    ('#ff9408'): ['tangerine'],
    ('#6a6e09'): ['brownish_green'],
    ('#8b2e16'): ['red_brown'],
    ('#696112'): ['greenish_brown'],
    ('#e17701'): ['pumpkin'],
    ('#0a481e'): ['pine_green'],
    ('#343837'): ['charcoal'],
    ('#ffb7ce'): ['baby_pink'],
    ('#6a79f7'): ['cornflower'],
    ('#5d06e9'): ['blue_violet'],
    ('#3d1c02'): ['chocolate'],
    ('#82a67d'): ['greyish_green'],
    ('#be0119'): ['scarlet'],
    ('#c9ff27'): ['green_yellow'],
    ('#373e02'): ['dark_olive'],
    ('#a9561e'): ['sienna'],
    ('#caa0ff'): ['pastel_purple'],
    ('#ca6641'): ['terracotta'],
    ('#02d8e9'): ['aqua_blue'],
    ('#88b378'): ['sage_green'],
    ('#980002'): ['blood_red'],
    ('#cb0162'): ['deep_pink'],
    ('#5cac2d'): ['grass'],
    ('#769958'): ['moss'],
    ('#a2bffe'): ['pastel_blue'],
    ('#10a674'): ['bluish_green'],
    ('#06b48b'): ['green_blue'],
    ('#af884a'): ['dark_tan'],
    ('#0b8b87'): ['greenish_blue'],
    ('#ffa756'): ['pale_orange'],
    ('#a2a415'): ['vomit'],
    ('#154406'): ['forrest_green'],
    ('#856798'): ['dark_lavender'],
    ('#34013f'): ['dark_violet'],
    ('#632de9'): ['purple_blue'],
    ('#0a888a'): ['dark_cyan'],
    ('#6f7632'): ['olive_drab'],
    ('#d46a7e'): ['pinkish'],
    ('#1e488f'): ['cobalt'],
    ('#bc13fe'): ['neon_purple'],
    ('#7ef4cc'): ['light_turquoise'],
    ('#76cd26'): ['apple_green'],
    ('#74a662'): ['dull_green'],
    ('#80013f'): ['wine'],
    ('#b1d1fc'): ['powder_blue'],
    ('#ffffe4'): ['off_white'],
    ('#0652ff'): ['electric_blue'],
    ('#045c5a'): ['dark_turquoise'],
    ('#5729ce'): ['blue_purple'],
    ('#069af3'): ['azure'],
    ('#ff000d'): ['bright_red'],
    ('#f10c45'): ['pinkish_red'],
    ('#5170d7'): ['cornflower_blue'],
    ('#acbf69'): ['light_olive'],
    ('#6c3461'): ['grape'],
    ('#5e819d'): ['greyish_blue'],
    ('#601ef9'): ['purplish_blue'],
    ('#b0dd16'): ['yellowish_green'],
    ('#cdfd02'): ['greenish_yellow'],
    ('#2c6fbb'): ['medium_blue'],
    ('#c0737a'): ['dusty_rose'],
    ('#d6b4fc'): ['light_violet'],
    ('#020035'): ['midnight_blue'],
    ('#703be7'): ['bluish_purple'],
    ('#fd3c06'): ['red_orange'],
    ('#960056'): ['dark_magenta'],
    ('#40a368'): ['greenish'],
    ('#03719c'): ['ocean_blue'],
    ('#fc5a50'): ['coral'],
    ('#ffffc2'): ['cream'],
    ('#7f2b0a'): ['reddish_brown'],
    ('#b04e0f'): ['burnt_sienna'],
    ('#a03623'): ['brick'],
    ('#87ae73'): ['sage'],
    ('#789b73'): ['grey_green'],
    ('#ffffff'): ['white'],
    ('#98eff9'): ['robin_s_egg_blue'],
    ('#658b38'): ['moss_green'],
    ('#5a7d9a'): ['steel_blue'],
    ('#380835'): ['eggplant'],
    ('#fffe7a'): ['light_yellow'],
    ('#5ca904'): ['leaf_green'],
    ('#d8dcd6'): ['light_grey'],
    ('#a5a502'): ['puke'],
    ('#d648d7'): ['pinkish_purple'],
    ('#047495'): ['sea_blue'],
    ('#b790d4'): ['pale_purple'],
    ('#5b7c99'): ['slate_blue'],
    ('#607c8e'): ['blue_grey'],
    ('#0b4008'): ['hunter_green'],
    ('#ed0dd9'): ['fuchsia'],
    ('#8c000f'): ['crimson'],
    ('#ffff84'): ['pale_yellow'],
    ('#bf9005'): ['ochre'],
    ('#d2bd0a'): ['mustard_yellow'],
    ('#ff474c'): ['light_red'],
    ('#0485d1'): ['cerulean'],
    ('#ffcfdc'): ['pale_pink'],
    ('#040273'): ['deep_blue'],
    ('#a83c09'): ['rust'],
    ('#90e4c1'): ['light_teal'],
    ('#516572'): ['slate'],
    ('#fac205'): ['goldenrod'],
    ('#d5b60a'): ['dark_yellow'],
    ('#363737'): ['dark_grey'],
    ('#4b5d16'): ['army_green'],
    ('#6b8ba4'): ['grey_blue'],
    ('#80f9ad'): ['seafoam'],
    ('#a57e52'): ['puce'],
    ('#a9f971'): ['spring_green'],
    ('#c65102'): ['dark_orange'],
    ('#e2ca76'): ['sand'],
    ('#b0ff9d'): ['pastel_green'],
    ('#9ffeb0'): ['mint'],
    ('#fdaa48'): ['light_orange'],
    ('#fe01b1'): ['bright_pink'],
    ('#c1f80a'): ['chartreuse'],
    ('#36013f'): ['deep_purple'],
    ('#341c02'): ['dark_brown'],
    ('#b9a281'): ['taupe'],
    ('#8eab12'): ['pea_green'],
    ('#9aae07'): ['puke_green'],
    ('#02ab2e'): ['kelly_green'],
    ('#7af9ab'): ['seafoam_green'],
    ('#137e6d'): ['blue_green'],
    ('#aaa662'): ['khaki'],
    ('#610023'): ['burgundy'],
    ('#014d4e'): ['dark_teal'],
    ('#8f1402'): ['brick_red'],
    ('#4b006e'): ['royal_purple'],
    ('#580f41'): ['plum'],
    ('#8fff9f'): ['mint_green'],
    ('#dbb40c'): ['gold'],
    ('#a2cffe'): ['baby_blue'],
    ('#c0fb2d'): ['yellow_green'],
    ('#be03fd'): ['bright_purple'],
    ('#840000'): ['dark_red'],
    ('#d0fefe'): ['pale_blue'],
    ('#3f9b0b'): ['grass_green'],
    ('#01153e'): ['navy'],
    ('#04d8b2'): ['aquamarine'],
    ('#c04e01'): ['burnt_orange'],
    ('#0cff0c'): ['neon_green'],
    ('#0165fc'): ['bright_blue'],
    ('#cf6275'): ['rose'],
    ('#ffd1df'): ['light_pink'],
    ('#ceb301'): ['mustard'],
    ('#380282'): ['indigo'],
    ('#aaff32'): ['lime'],
    ('#53fca1'): ['sea_green'],
    ('#8e82fe'): ['periwinkle'],
    ('#cb416b'): ['dark_pink'],
    ('#677a04'): ['olive_green'],
    ('#ffb07c'): ['peach'],
    ('#c7fdb5'): ['pale_green'],
    ('#ad8150'): ['light_brown'],
    ('#ff028d'): ['hot_pink'],
    ('#000000'): ['black'],
    ('#cea2fd'): ['lilac'],
    ('#001146'): ['navy_blue'],
    ('#0504aa'): ['royal_blue'],
    ('#e6daa6'): ['beige'],
    ('#ff796c'): ['salmon'],
    ('#6e750e'): ['olive'],
    ('#650021'): ['maroon'],
    ('#01ff07'): ['bright_green'],
    ('#35063e'): ['dark_purple'],
    ('#ae7181'): ['mauve'],
    ('#06470c'): ['forest_green'],
    ('#13eac9'): ['aqua'],
    ('#00ffff'): ['cyan'],
    ('#d1b26f'): ['tan'],
    ('#00035b'): ['dark_blue'],
    ('#c79fef'): ['lavender'],
    ('#06c2ac'): ['turquoise'],
    ('#033500'): ['dark_green'],
    ('#9a0eea'): ['violet'],
    ('#bf77f6'): ['light_purple'],
    ('#89fe05'): ['lime_green'],
    ('#929591'): ['grey'],
    ('#75bbfd'): ['sky_blue'],
    ('#ffff14'): ['yellow'],
    ('#c20078'): ['magenta'],
    ('#96f97b'): ['light_green'],
    ('#f97306'): ['orange'],
    ('#029386'): ['teal'],
    ('#95d0fc'): ['light_blue'],
    ('#e50000'): ['red'],
    ('#653700'): ['brown'],
    ('#ff81c0'): ['pink'],
    ('#0343df'): ['blue'],
    ('#15b01a'): ['green'],
    ('#7e1e9c'): ['purple']
}

## Building inverse relation
XKCD_COLOR_NAME_TO_HEX = dict(
    (name.lower(), hex_val)
    for hex_val, names in HEX_TO_XKCD_COLOR_NAMES.items()
    for name in names)

RGB_TO_COLOR_NAMES = {
    (0, 0, 0): ['Black'],
    (0, 0, 128): ['Navy', 'NavyBlue'],
    (0, 0, 139): ['DarkBlue'],
    (0, 0, 205): ['MediumBlue'],
    (0, 0, 255): ['Blue'],
    (0, 100, 0): ['DarkGreen'],
    (0, 128, 0): ['Green'],
    (0, 139, 139): ['DarkCyan'],
    (0, 191, 255): ['DeepSkyBlue'],
    (0, 206, 209): ['DarkTurquoise'],
    (0, 250, 154): ['MediumSpringGreen'],
    (0, 255, 0): ['Lime'],
    (0, 255, 127): ['SpringGreen'],
    (0, 255, 255): ['Cyan', 'Aqua'],
    (25, 25, 112): ['MidnightBlue'],
    (30, 144, 255): ['DodgerBlue'],
    (32, 178, 170): ['LightSeaGreen'],
    (34, 139, 34): ['ForestGreen'],
    (46, 139, 87): ['SeaGreen'],
    (47, 79, 79): ['DarkSlateGray', 'DarkSlateGrey'],
    (50, 205, 50): ['LimeGreen'],
    (60, 179, 113): ['MediumSeaGreen'],
    (64, 224, 208): ['Turquoise'],
    (65, 105, 225): ['RoyalBlue'],
    (70, 130, 180): ['SteelBlue'],
    (72, 61, 139): ['DarkSlateBlue'],
    (72, 209, 204): ['MediumTurquoise'],
    (75, 0, 130): ['Indigo'],
    (85, 107, 47): ['DarkOliveGreen'],
    (95, 158, 160): ['CadetBlue'],
    (100, 149, 237): ['CornflowerBlue'],
    (102, 205, 170): ['MediumAquamarine'],
    (105, 105, 105): ['DimGray', 'DimGrey'],
    (106, 90, 205): ['SlateBlue'],
    (107, 142, 35): ['OliveDrab'],
    (112, 128, 144): ['SlateGray', 'SlateGrey'],
    (119, 136, 153): ['LightSlateGray', 'LightSlateGrey'],
    (123, 104, 238): ['MediumSlateBlue'],
    (124, 252, 0): ['LawnGreen'],
    (127, 255, 0): ['Chartreuse'],
    (127, 255, 212): ['Aquamarine'],
    (128, 0, 0): ['Maroon'],
    (128, 0, 128): ['Purple'],
    (128, 128, 0): ['Olive'],
    (128, 128, 128): ['Gray', 'Grey'],
    (132, 112, 255): ['LightSlateBlue'],
    (135, 206, 235): ['SkyBlue'],
    (135, 206, 250): ['LightSkyBlue'],
    (138, 43, 226): ['BlueViolet'],
    (139, 0, 0): ['DarkRed'],
    (139, 0, 139): ['DarkMagenta'],
    (139, 69, 19): ['SaddleBrown'],
    (143, 188, 143): ['DarkSeaGreen'],
    (144, 238, 144): ['LightGreen'],
    (147, 112, 219): ['MediumPurple'],
    (148, 0, 211): ['DarkViolet'],
    (152, 251, 152): ['PaleGreen'],
    (153, 50, 204): ['DarkOrchid'],
    (154, 205, 50): ['YellowGreen'],
    (160, 82, 45): ['Sienna'],
    (165, 42, 42): ['Brown'],
    (169, 169, 169): ['DarkGray', 'DarkGrey'],
    (173, 216, 230): ['LightBlue'],
    (173, 255, 47): ['GreenYellow'],
    (175, 238, 238): ['PaleTurquoise'],
    (176, 196, 222): ['LightSteelBlue'],
    (176, 224, 230): ['PowderBlue'],
    (178, 34, 34): ['Firebrick'],
    (184, 134, 11): ['DarkGoldenrod'],
    (186, 85, 211): ['MediumOrchid'],
    (188, 143, 143): ['RosyBrown'],
    (189, 183, 107): ['DarkKhaki'],
    (192, 192, 192): ['Silver'],
    (199, 21, 133): ['MediumVioletRed'],
    (205, 92, 92): ['IndianRed'],
    (205, 133, 63): ['Peru'],
    (208, 32, 144): ['VioletRed'],
    (210, 105, 30): ['Chocolate'],
    (210, 180, 140): ['Tan'],
    (211, 211, 211): ['LightGray', 'LightGrey'],
    (216, 191, 216): ['Thistle'],
    (218, 112, 214): ['Orchid'],
    (218, 165, 32): ['Goldenrod'],
    (219, 112, 147): ['PaleVioletRed'],
    (220, 20, 60): ['Crimson'],
    (220, 220, 220): ['Gainsboro'],
    (221, 160, 221): ['Plum'],
    (222, 184, 135): ['Burlywood'],
    (224, 255, 255): ['LightCyan'],
    (230, 230, 250): ['Lavender'],
    (233, 150, 122): ['DarkSalmon'],
    (238, 130, 238): ['Violet'],
    (238, 221, 130): ['LightGoldenrod'],
    (238, 232, 170): ['PaleGoldenrod'],
    (240, 128, 128): ['LightCoral'],
    (240, 230, 140): ['Khaki'],
    (240, 248, 255): ['AliceBlue'],
    (240, 255, 240): ['Honeydew'],
    (240, 255, 255): ['Azure'],
    (244, 164, 96): ['SandyBrown'],
    (245, 222, 179): ['Wheat'],
    (245, 245, 220): ['Beige'],
    (245, 245, 245): ['WhiteSmoke'],
    (245, 255, 250): ['MintCream'],
    (248, 248, 255): ['GhostWhite'],
    (250, 128, 114): ['Salmon'],
    (250, 235, 215): ['AntiqueWhite'],
    (250, 240, 230): ['Linen'],
    (250, 250, 210): ['LightGoldenrodYellow'],
    (253, 245, 230): ['OldLace'],
    (255, 0, 0): ['Red'],
    (255, 0, 255): ['Magenta', 'Fuchsia'],
    (255, 20, 147): ['DeepPink'],
    (255, 69, 0): ['OrangeRed'],
    (255, 99, 71): ['Tomato'],
    (255, 105, 180): ['HotPink'],
    (255, 127, 80): ['Coral'],
    (255, 140, 0): ['DarkOrange'],
    (255, 160, 122): ['LightSalmon'],
    (255, 165, 0): ['Orange'],
    (255, 182, 193): ['LightPink'],
    (255, 192, 203): ['Pink'],
    (255, 215, 0): ['Gold'],
    (255, 218, 185): ['PeachPuff'],
    (255, 222, 173): ['NavajoWhite'],
    (255, 228, 181): ['Moccasin'],
    (255, 228, 196): ['Bisque'],
    (255, 228, 225): ['MistyRose'],
    (255, 235, 205): ['BlanchedAlmond'],
    (255, 239, 213): ['PapayaWhip'],
    (255, 240, 245): ['LavenderBlush'],
    (255, 245, 238): ['Seashell'],
    (255, 248, 220): ['Cornsilk'],
    (255, 250, 205): ['LemonChiffon'],
    (255, 250, 240): ['FloralWhite'],
    (255, 250, 250): ['Snow'],
    (255, 255, 0): ['Yellow'],
    (255, 255, 224): ['LightYellow'],
    (255, 255, 240): ['Ivory'],
    (255, 255, 255): ['White']
}

## Building inverse relation
COLOR_NAME_TO_RGB = dict(
    (name.lower(), rgb)
    for rgb, names in RGB_TO_COLOR_NAMES.items()
    for name in names)


LONG_HEX_COLOR = re.compile(r'^#[0-9a-fA-F]{6}$')
SHORT_HEX_COLOR = re.compile(r'^#[0-9a-fA-F]{3}$')


class C_HSL:

    def __getattr__(self, value):
        label = value.lower()
        if label in COLOR_NAME_TO_RGB:
            return rgb2hsl(tuple(v / 255. for v in COLOR_NAME_TO_RGB[label]))
        raise AttributeError("%s instance has no attribute %r"
                             % (self.__class__, value))


HSL = C_HSL()


class C_RGB:
    """RGB colors container

    Provides a quick color access.

    >>> from colour import RGB

    >>> RGB.WHITE
    (1.0, 1.0, 1.0)
    >>> RGB.BLUE
    (0.0, 0.0, 1.0)

    >>> RGB.DONOTEXISTS  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    AttributeError: ... has no attribute 'DONOTEXISTS'

    """

    def __getattr__(self, value):
        return hsl2rgb(getattr(HSL, value))


class C_HEX:
    """RGB colors container

    Provides a quick color access.

    >>> from colour import HEX

    >>> HEX.WHITE
    '#fff'
    >>> HEX.BLUE
    '#00f'

    >>> HEX.DONOTEXISTS  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    AttributeError: ... has no attribute 'DONOTEXISTS'

    """

    def __getattr__(self, value):
        return rgb2hex(getattr(RGB, value))

RGB = C_RGB()
HEX = C_HEX()


##
## Conversion function
##

def hsl2rgb(hsl):
    """Convert HSL representation towards RGB

    :param h: Hue, position around the chromatic circle (h=1 equiv h=0)
    :param s: Saturation, color saturation (0=full gray, 1=full color)
    :param l: Ligthness, Overhaul lightness (0=full black, 1=full white)
    :rtype: 3-uple for RGB values in float between 0 and 1

    Hue, Saturation, Range from Lightness is a float between 0 and 1

    Note that Hue can be set to any value but as it is a rotation
    around the chromatic circle, any value above 1 or below 0 can
    be expressed by a value between 0 and 1 (Note that h=0 is equiv
    to h=1).

    This algorithm came from:
    http://www.easyrgb.com/index.php?X=MATH&H=19#text19

    Here are some quick notion of HSL to RGB conversion:

    >>> from colour import hsl2rgb

    With a lightness put at 0, RGB is always rgbblack

    >>> hsl2rgb((0.0, 0.0, 0.0))
    (0.0, 0.0, 0.0)
    >>> hsl2rgb((0.5, 0.0, 0.0))
    (0.0, 0.0, 0.0)
    >>> hsl2rgb((0.5, 0.5, 0.0))
    (0.0, 0.0, 0.0)

    Same for lightness put at 1, RGB is always rgbwhite

    >>> hsl2rgb((0.0, 0.0, 1.0))
    (1.0, 1.0, 1.0)
    >>> hsl2rgb((0.5, 0.0, 1.0))
    (1.0, 1.0, 1.0)
    >>> hsl2rgb((0.5, 0.5, 1.0))
    (1.0, 1.0, 1.0)

    With saturation put at 0, the RGB should be equal to Lightness:

    >>> hsl2rgb((0.0, 0.0, 0.25))
    (0.25, 0.25, 0.25)
    >>> hsl2rgb((0.5, 0.0, 0.5))
    (0.5, 0.5, 0.5)
    >>> hsl2rgb((0.5, 0.0, 0.75))
    (0.75, 0.75, 0.75)

    With saturation put at 1, and lightness put to 0.5, we can find
    normal full red, green, blue colors:

    >>> hsl2rgb((0 , 1.0, 0.5))
    (1.0, 0.0, 0.0)
    >>> hsl2rgb((1 , 1.0, 0.5))
    (1.0, 0.0, 0.0)
    >>> hsl2rgb((1.0/3 , 1.0, 0.5))
    (0.0, 1.0, 0.0)
    >>> hsl2rgb((2.0/3 , 1.0, 0.5))
    (0.0, 0.0, 1.0)

    Of course:
    >>> hsl2rgb((0.0, 2.0, 0.5))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: Saturation must be between 0 and 1.

    And:
    >>> hsl2rgb((0.0, 0.0, 1.5))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: Lightness must be between 0 and 1.

    """
    h, s, l = [float(v) for v in hsl]

    if not (0.0 - FLOAT_ERROR <= s <= 1.0 + FLOAT_ERROR):
        raise ValueError("Saturation must be between 0 and 1.")
    if not (0.0 - FLOAT_ERROR <= l <= 1.0 + FLOAT_ERROR):
        raise ValueError("Lightness must be between 0 and 1.")

    if s == 0:
        return l, l, l

    if l < 0.5:
        v2 = l * (1.0 + s)
    else:
        v2 = (l + s) - (s * l)

    v1 = 2.0 * l - v2

    r = _hue2rgb(v1, v2, h + (1.0 / 3))
    g = _hue2rgb(v1, v2, h)
    b = _hue2rgb(v1, v2, h - (1.0 / 3))

    return r, g, b


def rgb2hsl(rgb):
    """Convert RGB representation towards HSL

    :param r: Red amount (float between 0 and 1)
    :param g: Green amount (float between 0 and 1)
    :param b: Blue amount (float between 0 and 1)
    :rtype: 3-uple for HSL values in float between 0 and 1

    This algorithm came from:
    http://www.easyrgb.com/index.php?X=MATH&H=19#text19

    Here are some quick notion of RGB to HSL conversion:

    >>> from colour import rgb2hsl

    Note that if red amount is equal to green and blue, then you
    should have a gray value (from black to white).


    >>> rgb2hsl((1.0, 1.0, 1.0))  # doctest: +ELLIPSIS
    (..., 0.0, 1.0)
    >>> rgb2hsl((0.5, 0.5, 0.5))  # doctest: +ELLIPSIS
    (..., 0.0, 0.5)
    >>> rgb2hsl((0.0, 0.0, 0.0))  # doctest: +ELLIPSIS
    (..., 0.0, 0.0)

    If only one color is different from the others, it defines the
    direct Hue:

    >>> rgb2hsl((0.5, 0.5, 1.0))  # doctest: +ELLIPSIS
    (0.66..., 1.0, 0.75)
    >>> rgb2hsl((0.2, 0.1, 0.1))  # doctest: +ELLIPSIS
    (0.0, 0.33..., 0.15...)

    Having only one value set, you can check that:

    >>> rgb2hsl((1.0, 0.0, 0.0))
    (0.0, 1.0, 0.5)
    >>> rgb2hsl((0.0, 1.0, 0.0))  # doctest: +ELLIPSIS
    (0.33..., 1.0, 0.5)
    >>> rgb2hsl((0.0, 0.0, 1.0))  # doctest: +ELLIPSIS
    (0.66..., 1.0, 0.5)

    Regression check upon very close values in every component of
    red, green and blue:

    >>> rgb2hsl((0.9999999999999999, 1.0, 0.9999999999999994))
    (0.0, 0.0, 0.999...)

    Of course:

    >>> rgb2hsl((0.0, 2.0, 0.5))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: Green must be between 0 and 1. You provided 2.0.

    And:
    >>> rgb2hsl((0.0, 0.0, 1.5))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: Blue must be between 0 and 1. You provided 1.5.

    """
    r, g, b = [float(v) for v in rgb]

    for name, v in {'Red': r, 'Green': g, 'Blue': b}.items():
        if not (0 - FLOAT_ERROR <= v <= 1 + FLOAT_ERROR):
            raise ValueError("%s must be between 0 and 1. You provided %r."
                             % (name, v))

    vmin = min(r, g, b)  ## Min. value of RGB
    vmax = max(r, g, b)  ## Max. value of RGB
    diff = vmax - vmin   ## Delta RGB value

    vsum = vmin + vmax

    l = vsum / 2

    if diff < FLOAT_ERROR:  ## This is a gray, no chroma...
        return (0.0, 0.0, l)

    ##
    ## Chromatic data...
    ##

    ## Saturation
    if l < 0.5:
        s = diff / vsum
    else:
        s = diff / (2.0 - vsum)

    dr = (((vmax - r) / 6) + (diff / 2)) / diff
    dg = (((vmax - g) / 6) + (diff / 2)) / diff
    db = (((vmax - b) / 6) + (diff / 2)) / diff

    if r == vmax:
        h = db - dg
    elif g == vmax:
        h = (1.0 / 3) + dr - db
    elif b == vmax:
        h = (2.0 / 3) + dg - dr

    if h < 0: h += 1
    if h > 1: h -= 1

    return (h, s, l)


def _hue2rgb(v1, v2, vH):
    """Private helper function (Do not call directly)

    :param vH: rotation around the chromatic circle (between 0..1)

    """

    while vH < 0: vH += 1
    while vH > 1: vH -= 1

    if 6 * vH < 1: return v1 + (v2 - v1) * 6 * vH
    if 2 * vH < 1: return v2
    if 3 * vH < 2: return v1 + (v2 - v1) * ((2.0 / 3) - vH) * 6

    return v1


def rgb2hex(rgb, force_long=False):
    """Transform RGB tuple to hex RGB representation

    :param rgb: RGB 3-uple of float between 0 and 1
    :rtype: 3 hex char or 6 hex char string representation

    Usage
    -----

    >>> from colour import rgb2hex

    >>> rgb2hex((0.0,1.0,0.0))
    '#0f0'

    Rounding try to be as natural as possible:

    >>> rgb2hex((0.0,0.999999,1.0))
    '#0ff'

    And if not possible, the 6 hex char representation is used:

    >>> rgb2hex((0.23,1.0,1.0))
    '#3bffff'

    >>> rgb2hex((0.0,0.999999,1.0), force_long=True)
    '#00ffff'

    """

    hx = ''.join(["%02x" % int(c * 255 + 0.5 - FLOAT_ERROR)
                  for c in rgb])

    if not force_long and hx[0::2] == hx[1::2]:
        hx = ''.join(hx[0::2])

    return "#%s" % hx


def hex2rgb(str_rgb):
    """Transform hex RGB representation to RGB tuple

    :param str_rgb: 3 hex char or 6 hex char string representation
    :rtype: RGB 3-uple of float between 0 and 1

    >>> from colour import hex2rgb

    >>> hex2rgb('#00ff00')
    (0.0, 1.0, 0.0)

    >>> hex2rgb('#0f0')
    (0.0, 1.0, 0.0)

    >>> hex2rgb('#aaa')  # doctest: +ELLIPSIS
    (0.66..., 0.66..., 0.66...)

    >>> hex2rgb('#aa')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: Invalid value '#aa' provided for rgb color.

    """

    try:
        rgb = str_rgb[1:]

        if len(rgb) == 6:
            r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
        elif len(rgb) == 3:
            r, g, b = rgb[0] * 2, rgb[1] * 2, rgb[2] * 2
        else:
            raise ValueError()
    except:
        raise ValueError("Invalid value %r provided for rgb color."
                         % str_rgb)

    return tuple([float(int(v, 16)) / 255 for v in (r, g, b)])


def hex2web(hex):
    """Converts HEX representation to WEB

    :param rgb: 3 hex char or 6 hex char string representation
    :rtype: web string representation (human readable if possible)

    WEB representation uses X11 rgb.txt to define conversion
    between RGB and english color names.

    Usage
    =====

    >>> from colour import hex2web

    >>> hex2web('#ff0000')
    'red'

    >>> hex2web('#aaaaaa')
    '#aaa'

    >>> hex2web('#abc')
    '#abc'

    >>> hex2web('#acacac')
    '#acacac'

    """
    dec_rgb = tuple(int(v * 255) for v in hex2rgb(hex))
    if dec_rgb in RGB_TO_COLOR_NAMES:
        ## take the first one
        color_name = RGB_TO_COLOR_NAMES[dec_rgb][0]
        ## Enforce full lowercase for single worded color name.
        return color_name if len(re.sub(r"[^A-Z]", "", color_name)) > 1 \
               else color_name.lower()

    # Hex format is verified by hex2rgb function. And should be 3 or 6 digit
    if len(hex) == 7:
        if hex[1] == hex[2] and \
           hex[3] == hex[4] and \
           hex[5] == hex[6]:
            return '#' + hex[1] + hex[3] + hex[5]
    return hex


def web2hex(web, force_long=False):
    """Converts WEB representation to HEX

    :param rgb: web string representation (human readable if possible)
    :rtype: 3 hex char or 6 hex char string representation

    WEB representation uses X11 rgb.txt to define conversion
    between RGB and english color names.

    Usage
    =====

    >>> from colour import web2hex

    >>> web2hex('red')
    '#f00'

    >>> web2hex('#aaa')
    '#aaa'

    >>> web2hex('#foo')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    AttributeError: '#foo' is not in web format. Need 3 or 6 hex digit.

    >>> web2hex('#aaa', force_long=True)
    '#aaaaaa'

    >>> web2hex('#aaaaaa')
    '#aaaaaa'

    >>> web2hex('#aaaa')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    AttributeError: '#aaaa' is not in web format. Need 3 or 6 hex digit.

    >>> web2hex('pinky')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: 'pinky' is not a recognized color.

    And color names are case insensitive:

    >>> Color('RED')
    <Color red>

    """
    if web.startswith('#'):
        if (LONG_HEX_COLOR.match(web) or
            (not force_long and SHORT_HEX_COLOR.match(web))):
            return web.lower()
        elif SHORT_HEX_COLOR.match(web) and force_long:
            return '#' + ''.join([("%s" % (t, )) * 2 for t in web[1:]])
        raise AttributeError(
            "%r is not in web format. Need 3 or 6 hex digit." % web)

    web = web.lower()
    if web not in COLOR_NAME_TO_RGB:
        raise ValueError("%r is not a recognized color." % web)

    ## convert dec to hex:

    return rgb2hex([float(int(v)) / 255 for v in COLOR_NAME_TO_RGB[web]],
                   force_long)


## Missing functions conversion

hsl2hex = lambda x: rgb2hex(hsl2rgb(x))
hex2hsl = lambda x: rgb2hsl(hex2rgb(x))
rgb2web = lambda x: hex2web(rgb2hex(x))
web2rgb = lambda x: hex2rgb(web2hex(x))
web2hsl = lambda x: rgb2hsl(web2rgb(x))
hsl2web = lambda x: rgb2web(hsl2rgb(x))


def color_scale(begin_hsl, end_hsl, nb):
    """Returns a list of nb color HSL tuples between begin_hsl and end_hsl

    >>> from colour import color_scale

    >>> [rgb2hex(hsl2rgb(hsl)) for hsl in color_scale((0, 1, 0.5),
    ...                                               (1, 1, 0.5), 3)]
    ['#f00', '#0f0', '#00f', '#f00']

    >>> [rgb2hex(hsl2rgb(hsl))
    ...  for hsl in color_scale((0, 0, 0),
    ...                         (0, 0, 1),
    ...                         15)]  # doctest: +ELLIPSIS
    ['#000', '#111', '#222', ..., '#ccc', '#ddd', '#eee', '#fff']

    Of course, asking for negative values is not supported:

    >>> color_scale((0, 1, 0.5), (1, 1, 0.5), -2)
    Traceback (most recent call last):
    ...
    ValueError: Unsupported negative number of colors (nb=-2).

    """

    if nb < 0:
        raise ValueError(
            "Unsupported negative number of colors (nb=%r)." % nb)

    step = tuple([float(end_hsl[i] - begin_hsl[i]) / nb for i in range(0, 3)]) \
           if nb > 0 else (0, 0, 0)

    def mul(step, value):
        return tuple([v * value for v in step])

    def add_v(step, step2):
        return tuple([v + step2[i] for i, v in enumerate(step)])

    return [add_v(begin_hsl, mul(step, r)) for r in range(0, nb + 1)]


##
## Color Pickers
##

def RGB_color_picker(obj):
    """Build a color representation from the string representation of an object

    This allows to quickly get a color from some data, with the
    additional benefit that the color will be the same as long as the
    (string representation of the) data is the same::

        >>> from colour import RGB_color_picker, Color

    Same inputs produce the same result::

        >>> RGB_color_picker("Something") == RGB_color_picker("Something")
        True

    ... but different inputs produce different colors::

        >>> RGB_color_picker("Something") != RGB_color_picker("Something else")
        True

    In any case, we still get a ``Color`` object::

        >>> isinstance(RGB_color_picker("Something"), Color)
        True

    """

    ## Turn the input into a by 3-dividable string. SHA-384 is good because it
    ## divides into 3 components of the same size, which will be used to
    ## represent the RGB values of the color.
    digest = hashlib.sha384(str(obj).encode('utf-8')).hexdigest()

    ## Split the digest into 3 sub-strings of equivalent size.
    subsize = int(len(digest) / 3)
    splitted_digest = [digest[i * subsize: (i + 1) * subsize]
                       for i in range(3)]

    ## Convert those hexadecimal sub-strings into integer and scale them down
    ## to the 0..1 range.
    max_value = float(int("f" * subsize, 16))
    components = (
        int(d, 16)     ## Make a number from a list with hex digits
        / max_value    ## Scale it down to [0.0, 1.0]
        for d in splitted_digest)

    return Color(rgb2hex(components))  ## Profit!


def hash_or_str(obj):
    try:
        return hash((type(obj).__name__, obj))
    except TypeError:
        ## Adds the type name to make sure two object of different type but
        ## identical string representation get distinguished.
        return type(obj).__name__ + str(obj)


##
## All purpose object
##

class Color(object):
    """Abstraction of a color object

    Color object keeps information of a color. It can input/output to different
    format (HSL, RGB, HEX, WEB) and their partial representation.

        >>> from colour import Color, HSL

        >>> b = Color()
        >>> b.hsl = HSL.BLUE

    Access values
    -------------

        >>> b.hue  # doctest: +ELLIPSIS
        0.66...
        >>> b.saturation
        1.0
        >>> b.luminance
        0.5

        >>> b.red
        0.0
        >>> b.blue
        1.0
        >>> b.green
        0.0

        >>> b.rgb
        (0.0, 0.0, 1.0)
        >>> b.hsl  # doctest: +ELLIPSIS
        (0.66..., 1.0, 0.5)
        >>> b.hex
        '#00f'

    Change values
    -------------

    Let's change Hue toward red tint:

        >>> b.hue = 0.0
        >>> b.hex
        '#f00'

        >>> b.hue = 2.0/3
        >>> b.hex
        '#00f'

    In the other way round:

        >>> b.hex = '#f00'
        >>> b.hsl
        (0.0, 1.0, 0.5)

    Long hex can be accessed directly:

        >>> b.hex_l = '#123456'
        >>> b.hex_l
        '#123456'
        >>> b.hex
        '#123456'

        >>> b.hex_l = '#ff0000'
        >>> b.hex_l
        '#ff0000'
        >>> b.hex
        '#f00'

    Convenience
    -----------

        >>> c = Color('blue')
        >>> c
        <Color blue>
        >>> c.hue = 0
        >>> c
        <Color red>

        >>> c.saturation = 0.0
        >>> c.hsl  # doctest: +ELLIPSIS
        (..., 0.0, 0.5)
        >>> c.rgb
        (0.5, 0.5, 0.5)
        >>> c.hex
        '#7f7f7f'
        >>> c
        <Color #7f7f7f>

        >>> c.luminance = 0.0
        >>> c
        <Color black>

        >>> c.hex
        '#000'

        >>> c.green = 1.0
        >>> c.blue = 1.0
        >>> c.hex
        '#0ff'
        >>> c
        <Color cyan>

        >>> c = Color('blue', luminance=0.75)
        >>> c
        <Color #7f7fff>

        >>> c = Color('red', red=0.5)
        >>> c
        <Color #7f0000>

        >>> print(c)
        #7f0000

    You can try to query unexisting attributes:

        >>> c.lightness  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        AttributeError: 'lightness' not found

    TODO: could add HSV, CMYK, YUV conversion.

#     >>> b.hsv
#     >>> b.value
#     >>> b.cyan
#     >>> b.magenta
#     >>> b.yellow
#     >>> b.key
#     >>> b.cmyk


    Recursive init
    --------------

    To support blind conversion of web strings (or already converted object),
    the Color object supports instantiation with another Color object.

        >>> Color(Color(Color('red')))
        <Color red>

    Equality support
    ----------------

    Default equality is RGB hex comparison:

        >>> Color('red') == Color('blue')
        False
        >>> Color('red') == Color('red')
        True
        >>> Color('red') != Color('blue')
        True
        >>> Color('red') != Color('red')
        False

    But this can be changed:

        >>> saturation_equality = lambda c1, c2: c1.luminance == c2.luminance
        >>> Color('red', equality=saturation_equality) == Color('blue')
        True


    Subclassing support
    -------------------

    You should be able to subclass ``Color`` object without any issues::

        >>> class Tint(Color):
        ...     pass

    And keep the internal API working::

        >>> Tint("red").hsl
        (0.0, 1.0, 0.5)

    """

    _hsl = None   ## internal representation

    def __init__(self, color=None,
                 pick_for=None, picker=RGB_color_picker, pick_key=hash_or_str,
                 **kwargs):

        if pick_key is None:
            pick_key = lambda x: x

        if pick_for is not None:
            color = picker(pick_key(pick_for))

        if isinstance(color, Color):
            self.web = color.web
        else:
            self.web = color if color else 'black'

        self.equality = RGB_equivalence

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __getattr__(self, label):
        if label.startswith("get_"):
            raise AttributeError("'%s' not found" % label)
        try:
            return getattr(self, 'get_' + label)()
        except AttributeError:
            raise AttributeError("'%s' not found" % label)

    def __setattr__(self, label, value):
        if label not in ["_hsl", "equality"]:
            fc = getattr(self, 'set_' + label)
            fc(value)
        else:
            self.__dict__[label] = value

    ##
    ## Get
    ##

    def get_hsl(self):
        return tuple(self._hsl)

    def get_hex(self):
        return rgb2hex(self.rgb)

    def get_hex_l(self):
        return rgb2hex(self.rgb, force_long=True)

    def get_rgb(self):
        return hsl2rgb(self.hsl)

    def get_hue(self):
        return self.hsl[0]

    def get_saturation(self):
        return self.hsl[1]

    def get_luminance(self):
        return self.hsl[2]

    def get_red(self):
        return self.rgb[0]

    def get_green(self):
        return self.rgb[1]

    def get_blue(self):
        return self.rgb[2]

    def get_web(self):
        return hex2web(self.hex)

    ##
    ## Set
    ##

    def set_hsl(self, value):
        self._hsl = list(value)

    def set_rgb(self, value):
        self.hsl = rgb2hsl(value)

    def set_hue(self, value):
        self._hsl[0] = value

    def set_saturation(self, value):
        self._hsl[1] = value

    def set_luminance(self, value):
        self._hsl[2] = value

    def set_red(self, value):
        _, g, b = self.rgb
        self.rgb = (value, g, b)

    def set_green(self, value):
        r, _, b = self.rgb
        self.rgb = (r, value, b)

    def set_blue(self, value):
        r, g, _ = self.rgb
        self.rgb = (r, g, value)

    def set_hex(self, value):
        self.rgb = hex2rgb(value)

    set_hex_l = set_hex

    def set_web(self, value):
        self.hex = web2hex(value)

    def set_xkcd(self, value):
        self.hex = XKCD_COLOR_NAME_TO_HEX[value]

    ## range of color generation

    def range_to(self, value, steps):
        for hsl in color_scale(self._hsl, Color(value).hsl, steps - 1):
            yield Color(hsl=hsl)

    ##
    ## Convenience
    ##

    def __str__(self):
        return "%s" % self.web

    def __repr__(self):
        return "<Color %s>" % self.web

    def __eq__(self, other):
        if isinstance(other, Color):
            return self.equality(self, other)
        return NotImplemented

    if sys.version_info[0] == 2:
        ## Note: intended to be a backport of python 3 behavior
        def __ne__(self, other):
            equal = self.__eq__(other)
            return equal if equal is NotImplemented else not equal


RGB_equivalence = lambda c1, c2: c1.hex_l == c2.hex_l
HSL_equivalence = lambda c1, c2: c1._hsl == c2._hsl


def make_color_factory(**kwargs_defaults):

    def ColorFactory(*args, **kwargs):
        new_kwargs = kwargs_defaults.copy()
        new_kwargs.update(kwargs)
        return Color(*args, **new_kwargs)
    return ColorFactory
