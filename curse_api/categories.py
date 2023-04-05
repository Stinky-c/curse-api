from enum import IntEnum
from .enums import Games


class BaseCategory(IntEnum):
    """Base of all game categories"""


class Demeo_Categories(BaseCategory):
    pc = 5300
    vr = 5301
    utility = 5225
    mods = 5223
    library = 5227
    gameplay = 5226


class Wildstar_Categories(BaseCategory):
    twitch_integration = 4676
    spellslinger = 4412
    map_and_minimap = 4430
    soldier = 4438
    outfitter = 4419
    damage_dealer = 4440
    bags_bank_and_inventory = 4404
    explorer = 4435
    development_tools = 4424
    relic_hunter = 4420
    stalker = 4413
    tailor = 4423
    farming = 4427
    medic = 4411
    settler = 4437
    esper = 4409
    healer = 4441
    mining = 4418
    class_specific = 4408
    architect = 4416
    engineer = 4410
    scientist = 4436
    path_specific = 4434
    guild = 4425
    miscellaneous = 255
    chat_and_communication = 4407
    artwork_and_decoration = 4402
    technologist = 4422
    roleplaying = 4443
    pvp = 4432
    crafting = 4415
    boss_encounters = 4405
    armorer = 4417
    cooking = 4426
    fishing = 4428
    quests_and_leveling = 4433
    tank = 4442
    action_bars = 4401
    buffs_and_debuffs = 4406
    unit_frames = 4445
    warrior = 4414
    plugins = 4431
    libraries = 4429
    tooltip = 4444
    auction_and_economy = 4403
    survivalist = 4421
    ws_addons = 18
    role_specific = 4439


class Chronicles_of_arcadia_Categories(BaseCategory):
    auction_economy = 4786
    development_tools = 4790
    twitch_integration = 4800
    pvp = 4795
    quests_leveling = 4796
    chat_communication = 4788
    huds = 4799
    crafting = 4789
    unit_frames = 4798
    libraries = 4791
    bags_inventory = 4787
    addons = 4783
    action_bars = 4784
    miscellaneous = 4794
    map_minimap = 4792
    minigames = 4793
    tooltip = 4797
    artwork = 4785


class Final_fantasy_iii_Categories(BaseCategory):
    enemy_sprite = 5835
    window_frames = 5849
    title_screen = 5843
    fonts = 5836
    battle_scene = 5834
    gameplay = 5838
    game_overhauls = 5837
    player_npc_sprite = 5839
    tile_set = 5842
    menu_portraits = 5847
    ui = 5845
    script_text = 5840
    mods = 5833
    textbox_portraits = 5848
    general = 5846
    utility = 5844
    soundtrack = 5841


class Rom_Categories(BaseCategory):
    quests_leveling = 4579
    chat_communication = 4572
    crafting = 4586
    miscellaneous = 4581
    twitch_integration = 4679
    bags_inventory = 4576
    development_tools = 4583
    minigames = 4584
    map_minimap = 4578
    addons = 4571
    unit_frames = 4580
    libraries = 4577
    action_bars = 4582
    huds = 4587
    artwork = 4575
    auction_economy = 4573
    tooltip = 4585
    pvp = 4574


class Civ6_Categories(BaseCategory):
    mods = 4852
    building = 4855
    technology_or_civic = 4857
    great_person = 4858
    unit = 4854
    leader = 4856
    civilization = 4853


class Final_fantasy_v_Categories(BaseCategory):
    gameplay = 5873
    tile_set = 5877
    soundtrack = 5876
    title_screen = 5878
    fonts = 5871
    game_overhauls = 5872
    player_npc_sprite = 5874
    general = 5880
    textbox_portraits = 5882
    mods = 5867
    enemy_sprite = 5870
    menu_portraits = 5881
    window_frames = 5883
    ui = 5868
    battle_scene = 5869
    utility = 5879
    script_text = 5875


class Final_fantasy_i_Categories(BaseCategory):
    title_screen = 5809
    player_npc_sprite = 5805
    battle_scene = 5800
    script_text = 5806
    game_overhauls = 5803
    fonts = 5802
    menu_portraits = 5813
    textbox_portraits = 5814
    window_frames = 5815
    gameplay = 5804
    enemy_sprite = 5801
    utility = 5810
    general = 5812
    soundtrack = 5807
    tile_set = 5808
    mods = 5799
    ui = 5811


