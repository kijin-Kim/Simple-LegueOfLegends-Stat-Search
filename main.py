import tkinter as tk
import json
import math
import random
import time
from tkinter import messagebox
from DataLoader import*
from PIL import ImageTk,Image


class Application(tk.Frame):
      def __init__(self, master=None):
            super().__init__(master)
            self.master = master

            self.master.title("MY LOL GG")
            self.master.geometry("1366x575")
            self.master['background'] = "grey90"

            self.pack()
            self.create()

            self.dataLoader = DataLoader()

            self.profile_atlas = None

            self.progamer_dict = {
                  "faker" : "Hide on bush",
                  "teddy" : "천 번 찔린 테디",
                  "cuzz" : "T1 Cuzz"
            }

            self.test_name_list = [
                  "snarang", "진짜따효니", "은룡검탈론", "BCT 한동숙",
                  "민트초코하프갤런", "화웅 강소연", "칼챔전문가", "비빔전사 김팔도",
                  "상처투성E", "꿀벌내현", "파인트", "쿼터", "이도류"
            ]

            self.progamer_fns= [self.on_faker_pressed, self.on_teddy_pressed, self.on_cuzz_pressed]
            self.elapsed = 0
            self.update_clock()


      def update_clock(self):
            now = time.strftime("%H:%M:%S")
            self.master.after(1000, self.update_clock)
            self.elapsed += 1000

      def create(self):
            self.search_frame = tk.Frame(self.master)
            self.search_frame['background'] = "grey95"
            self.search_frame.place(x = 20, y = 20, width = 300, height = 36)

            self.search_entry = tk.Entry(self.search_frame, font = ('Consolas', 13))
            self.search_entry.place(x = 30, y= 5)

            self.search_button = tk.Button(self.search_frame, text = "검색")
            self.search_button.place(x = 220, y= 5)
            self.search_button["command"] = self.on_search_button_pressed

            self.random_button = tk.Button(self.search_frame, text = "랜덤")
            self.random_button.place(x = 260, y= 5)
            self.random_button["command"] = self.on_random_button_pressed


      def on_search_button_pressed(self):
            if self.elapsed >= 5000:
                  self.elapsed = 0
                  summoner_name = self.search_entry.get()
                  data = self.dataLoader.get_summoner_data(summoner_name)

                  if len(data) <= 1:
                        self.on_error_page()
                  else:
                        self.on_success_page(data)
            else:
                  tk.messagebox.showinfo(title= "Fail", message= "너무 빨리 검색하려 합니다. 잠시 기다려주세요")


      def on_random_button_pressed(self):
            summoner_name = random.choice(self.test_name_list)
            data = self.dataLoader.get_summoner_data(summoner_name)

            if len(data) <= 1:
                  self.on_error_page()
            else:
                  self.on_success_page(data)


      def summoner_query_data(self, summoner_name):
            data = self.dataLoader.get_summoner_data(summoner_name)
            self.on_success_page(data)



      def on_error_page(self):
            tk.messagebox.showinfo(title= "Fail", message= "플레이어를 찾을 수 없습니다.")

      def on_success_page(self, data):
            league_data = self.dataLoader.get_summoner_league(data['id'])

            data_path = "dragontail-10.13.1/10.13.1/data/ko_KR/"
            img_path = "dragontail-10.13.1/10.13.1/img/"

            with open(data_path + "profileicon.json", encoding='UTF8') as file:
                  profile_data = json.load(file)
            file.close()

            profile_image_data = profile_data['data'][str(data['profileIconId'])]['image']

            if not self.profile_atlas:
                  self.profile_atlas = Image.open(img_path + "sprite/" + profile_image_data['sprite']).convert("RGBA")

            cropped = self.profile_atlas.crop((profile_image_data['x'],
                                               profile_image_data['y'],
                                               profile_image_data['x'] + profile_image_data['w'],
                                               profile_image_data['y'] + profile_image_data['h']))

            player_indicator_frame = tk.Frame(self.master)
            player_indicator_frame['background'] = "grey95"
            player_indicator_frame.place(x = 20, y = 50 + 15, width = 300, height = 36)

            player_idicator_label = tk.Label(player_indicator_frame, text = "Player Rank Game Information", font = ('Consolas', 12, "bold"))
            player_idicator_label.place(x = 20, y= 75/2 - 48/2 - 10)

            self.default_information_frame = tk.Frame(self.master)
            self.default_information_frame['background'] = "grey95"
            self.default_information_frame.place(x = 20, y = 50 + 15 + 46, width = 300, height = 100)

            self.profile_image = ImageTk.PhotoImage(cropped)
            profile_image_label = tk.Label(self.default_information_frame, image = self.profile_image)
            profile_image_label.place(x = 20, y= 50 - 48/2)
            name_label = tk.Label(self.default_information_frame, text = data['name'], font = ('Consolas', 15, "bold"), bg = "grey95" )
            name_label.place(x = 80, y= 50 - 48/2)
            level_lable = tk.Label(self.default_information_frame, text = "Level " + str(data['summonerLevel']), font = ('Consolas', 10,"italic"), bg = "grey95" )
            level_lable.place(x = 80, y= 50 - 48/2 + 30)

            self.rank_information_frame = tk.Frame(self.master)
            self.rank_information_frame['background'] = "grey95"
            self.rank_information_frame.place(x = 20, y = 150 + 20 + 20 + 46, width = 300, height = 150)

            rank_information_frame = tk.Frame(self.master)
            rank_information_frame['background'] = "grey95"
            rank_information_frame.place(x = 20, y = 150 + 20 + 5 + 46, width = 300, height = 157)

            rank_information_frame2 = tk.Frame(self.master)
            rank_information_frame2['background'] = "grey95"
            rank_information_frame2.place(x = 20, y = 150 + 20 + 150 + 20 + 10 + 46 + 2, width = 300, height = 157)

            self.rank_frames = [ rank_information_frame, rank_information_frame2 ]

            self.rank_emblem_images=[]

            for i in range (0, len(league_data)):
                  rank_image = Image.open(img_path + "ranked-emblems/" + "Emblem_" + league_data[i]['tier'] + ".png")
                  self.rank_emblem_images.append(ImageTk.PhotoImage(rank_image))


            for i in range (0, len(league_data)):
                  rank_image_label = tk.Label(self.rank_frames[i], image = self.rank_emblem_images[i])
                  rank_image_label.place(x = 20, y= 150/2 - 55)
                  queue_label = tk.Label(self.rank_frames[i], text = league_data[i]['queueType'], font = ('Consolas', 10, "italic"), bg = "grey95" )
                  queue_label.place(x = 130, y= 50 - 20)
                  rank_label = tk.Label(self.rank_frames[i], text = league_data[i]['tier'] + " " + league_data[i]['rank']  , font = ('Consolas', 15, "bold"), bg = "grey95" )
                  rank_label.place(x = 130, y= 50)
                  lp_lw_text = str(league_data[i]['leaguePoints']) + "포인트 / " + str(league_data[i]['wins']) + "승 " + str(league_data[i]['losses']) + "패\n 승률 " \
                               + str( math.floor(league_data[i]['wins'] * 100 /(league_data[i]['wins'] + league_data[i]['losses']))) + "%"
                  lp_lw_label = tk.Label(self.rank_frames[i], text = lp_lw_text, font = ('Consolas', 10, "italic"), bg = "grey95", justify = "left")
                  lp_lw_label.place(x = 130, y= 50 + 10 + 15)


            matches = self.dataLoader.get_summoner_match(data['accountId'])
            self.champion_images = []

            self.match_informations = []
            for i in range (0, 4):
                  self.match_informations.append(self.dataLoader.get_match_information(str(matches['matches'][i]['gameId'])))

            self.participant_ids = []
            for i in range (0, 4):
                  for j in range(0, len(self.match_informations[i]['participantIdentities'])):
                        if self.match_informations[i]['participantIdentities'][j]['player']['accountId'] == data['accountId']:
                              self.participant_ids.append(self.match_informations[i]['participantIdentities'][j]['participantId'])

            for i in range(0,4):
                  with open(data_path + "champion.json", encoding='UTF8') as file:
                        champion_icon_data = json.load(file)
                  file.close()

                  match_champion_name = None
                  for champion_name in champion_icon_data['data']:
                        if champion_icon_data['data'][champion_name]["key"] == str(matches['matches'][i]['champion']):
                              match_champion_name = champion_name

                  with open(data_path + "champion/" +  match_champion_name + ".json", encoding='UTF8') as file:
                        champion_data = json.load(file)
                  file.close()

                  champion_atlas = Image.open(img_path + "sprite/" + champion_data['data'][match_champion_name]['image']['sprite']).convert("RGBA")

                  champion_cropped = champion_atlas.crop((champion_data['data'][match_champion_name]['image']['x'],
                                                     champion_data['data'][match_champion_name]['image']['y'],
                                                     champion_data['data'][match_champion_name]['image']['x'] + champion_data['data'][match_champion_name]['image']['w'],
                                                     champion_data['data'][match_champion_name]['image']['y'] + champion_data['data'][match_champion_name]['image']['h']))


                  self.champion_images.append(ImageTk.PhotoImage(champion_cropped))


            match_indicator_frame = tk.Frame(self.master)
            match_indicator_frame['background'] = "grey95"
            match_indicator_frame.place(x = 340, y = 20, width = 366, height = 36)

            match_label = tk.Label(match_indicator_frame, text = "Recent Game Information", font = ('Consolas', 12, "bold"))
            match_label.place(x = 20, y= 75/2 - 48/2 - 10)


            in_game_match_indicator_frame = tk.Frame(self.master)
            in_game_match_indicator_frame['background'] = "grey95"
            in_game_match_indicator_frame.place(x = 726, y = 20, width = 620, height = 36)

            match_label = tk.Label(in_game_match_indicator_frame, text = "Current Game-Playing Information", font = ('Consolas', 12, "bold"))
            match_label.place(x = 20, y= 75/2 - 48/2 - 10)


            self.matches_histroy_frame = tk.Frame(self.master)
            self.matches_histroy_frame['background'] = "grey95"
            self.matches_histroy_frame.place(x = 340, y = 65, width = 366, height = 325)

            for i in range(0, 4):
                  match_frame = tk.Frame(self.matches_histroy_frame)
                  frame_bg_color = None
                  if self.match_informations[i]['participants'][self.participant_ids[i] - 1]['stats']['win']:
                        frame_bg_color = "LightSteelBlue1"
                  else:
                        frame_bg_color = "thistle1"

                  match_frame['background'] = frame_bg_color

                  match_frame.place(x = 10, y = 5 + (5 + 75) * i, width = 350, height = 75)

                  match_label = tk.Label(match_frame, image = self.champion_images[i])
                  match_label.place(x = 20, y= 75/2 - 48/2)

                  if self.match_informations[i]['participants'][self.participant_ids[i] - 1]['stats']['deaths'] is not 0:
                        kda_ratio = str(round((self.match_informations[i]['participants'][self.participant_ids[i] - 1]['stats']['kills'] + \
                              self.match_informations[i]['participants'][self.participant_ids[i] - 1]['stats']['assists'])\
                              / self.match_informations[i]['participants'][self.participant_ids[i] - 1]['stats']['deaths'],2))
                  else:
                        kda_ratio = str((self.match_informations[i]['participants'][self.participant_ids[i] - 1]['stats']['kills'] + \
                              self.match_informations[i]['participants'][self.participant_ids[i] - 1]['stats']['assists']))

                  kda_ratio_label = tk.Label(match_frame, text = kda_ratio + " KDA", font = ('Consolas', 12, "bold"),
                                       bg = frame_bg_color)
                  kda_ratio_label.place(x = 20 + 80, y= 15)


                  kda = str(self.match_informations[i]['participants'][self.participant_ids[i] - 1]['stats']['kills']) + " / " \
                        + str(self.match_informations[i]['participants'][self.participant_ids[i] - 1]['stats']['deaths']) + " / "\
                        + str(self.match_informations[i]['participants'][self.participant_ids[i] - 1]['stats']['assists'])

                  kda_label = tk.Label(match_frame, text = kda, font = ('Consolas', 12, "bold"),
                                       bg = frame_bg_color)
                  kda_label.place(x = 20 + 80, y= 75/2 - 24/2 + 15)

                  game_duration = str(int(self.match_informations[i]['gameDuration'] / 60)) + ":" + str(self.match_informations[i]['gameDuration'] % 60)
                  game_duration_label = tk.Label(match_frame, text = "Game Duration\n" +  game_duration, font = ('Consolas', 12, "bold"),
                                       bg = frame_bg_color)
                  game_duration_label.place(x = 20 + 100 + 100, y= 75/2 - 24/2 - 10)




            self.shortcut_main_frame = tk.Frame(self.master)
            self.shortcut_main_frame['background'] = "grey95"
            self.shortcut_main_frame.place(x = 726, y = 65 + 10 + 325, width = 620, height = 155)

            self.progamer_images = []
            for name in self.progamer_dict:
                  self.progamer_images.append(ImageTk.PhotoImage(Image.open(img_path + "progamer/" + name + ".png").convert("RGBA")))

            self.progamer_buttons = []
            for i in range (0, len(self.progamer_images)):
                  self.progamer_buttons.append(tk.Button(self.shortcut_main_frame, image = self.progamer_images[i]))
                  self.progamer_buttons[i].place(x = 10+0 + i* 196, y= 0)
                  self.progamer_buttons[i]['command'] = self.progamer_fns[i]

            free_champion_ids = self.dataLoader.get_champion_rotation()['freeChampionIds']
            with open(data_path + "champion.json", encoding='UTF8') as file:
                  champions_data = json.load(file)
            file.close()
            self.rotation_sprites = []


            for i in champions_data['data']:
                  if int(champions_data['data'][i]['key']) in free_champion_ids:
                        atlas = Image.open(img_path + "sprite/" + champions_data['data'][i]['image']['sprite']).convert("RGBA")
                        cropped = atlas.crop((champions_data['data'][i]['image']['x'],
                                               champions_data['data'][i]['image']['y'],
                                               champions_data['data'][i]['image']['x'] + champions_data['data'][i]['image']['w'],
                                               champions_data['data'][i]['image']['y'] + champions_data['data'][i]['image']['h']))
                        self.rotation_sprites.append(ImageTk.PhotoImage(cropped))

            self.rotation_indicator = tk.Frame(self.master)
            self.rotation_indicator['background'] = "grey95"
            self.rotation_indicator.place(x = 340, y = 65 + 10 + 325, width = 366, height = 36)

            rotation_label = tk.Label(self.rotation_indicator, text = "This Week Free Champions", font = ('Consolas', 12, "bold"))
            rotation_label.place(x = 20, y= 75/2 - 48/2 - 10)


            self.rotation_frame = tk.Frame(self.master)
            self.rotation_frame['background'] = "grey95"
            self.rotation_frame.place(x = 340, y = 65 + 20 + 325 + 36, width = 366, height = 110)


            self.sprite_row = 0
            self.sprite_coloumn = 0
            increment = 0
            for i in range(0, len(self.rotation_sprites) - 1):
                  increment += 1
                  if increment > 7:
                        increment = 0
                        self.sprite_coloumn += 1
                        self.sprite_row = 0
                  temp = tk.Label(self.rotation_frame, image = self.rotation_sprites[i])
                  temp.place(x = 15 + (48 * self.sprite_row), y= 5 + (self.sprite_coloumn * 48))
                  self.sprite_row += 1

            current_game_information = self.dataLoader.get_current_game_information(data['id'])

            self.in_game_main_frame = tk.Frame(self.master)
            self.in_game_main_frame['background'] = "grey95"
            self.in_game_main_frame.place(x = 726, y = 65, width = 620, height = 325)





            self.blue_team_images = []
            self.blue_team_ids = []
            self.purple_team_images = []
            self.purple_team_ids = []

            if len(current_game_information) >= 2:
                  self.current_game_champions_id = {}

                  for i in current_game_information['participants']:
                      self.current_game_champions_id[i['championId']] = [i['teamId'], i['summonerName']]
                  for i in champions_data['data']:
                        if int(champions_data['data'][i]['key']) in self.current_game_champions_id:
                              atlas = Image.open(img_path + "sprite/" + champions_data['data'][i]['image']['sprite']).convert("RGBA")
                              cropped = atlas.crop((champions_data['data'][i]['image']['x'],
                                                     champions_data['data'][i]['image']['y'],
                                                     champions_data['data'][i]['image']['x'] + champions_data['data'][i]['image']['w'],
                                                     champions_data['data'][i]['image']['y'] + champions_data['data'][i]['image']['h']))
                              if self.current_game_champions_id[int(champions_data['data'][i]['key'])][0] == 100:
                                    self.blue_team_images.append([ImageTk.PhotoImage(cropped),self.current_game_champions_id[int(champions_data['data'][i]['key'])][1]])
                              else:
                                    self.purple_team_images.append([ImageTk.PhotoImage(cropped),self.current_game_champions_id[int(champions_data['data'][i]['key'])][1]])

                  self.purple_team_frames = []
                  self.blue_team_frames = []
                  n =0
                  for i in range(0, 2):
                            for j in range(0, 5):
                                    in_game_frame = tk.Frame(self.in_game_main_frame)
                                    in_game_frame.place(x = 7 +  + (10 + 290 + 3 + 3 + 30 ) * i,
                                                                 y =10 + (5 + 51.3 + 5.5) * j,
                                                                 width = 10 + 260,
                                                                 height = 5+ 52 )

                                    if i is 1 :
                                          in_game_frame['background'] = "thistle1"
                                          self.purple_team_frames.append(in_game_frame)
                                    else:
                                          in_game_frame['background'] = "LightSteelBlue1"
                                          self.blue_team_frames.append(in_game_frame)

                                    n = n+1


                  for i in range(0, len(self.blue_team_frames)):
                        in_game_champion_label = tk.Label(self.blue_team_frames[i], image = self.blue_team_images[i][0])
                        in_game_champion_label.place(x = 270 - 48 - 2, y= 2)

                        in_game_name_label = tk.Label(self.blue_team_frames[i], text = self.blue_team_images[i][1], font = ('Consolas', 13, 'bold'),
                                                      bg = "LightSteelBlue1")
                        in_game_name_label.place(x = 270 - 48 - 2 - 200, y= 48 - 30)

                  for i in range(0, len(self.purple_team_frames)):
                        in_game_champion_label = tk.Label(self.purple_team_frames[i], image = self.purple_team_images[i][0])
                        in_game_champion_label.place(x = 2, y= 2)

                        in_game_name_label = tk.Label(self.purple_team_frames[i], text = self.purple_team_images[i][1], font = ('Consolas', 13, 'bold'),
                                                      bg = "thistle1")
                        in_game_name_label.place(x = 48 + 20, y= 48 - 30)


      def on_faker_pressed(self):
            self.summoner_query_data(self.progamer_dict["faker"])
      def on_teddy_pressed(self):
            self.summoner_query_data(self.progamer_dict["teddy"])
      def on_cuzz_pressed(self):
            self.summoner_query_data(self.progamer_dict["cuzz"])








root = tk.Tk()
app = Application(master=root)
app.mainloop()