class Teso_Categories(BaseCategory):
    sorcerer = 329
    class_specific = 327
    buffs_and_debuffs = 350
    bags_bank_and_inventory = 348
    development_tools = 349
    unit_frames = 360
    boss_encounters = 361
    pvp = 354
    quests_and_leveling = 357
    auction_and_economy = 347
    libraries = 352
    templar = 330
    twitch_integration = 4681
    artwork = 346
    roleplaying = 355
    healer = 337
    miscellaneous = 326
    nightblade = 336
    armorsmithing = 340
    alchemy = 343
    crafting = 339
    provisioning = 344
    role_specific = 333
    dragonknight = 328
    guild = 351
    weaponsmithing = 341
    tooltip = 356
    map = 358
    damage_dealer = 335
    chat_and_communication = 345
    tank = 338
    teso_addons = 19
    enchanting = 342
    plugins = 359
    action_bars = 332


class Sims4_Categories(BaseCategory):
    sims = 5693
    lighting_and_shaders = 5742
    graphic_overhauls = 5741
    sets = 5605
    skin_details = 5710
    pants = 5704
    kitchen = 5643
    living_room = 5625
    lighting = 6024
    electronics = 6023
    makeup = 5610
    activities_and_skills = 5673
    venue = 5662
    kids_room = 5648
    miscellaneous = 5745
    head_accessories = 5923
    gameplay = 5091
    study = 5649
    hairstyles = 5606
    landscaping = 5612
    body_accessories = 5603
    bathroom = 5644
    functional_objects = 5940
    bedroom = 5645
    outdoors = 5650
    cats = 5666
    body_and_face_presets = 5711
    storage = 5675
    house = 5655
    underwear_and_socks = 5602
    tattoos = 5608
    teen = 6142
    skintones = 5609
    eye_color = 5607
    career = 5652
    elder = 6141
    traits = 5598
    shirts = 5600
    utilities = 5596
    likes_dislikes = 5939
    shoes = 5601
    toddler = 6144
    events = 5925
    families = 5702
    build_mode = 5438
    adult = 6139
    child = 6140
    bug_fixes = 5941
    scenarios = 5926
    map_replacements = 5743
    skirts = 5705
    clothing = 5340
    other_community = 5664
    poses_and_animations = 5599
    apartment = 5656
    entertainment = 5679
    facial_body_hair = 5611
    skins = 5709
    young_adult = 6143
    styled_looks = 5604
    dining_room = 5647
    pet_accessories = 5668
    aspirations = 5924
    body_sliders = 5716
    bar = 5660
    overrides = 5927
    park = 5659
    misc = 5651
    world_replacements = 5740
    dogs = 5667
    body = 5341
    other_residentials = 5657
    households = 5701
    shop = 5922
    buy_mode = 5621
    club = 5661
    careers = 5597
    face_sliders = 5715
    highschool = 5658
    pets = 5665
    roommates = 5703
    dresses = 5706
    recipes = 5934
    foundation_platforms = 6021
    water_overlays = 5930
    walls = 5616
    infant = 6180
    masculine = 5918
    mods = 5089
    roofing = 5620
    wallpapers = 5613
    community = 5653
    doors = 5617
    terrain_paints = 5929
    windows = 5618
    rooms = 5440
    save_files = 5965
    feminine = 5919
    build_buy = 5437
    residentials = 5654
    comfort = 5677
    create_a_sim = 5339
    decor = 5676
    occult = 5700
    stairs = 5619
    other_pets = 5977
    platform_trim = 6022
    floor_tiles = 5614
    worlds = 5739
    recreation_center = 6181
    rooms_lots = 5344
    sims_households = 5681


class Tsw_Categories(BaseCategory):
    chat_and_communication = 229
    bags_inventory = 227
    pvp = 233
    combat_tools = 239
    trading_post = 235
    miscellaneous = 231
    data_export = 237
    deck_gear_management = 240
    twitch_integration = 4680
    tsw_mods = 14
    action_bars = 224
    map_minimap = 230
    achievements = 223
    assembly = 226
    artwork = 225
    unit_frames = 236
    missions = 232
    roleplay = 234
    cabal = 228


class Among_us_Categories(BaseCategory):
    sounds = 4815
    miscellaneous = 4809
    textures = 4813
    maps = 4814
    guis = 4816
    game_modes = 4821
    all_mods = 4808
    skins = 4812


class Minecraft_Categories(BaseCategory):
    teleportation = 134
    lucky_blocks = 4548
    building_gadgets = 4752
    addons_buildcraft = 432
    galacticraft = 5232
    worlds = 17
    role_playing = 132
    hardcore_questing_mode = 4551
    guidebook = 4549
    admin_tools = 115
    addons_tinkers_construct = 428
    customization = 4546
    fancymenu = 5186
    world_structures = 409
    mc_addons = 4559
    armor_weapons_tools = 434
    world_generators = 131
    fun = 126
    website_administration = 130
    miscellaneous = 405
    technology_genetics = 418
    sci_fi = 4474
    blood_magic = 4485
    resource_packs = 4561
    progression = 4556
    one_twenty_eight_x = 396
    developer_tools = 122
    mechanics = 129
    chat_related = 117
    mc_miscellaneous = 425
    anti_griefing_tools = 116
    world_mobs = 411
    multiplayer = 4484
    recipes = 4554
    map_information = 423
    five_twelve_x_and_beyond = 398
    game_map = 250
    sixty_four_x = 395
    mini_game = 4477
    medieval = 402
    addons_thaumcraft = 430
    twitch_integration = 4671
    creation = 249
    modpacks = 4471
    technology_player_transport = 414
    technology_item_fluid_energy_transport = 415
    steampunk = 399
    technology_automation = 4843
    world_gen = 4555
    data_packs = 5193
    small_light = 4481
    adventure_and_rpg = 4475
    configuration = 4547
    mc_food = 436
    world_editing_and_management = 124
    crafttweaker = 4553
    hardcore = 4479
    combat_pvp = 4483
    kubejs = 5314
    world_biomes = 407
    technology_energy = 417
    addons_thermalexpansion = 427
    vanilla = 5128
    traditional = 403
    bukkit_plugins = 5
    fixes = 125
    addons_industrialcraft = 429
    library_api = 421
    adventure_rpg = 422
    font_packs = 5244
    utility_qol = 5191
    texture_packs = 12
    economy = 123
    scenarios = 4562
    server_utility = 435
    skyblock = 6145
    technology_farming = 416
    general = 127
    adventure = 248
    informational = 128
    modded_world = 4464
    survival = 253
    quests = 4550
    map_based = 4480
    animated = 404
    redstone = 4558
    magic = 4473
    addons_forestry = 433
    education = 5299
    cosmetic = 424
    tech = 4472
    technology = 412
    storage = 420
    two_fifty_six_x = 397
    photo_realistic = 400
    mod_support = 4465
    world_dimensions = 410
    applied_energistics_2 = 4545
    sixteen_x = 393
    world_ores_resources = 408
    extra_large = 4482
    technology_processing = 413
    mc_creator = 4906
    exploration = 4476
    thirty_two_x = 394
    ftb_official_pack = 4487
    scripts = 4552
    modern = 401
    parkour = 251
    mc_mods = 6
    puzzle = 252


class Final_fantasy_vi_Categories(BaseCategory):
    utility = 5793
    enemy_sprite = 5784
    tile_set = 5791
    mods = 5750
    title_screen = 5792
    player_npc_sprite = 5788
    gameplay = 5787
    general = 5795
    window_frames = 5798
    script_text = 5789
    soundtrack = 5790
    game_overhauls = 5786
    textbox_portraits = 5797
    ui = 5794
    menu_portraits = 5796
    fonts = 5785
    battle_scene = 5751


class Swlegends_Categories(BaseCategory):
    deck_gear_management = 4609
    data_export = 4607
    bags_inventory = 4597
    missions = 4602
    roleplay = 4604
    combat_tools = 4608
    artwork = 4595
    cabal = 4598
    unit_frames = 4606
    trading_post = 4605
    action_bars = 4594
    pvp = 4603
    chat_and_communication = 4599
    map_minimap = 4600
    twitch_integration = 4684
    achievements = 4593
    tswl_mods = 4592
    assembly = 4596
    miscellaneous = 4601


class Worldoftanks_Categories(BaseCategory):
    garage = 192
    target_markers = 218
    german = 201
    sights = 193
    czechoslovakia = 4611
    user_interface = 187
    ussr = 202
    japan = 293
    configurations = 216
    french = 203
    other = 220
    poland = 4610
    tools = 210
    british = 254
    twitch_integration = 4677
    icons = 205
    american = 200
    china = 221
    damage_panels = 217
    sweden = 4612
    environment = 222
    minimap = 219
    sounds = 188
    wot_mods = 8
    skins = 183
    packages = 209
    wot_skins = 9


class Terraria_Categories(BaseCategory):
    twitch_integration = 4748
    gardening_farms = 112
    fortresses_living_quarters = 108
    templates = 113
    optimizations = 4747
    multiplayer = 121
    art = 104
    survival = 114
    maps = 3
    items = 4745
    utilities_and_tools = 4746
    dungeons = 107
    adventures = 106
    parkour = 111
    items_storage = 109
    mods = 4744
    puzzles = 105
    pvp = 110


class Darkestdungeon_Categories(BaseCategory):
    overhauled_monsters = 4630
    core_mechanics = 4618
    localization = 4632
    gameplay = 4614
    inventory_tweaks = 4615
    new_classes = 4621
    new_monsters = 4629
    quests = 4616
    dd_mods = 4613
    c_skins = 4620
    t_skins = 4624
    new_trinkets = 4625
    trinkets = 4623
    monsters_creatures = 4627
    skins = 4628
    classes = 4619
    overhauled_trinkets = 4626
    overhaul_classes = 4622
    combat_tweaks = 4617
    ui = 4631


class Kerbal_Categories(BaseCategory):
    structural_and_aerodynamic = 4449
    flags_and_decals = 4461
    utility_and_navigation = 4466
    twitch_integration = 4674
    config_tweaks = 4462
    missions = 4660
    planes_and_ships = 4460
    science = 4450
    resources = 4455
    parts_pack = 4469
    sub_assembly = 4467
    command_and_control = 4448
    miscellaneous = 4451
    propulsion = 4447
    space_bases_and_stations = 4468
    physics = 4453
    ship_systems = 4454
    saved_games = 4459
    gameplay = 4456
    ksp_mods = 4470
    shareables = 4458


class Stardewvalley_Categories(BaseCategory):
    twitch_integration = 4682
    walkthrough = 4658
    achivements = 4644
    secrets = 4655
    gameplay_basics = 4650
    loot = 4651
    characters = 4645
    co_op = 4647
    game_modes = 4649
    crafting = 4648
    story = 4656
    trading = 4657
    mods = 4643
    weapons = 4659
    classes = 4646
    maps = 4652
    starjam = 4751
    modding = 4653


class Final_fantasy_iv_Categories(BaseCategory):
    textbox_portraits = 5865
    game_overhauls = 5854
    title_screen = 5860
    enemy_sprite = 5852
    soundtrack = 5858
    player_npc_sprite = 5856
    script_text = 5857
    battle_scene = 5851
    ui = 5862
    fonts = 5853
    menu_portraits = 5864
    general = 5863
    mods = 5850
    tile_set = 5859
    gameplay = 5855
    window_frames = 5866
    utility = 5861


class Wow_Categories(BaseCategory):
    titan_panel = 1065
    death_knight = 1036
    jewelcrafting = 1050
    leatherworking = 1051
    audio_video = 1003
    damage_dealer = 1035
    archaeology = 1103
    chat_communication = 1001
    twitch_integration = 4675
    demon_hunters = 1502
    transmogrification = 1171
    plugins = 1063
    paladin = 1022
    minigames = 1038
    achievements = 1067
    blacksmithing = 1043
    bags_inventory = 1009
    garrison = 1469
    auction_economy = 1002
    first_aid = 1047
    battleground = 1041
    libraries = 1010
    caster = 1034
    engineering = 1046
    boss_encounters = 1014
    pvp = 1004
    priest = 1026
    map_minimap = 1011
    data_broker = 1066
    enchanting = 1045
    monk = 1242
    fishing = 1048
    alchemy = 1042
    guild = 1008
    quests_leveling = 1013
    battle_pets = 1243
    fubar = 1064
    data_export = 1007
    herbalism = 1049
    addons = 1
    combat = 1019
    mail = 1012
    professions = 1015
    buffs_debuffs = 1005
    warlock = 1029
    inscription = 1059
    druid = 1023
    action_bars = 1018
    miscellaneous = 1017
    rogue = 1027
    skinning = 1053
    warrior = 1028
    roleplay = 1060
    huds = 1039
    development_tools = 1031
    companions = 1085
    shaman = 1025
    cooking = 1044
    artwork = 1006
    mage = 1021
    healer = 1032
    unit_frames = 1016
    raid_frames = 1037
    arena = 1040
    hunter = 1024
    class_ = 1020
    tailoring = 1054
    mining = 1052
    tooltip = 1055
    tank = 1033
    evoker = 6137


class Minecraft_dungeons_Categories(BaseCategory):
    resource_packs = 4949
    maps = 4947
    pets = 4946
    skins = 4951
    mods = 4944
    tools = 5975
    utility = 4983
    mobs = 4950
    capes = 4945


class Sc2_Categories(BaseCategory):
    minigames_sports = 72
    galaxy_scripts = 91
    roleplaying_games = 74
    buildings = 89
    war_craft_2 = 98
    war_craft_3 = 97
    tilesets = 92
    miscellaneous = 82
    textures = 93
    proof_of_concept = 100
    survivor = 76
    cooperative = 77
    capture_the_flag = 84
    star_craft_1 = 96
    melee = 81
    critter_games = 73
    hero_defense = 80
    units = 88
    hero_arena = 79
    base_defense = 69
    icons = 101
    maps = 4588
    library = 99
    training = 83
    scenario = 68
    legacy = 95
    tools = 90
    campaign = 70
    broken_maps = 102
    tower_defense = 75
    models = 94
    assets = 4
    ai = 86
    _3d_models = 87
    cinematics = 71
    tower_wars = 78


class Surviving_mars_Categories(BaseCategory):
    resources = 4668
    buildings = 4663
    units = 4669
    twitch_integration = 4673
    crops = 4665
    mods = 4662
    utilities = 4670
    research = 4667


class Final_fantasy_ii_Categories(BaseCategory):
    utility = 5827
    game_overhauls = 5820
    general = 5829
    soundtrack = 5824
    script_text = 5823
    ui = 5828
    gameplay = 5821
    player_npc_sprite = 5822
    textbox_portraits = 5831
    menu_portraits = 5830
    title_screen = 5826
    enemy_sprite = 5818
    battle_scene = 5817
    tile_set = 5825
    fonts = 5819
    window_frames = 5832
    mods = 5816


class Rift_Categories(BaseCategory):
    miscellaneous = 4567
    twitch_integration = 4678
    development_tools = 4569
    action_bars = 4568
    buffs_debuffs = 4565
    skins = 4570
    addons = 4564
    libraries = 4566


CATEGORIES = {
    Games.demeo: Demeo_Categories,
    Games.wildstar: Wildstar_Categories,
    Games.chronicles_of_arcadia: Chronicles_of_arcadia_Categories,
    Games.final_fantasy_iii: Final_fantasy_iii_Categories,
    Games.rom: Rom_Categories,
    Games.civ6: Civ6_Categories,
    Games.final_fantasy_v: Final_fantasy_v_Categories,
    Games.final_fantasy_i: Final_fantasy_i_Categories,
    Games.teso: Teso_Categories,
    Games.sims4: Sims4_Categories,
    Games.tsw: Tsw_Categories,
    Games.among_us: Among_us_Categories,
    Games.minecraft: Minecraft_Categories,
    Games.final_fantasy_vi: Final_fantasy_vi_Categories,
    Games.swlegends: Swlegends_Categories,
    Games.worldoftanks: Worldoftanks_Categories,
    Games.terraria: Terraria_Categories,
    Games.darkestdungeon: Darkestdungeon_Categories,
    Games.kerbal: Kerbal_Categories,
    Games.stardewvalley: Stardewvalley_Categories,
    Games.final_fantasy_iv: Final_fantasy_iv_Categories,
    Games.wow: Wow_Categories,
    Games.minecraft_dungeons: Minecraft_dungeons_Categories,
    Games.sc2: Sc2_Categories,
    Games.surviving_mars: Surviving_mars_Categories,
    Games.final_fantasy_ii: Final_fantasy_ii_Categories,
    Games.rift: Rift_Categories,
}
