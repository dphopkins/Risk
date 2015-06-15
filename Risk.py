"""
Dan Hopkins/Kenneth Gudel/Harrison Schell
CS 106
Term Project
Risk
3/26/14
"""

from Tkinter import *
from PIL import Image, ImageTk
import random
import sys
import time

class MainScreen(Canvas):
	def __init__(self, parent):
		self.w = Canvas(parent, width = 1000, height = 750, bg = 'steel blue')
		self.parent = parent
		self.parent.title("Risk")
		self.w.pack(fill=BOTH, expand=1)
		self.centerWindow()
		self.main_image = None
		self.extra_1 = None
		self.extra_2 = None
		self.extra_3 = None
		self.extra_4 = None
		self.extra_5 = None
		self.extra_6 = None
		self.chatbox = None
		self.chat = None
		self.enters = 0
		self.chatmem = []
		self.create_welcome_screen()
		self.cards = [None, None, None, None, None]
        

	def choose_players(self, num):
		global players
		players = num
		global names
		names = [0] * players

		self.newWindow = Toplevel(self.parent)
		self.app = NameScreen(self.newWindow, players)

	def start_game(self):
		create_player_instances()
		turn_order()

		self.redrawWindow()
		create_territories()
		assign_ownership()
		distribute_and_assign_armies()
		self.w.bind('<ButtonPress-1>', self.mb1callback)
		self.w.bind('<ButtonPress-2>', self.mb2callback)
		self.w.bind('<Return>', self.entercallback)

	def mb1callback(self, event):
		# Setup & Place armies
		if self.w.coords('turn_arrow') == [820, 225] or self.w.coords('turn_arrow') == [820, 250]:
			if self.w.coords('name_arrow') == [820, 42]:
				pool[0].place_armies(event.x, event.y)
			elif self.w.coords('name_arrow') == [820, 67]:
				pool[1].place_armies(event.x, event.y)
			elif self.w.coords('name_arrow') == [820, 92]:
				pool[2].place_armies(event.x, event.y)
			elif self.w.coords('name_arrow') == [820, 117]:
				pool[3].place_armies(event.x, event.y)
			elif self.w.coords('name_arrow') == [820, 142]:
				pool[4].place_armies(event.x, event.y)
			elif self.w.coords('name_arrow') == [820, 167]:
				pool[5].place_armies(event.x, event.y)

		# Invasions
		if self.w.coords('turn_arrow') == [820, 275]:
			if self.w.coords('name_arrow') == [820, 42]:
				pool[0].battle(event.x, event.y)
			elif self.w.coords('name_arrow') == [820, 67]:
				pool[1].battle(event.x, event.y)
			elif self.w.coords('name_arrow') == [820, 92]:
				pool[2].battle(event.x, event.y)
			elif self.w.coords('name_arrow') == [820, 117]:
				pool[3].battle(event.x, event.y)
			elif self.w.coords('name_arrow') == [820, 142]:
				pool[4].battle(event.x, event.y)
			elif self.w.coords('name_arrow') == [820, 167]:
				pool[5].battle(event.x, event.y)
		# Reinforce
		if self.w.coords('turn_arrow') == [820, 300]:
			if self.w.coords('name_arrow') == [820, 42]:
				pool[0].reinforce(event.x, event.y)
			elif self.w.coords('name_arrow') == [820, 67]:
				pool[1].reinforce(event.x, event.y)
			elif self.w.coords('name_arrow') == [820, 92]:
				pool[2].reinforce(event.x, event.y)
			elif self.w.coords('name_arrow') == [820, 117]:
				pool[3].reinforce(event.x, event.y)
			elif self.w.coords('name_arrow') == [820, 142]:
				pool[4].reinforce(event.x, event.y)
			elif self.w.coords('name_arrow') == [820, 167]:
				pool[5].reinforce(event.x, event.y)			

		# flip cards
		if event.x > 600 and event.x < 1000 and event.y > 544 and event.y < 750:
			if self.w.coords('name_arrow') == [820, 42]:
				pool[0].flip_cards()
				print 'happens'
			elif self.w.coords('name_arrow') == [820, 67]:
				pool[1].flip_cards()
			elif self.w.coords('name_arrow') == [820, 92]:
				pool[2].flip_cards()
			elif self.w.coords('name_arrow') == [820, 117]:
				pool[3].flip_cards()
			elif self.w.coords('name_arrow') == [820, 142]:
				pool[4].flip_cards()
			elif self.w.coords('name_arrow') == [820, 167]:
				pool[5].flip_cards()


	def mb2callback(self, event):
		print 'click 2'

	def system_message(self, message):
		position = []
		if self.enters > 0:
			for i in range(1, self.enters + 2):
				position += [1960 - (20 * i)]
			for j in range(1, self.enters + 1):
				self.chatbox.delete('entry' + str(j))
				self.chatbox.create_text((5, position[self.enters - j]), text = self.chatmem[j - 1], tag = 'entry' + str(j), anchor = 'w')
		self.enters += 1
		self.chatbox.create_text((5, 1960), text = "SYS: " + message, tags = 'entry' + str(self.enters), anchor = 'w')
		self.chatmem += ["SYS: " + message]

	def entercallback(self, event):
		position = []
		if self.enters > 0:
			for i in range(1, self.enters + 2):
				position += [1960 - (20 * i)]
			for j in range(1, self.enters + 1):
				self.chatbox.delete('entry' + str(j))
				self.chatbox.create_text((5, position[self.enters - j]), text = self.chatmem[j - 1], tag = 'entry' + str(j), anchor = 'w')
		self.enters += 1
		if self.w.coords('name_arrow') == [820, 42]:
			self.chatbox.create_text((5, 1960), text = str(pool[0].name) + ": " + self.chat.get(), tags = (self.chat.get(), 'entry' + str(self.enters)), anchor = 'w')			
			self.chatmem += [str(pool[0].name) + ": " + self.chat.get()]
		elif self.w.coords('name_arrow') == [820, 67]:
			self.chatbox.create_text((5, 1960), text = str(pool[1].name) + ": " + self.chat.get(), tags = (self.chat.get(), 'entry' + str(self.enters)), anchor = 'w')			
			self.chatmem += [str(pool[1].name) + ": " + self.chat.get()]
		elif self.w.coords('name_arrow') == [820, 92]:
			self.chatbox.create_text((5, 1960), text = str(pool[2].name) + ": " + self.chat.get(), tags = (self.chat.get(), 'entry' + str(self.enters)), anchor = 'w')			
			self.chatmem += [str(pool[2].name) + ": " + self.chat.get()]
		elif self.w.coords('name_arrow') == [820, 117]:
			self.chatbox.create_text((5, 1960), text = str(pool[3].name) + ": " + self.chat.get(), tags = (self.chat.get(), 'entry' + str(self.enters)), anchor = 'w')			
			self.chatmem += [str(pool[3].name) + ": " + self.chat.get()]
		elif self.w.coords('name_arrow') == [820, 142]:
			self.chatbox.create_text((5, 1960), text = str(pool[4].name) + ": " + self.chat.get(), tags = (self.chat.get(), 'entry' + str(self.enters)), anchor = 'w')			
			self.chatmem += [str(pool[4].name) + ": " + self.chat.get()]
		elif self.w.coords('name_arrow') == [820, 167]:
			self.chatbox.create_text((5, 1960), text = str(pool[5].name) + ": " + self.chat.get(), tags = (self.chat.get(), 'entry' + str(self.enters)), anchor = 'w')			
			self.chatmem += [str(pool[5].name) + ": " + self.chat.get()]
		self.chat.delete(0, len(self.chat.get()))

	def create_welcome_screen(self):
		image = Image.open("welcome.png")
		photo = ImageTk.PhotoImage(image)
		self.w.create_image((500, 375), image = photo)
		self.image = photo

		# Loading Quit Button
		q_im = Image.open('quit.png')
		q_pic = ImageTk.PhotoImage(q_im)
		q = Button(self.parent, image = q_pic, command = lambda: sys.exit())
		self.w.create_window(850, 675, window = q)
		self.extra_6 = q_pic

		# Loading Images for player buttons
		two_p_im = Image.open('two_players.png')
		two_p_pic = ImageTk.PhotoImage(two_p_im)
		two_players = Button(self.parent, image = two_p_pic, command = lambda: self.choose_players(2))
		self.w.create_window(203, 460, window = two_players)
		self.extra_1 = two_p_pic

		three_p_im = Image.open('three_players.png')
		three_p_pic = ImageTk.PhotoImage(three_p_im)
		three_players = Button(self.parent, image = three_p_pic, command = lambda: self.choose_players(3))
		self.w.create_window(203, 510, window = three_players)
		self.extra_2 = three_p_pic

		four_p_im = Image.open('four_players.png')
		four_p_pic = ImageTk.PhotoImage(four_p_im)
		four_players = Button(self.parent, image = four_p_pic, command = lambda: self.choose_players(4))
		self.w.create_window(203, 560, window = four_players)
		self.extra_3 = four_p_pic

		five_p_im = Image.open('five_players.png')
		five_p_pic = ImageTk.PhotoImage(five_p_im)
		five_players = Button(self.parent, image = five_p_pic, command = lambda: self.choose_players(5))
		self.w.create_window(203, 610, window = five_players)
		self.extra_4 = five_p_pic

		six_p_im = Image.open('six_players.png')
		six_p_pic = ImageTk.PhotoImage(six_p_im)
		six_players = Button(self.parent, image = six_p_pic, command = lambda: self.choose_players(6))
		self.w.create_window(203, 660, window = six_players)
		self.extra_5 = six_p_pic

	def redrawWindow(self):
		self.w.delete('all') # clear canvas

		# Create background
		newimage = Image.open('riskmap.png')
		newphoto = ImageTk.PhotoImage(newimage)
		self.w.create_image((400,272), image = newphoto, tag = 'background')
		self.image = newphoto

		# Create arrows
		arrowimage = Image.open('arrow.png')
		arrowphoto = ImageTk.PhotoImage(arrowimage)
		self.w.create_image((820,42), image = arrowphoto, tag = 'name_arrow')
		self.w.create_image((820, 225), image = arrowphoto, tag = 'turn_arrow')
		self.extra_1 = arrowphoto
		
		# Creating turn text
		self.w.create_text((900, 200), text = 'Game Phases', font = ('Times', 24, 'bold underline'))
		self.w.create_text((900, 225), text = 'Setup', font = ('Times', 24))
		self.w.create_text((900, 250), text = 'Place', font = ('Times', 24))
		self.w.create_text((900, 275), text = 'Invade', font = ('Times', 24))
		self.w.create_text((900, 300), text = 'Reinforce', font = ('Times', 24))
		self.w.create_text((900, 325), text = 'End of Turn', font = ('Times', 24))

		# Create player colors
		self.w.create_text((900,18), text = 'Names and Colors', font = ('Times', 24, 'bold underline'))
		starting_coords = 33
		for i in range(players):
			self.w.create_text((900, starting_coords + 9), text = pool[i].name, font = ('Times', 24))
			self.w.create_oval((975, starting_coords, 995, starting_coords + 20), fill = colors[i], outline = colors[i], tag = 'pcolor' + str(i))
			starting_coords += 25

		# Creating chatbox
		self.chatbox = Canvas(self.parent, width = 600, height = 196, bg = 'light sky blue', scrollregion = (0, 0, 2000, 2000))
		self.vbar = Scrollbar(self.chatbox, orient='vertical')
		self.vbar.place(x = 588, y = 3, height = 171)
		self.vbar.config(command = self.chatbox.yview)
		self.chatbox.place(x =0, y =750, anchor = 'sw')
		self.chatbox.config(yscrollcommand = self.vbar.set)
		self.chat = Entry(self.parent, width = 60)
		self.chat.place(x = 0, y = 750, anchor = 'sw')
		self.chat.bind('<Return>', self.entercallback)
		global send_button
		send_button = Button(self.parent, text = 'Send', command = lambda: self.entercallback(True))
		send_button.place(x = 492, y = 722)


		# Adding quit button
		global quit_button
		quit_button = Button(self.parent, text = 'Quit', command = sys.exit)
		quit_button.place(x = 551, y = 722)


	def updateNameArrow(self):
		coord = self.w.coords('name_arrow')
		threshold = 42 + ((players - 1) * 25)
		if coord[1] + 25 > threshold:
			self.w.coords('name_arrow', (820, 42))
		else:
			self.w.coords('name_arrow', (coord[0], coord[1] + 25))

	def updateTurnArrow(self):
		coord = self.w.coords('turn_arrow')
		if coord[1] > 300:
			self.w.coords('turn_arrow', (820, 250))
		else:
			self.w.coords('turn_arrow', (coord[0], coord[1] + 25))

	def centerWindow(self):
		w = 1000
		h = 750

		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()

		x = (sw - w)/2
		y = (sh - h)/2
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


class NameScreen():
	def __init__(self, master, i):
		self.master = master
		self.master.title('Player Names')
		self.entries = []
		for j in range(0, i):
			self.entries += [Entry(self.master)]
			self.entries[j].pack()
		self.enterButton = Button(self.master, text = 'Enter', command = lambda: self.assign_names())
		self.enterButton.pack()
		self.centerWindow()
		
	def assign_names(self):
		global names
		names = []
		for j in self.entries:
			text = j.get()
			names += [text]
		self.close_windows()

	def close_windows(self):
		self.master.destroy()
		w.start_game()

	def centerWindow(self):
		w = 200
		h = 200

		sw = self.master.winfo_screenwidth()
		sh = self.master.winfo_screenheight()

		x = (sw - w)/2
		y = (sh - h)/2
		self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))



class Territory:
	def __init__(self, name, continent, id, owner, armies, borders, win, coords):
		self.name = name
		self.continent = continent
		self.id = int(id)
		self.owner = owner
		self.armies = armies
		self.borders = borders
		self.color = 'black'
		self.win = win
		self.tag = self.name.replace(' ', '')
		win.create_oval((coords[0]-15, coords[1]-15, coords[0]+15, coords[1]+15), fill = self.color, outline = self.color, activeoutline = 'black', tag = self.tag)
		self.armies_text = win.create_text(coords, text = str(self.armies), tag = self.tag + 'text')

	def update_color(self):
		for i in pool:
			if i.name == self.owner:
				self.color = i.color
				self.win.itemconfig(self.tag, fill = self.color, outline = self.color)

	def update_armies(self):
		self.win.itemconfig(self.tag + 'text', text = str(self.armies))



class Player:
	def __init__(self, turn, name, armies):
		self.turn = turn
		self.name = name
		self.color = None
		self.armies = 0
		self.my_territories = []
		self.my_cards =[]

	def flip_cards(self):
		global swap
		card_coords = [(642,646), (722,646), (801,646), (880,646), (959,646)]
		if swap == True:
			cannonimage = Image.open('cannon.png')
			cannonphoto = [ImageTk.PhotoImage(cannonimage), ImageTk.PhotoImage(cannonimage), ImageTk.PhotoImage(cannonimage), ImageTk.PhotoImage(cannonimage), ImageTk.PhotoImage(cannonimage)]
			horseimage = Image.open('horse.png')
			horsephoto = [ImageTk.PhotoImage(horseimage), ImageTk.PhotoImage(horseimage), ImageTk.PhotoImage(horseimage), ImageTk.PhotoImage(horseimage), ImageTk.PhotoImage(horseimage)]
			soldierimage = Image.open('soldier.png')
			soldierphoto = [ImageTk.PhotoImage(soldierimage), ImageTk.PhotoImage(soldierimage), ImageTk.PhotoImage(soldierimage), ImageTk.PhotoImage(soldierimage), ImageTk.PhotoImage(soldierimage)]
			for i in range(0, len(self.my_cards)):
				if self.my_cards[i] == 'cannon':
					w.w.create_image(card_coords[i], image = cannonphoto[i], tag = 'card' + str(i))
					w.cards[i] = cannonphoto
				if self.my_cards[i] == 'horse':
					w.w.create_image(card_coords[i], image = horsephoto[i], tag = 'card' + str(i))
					w.cards[i] = horsephoto
				if self.my_cards[i] == 'soldier':
					w.w.create_image(card_coords[i], image = soldierphoto[i], tag = 'card' + str(i))
					w.cards[i] = soldierphoto
			swap = False
		if swap == False:
			cardimage = Image.open('card.png')
			cardphoto = [ImageTk.PhotoImage(cardimage), ImageTk.PhotoImage(cardimage), ImageTk.PhotoImage(cardimage), ImageTk.PhotoImage(cardimage), ImageTk.PhotoImage(cardimage)]
			for i in range(0, len(self.my_cards)):
				w.w.create_image(card_coords[i], image = cardphoto[i], tag = 'card' + str(i))
				w.cards[i] = cardphoto
				swap = True

	def play_cards(self): # currently unused
		print "Please choose 3 cards to play. Remember they must be either 3 of a kind or 3 different cards. \n The choices are 'cannon', 'horse', and 'soldier'."
		cards = [['cannon'], ['horse'], ['soldier']]
		cancel = False
		while cancel == False:
			c1 = raw_input('Please type in your first card:' )
			c2 = raw_input('Please type in your second card:' )
			c3 = raw_input('Please type in your third card:' )
			if c1 == 'cancel' or c2 == 'cancel' or c3 == 'cancel':
				cancel = True
			my_cards = self.my_cards
			i = 0
			while i < len(my_cards):
				if my_cards[i] == c1:
					del my_cards[i]
					c1 = 0
				elif my_cards[i] == c2:
					del my_cards[i]
					c2 = 0
				elif my_cards[i] == c3:
					del my_cards[i]
					c3 = 0
				else:
					i += 1
			if len(my_cards) == 2 and c1 == c2 and c2 == c3:
				print self.name, "plays three", str(c1), "and gets to place 8 more armies."
				return 8
			elif len(my_cards) == 2 and c1 != c2 and c2 != c3 and c3 != c1:
				print self.name, "plays one soldier, one horse and one cannon. They get to place 10 more armies."
				return 10
		
	def check_continents(self):
		NA_control = 0
		SA_control = 0
		EU_control = 0
		AF_control = 0
		AS_control = 0
		AU_control = 0
		my_territories_list = []
		for i in self.my_territories:
				if i.continent == 'North America':
					NA_control += 1
				if i.continent == 'South America':
					SA_control += 1
				if i.continent == 'Europe':
					EU_control += 1
				if i.continent == 'Africa':
					AF_control += 1
				if i.continent == 'Asia':
					AS_control += 1
				if i.continent == 'Australia':
					AU_control += 1
		additional_troops = 0
		if NA_control == 9:
			additional_troops += 5
		if EU_control == 7:
			additional_troops += 5
		if SA_control == 4:
			additional_troops += 2
		if AU_control == 4:
			additional_troops += 2
		if AF_control == 6:
			additional_troops += 3
		if AS_control == 12:
			additional_troops += 7
		return additional_troops

	def place_armies(self, x, y): # function for placing armies on territories
		for i in t_list:
			if i.owner == self.name:
				coords = w.w.coords(i.tag)
				if x >= coords[0]  and x <= coords[2] and y >= coords[1] and y <= coords[3]:
					i.armies += 1
					self.armies += 1
					i.update_armies()
					if w.w.coords('turn_arrow') == [820, 225]:
						w.updateNameArrow()
					armies_to_place[self.turn - 1] -= 1
					if armies_to_place == [0, 0, 0, 0, 0, 0]:
						if w.w.coords('turn_arrow') == [820, 225]:
							pool[0].deploy_troops()
						w.updateTurnArrow()

					
	def deploy_troops(self):
		global swap
		swap = True
		base_troops = 3
		country_control = len(self.my_territories)
		troops = max(base_troops, country_control/3) + self.check_continents()
		'''if len(self.my_cards) == 5:
			w.system_message("Since you now have 5 cards, you must turn them in for additional armies.")
		w.system_message('Click on a set of 3 cards if you would like to play your cards')'''

		'''	troops += self.play_cards()
		if len(self.my_cards) == 3 or len(self.my_cards) == 4:
			answer = raw_input('Do you want to play cards for extra armies? (yes/no) ')
			if answer == 'yes':
				troops += self.play_cards()'''

		# create dem cards
		cardimage = Image.open('card.png')
		cardphoto = [ImageTk.PhotoImage(cardimage), ImageTk.PhotoImage(cardimage), ImageTk.PhotoImage(cardimage), ImageTk.PhotoImage(cardimage), ImageTk.PhotoImage(cardimage)]
		card_coords = [(642,646), (722,646), (801,646), (880,646), (959,646)]
		how_many = [0, 0, 0, 0, 0, 0] # how many cards each player has
		for i in range(0, players):
			how_many[i] = len(pool[i].my_cards)
		if w.w.coords('name_arrow') == [820, 42]:
			for i in range(0, how_many[0]):
				w.w.create_image(card_coords[i], image = cardphoto[i], tag = 'card' + str(i))
				w.cards[i] = cardphoto[i]
		elif w.w.coords('name_arrow') == [820, 67]:
			for i in range(0, how_many[1]):
				w.w.create_image(card_coords[i], image = cardphoto[i], tag = 'card' + str(i))
				w.cards[i] = cardphoto[i]
		elif w.w.coords('name_arrow') == [820, 92]:
			for i in range(0, how_many[2]):
				w.w.create_image(card_coords[i], image = cardphoto[i], tag = 'card' + str(i))
				w.cards[i] = cardphoto[i]
		elif w.w.coords('name_arrow') == [820, 117]:
			for i in range(0, how_many[3]):
				w.w.create_image(card_coords[i], image = cardphoto[i], tag = 'card' + str(i))
				w.cards[i] = cardphoto[i]
		elif w.w.coords('name_arrow') == [820, 142]:
			for i in range(0, how_many[4]):
				w.w.create_image(card_coords[i], image = cardphoto[i], tag = 'card' + str(i))
				w.cards[i] = cardphoto[i]
		elif w.w.coords('name_arrow') == [820, 167]:
			for i in range(0, how_many[5]):
				w.w.create_image(card_coords[i], image = cardphoto[i], tag = 'card' + str(i))
				w.cards[i] = cardphoto[i]
		
		armies_to_place[self.turn -1] += troops
		global attack
		attack = False
		global defend
		defend = False
		global is_true
		is_true = False
		global rp1
		rp1 = False
		global rp2
		rp2 = False
		global territory_num_start
		territory_num_start = len(self.my_territories)
		global is_true2
		is_true2 = False
		global is_true3
		is_true3 = False

	def reinforce(self, x, y):
		global rp1
		global rp2
		global is_true2
		if is_true2 == False and rp2 == False:
			global end_retreat
			end_retreat = Button(w.parent, text = 'End Retreat', command = self.endretreat2)
			end_retreat.place(x = 850, y = 350)
			is_true2 = True
		if rp1 == False or rp1 == True:
			for i in t_list:
				if i.owner == self.name:
					coords = w.w.coords(i.tag)
					if x >= coords[0]  and x <= coords[2] and y >= coords[1] and y <= coords[3]:
						border_list = self.my_territories
						do_own = 0
						for j in border_list:
							if i.id in j.borders:
								do_own += 1
						if do_own == 0:
							w.system_message("You don't own any adjacent territories.")
						elif i.armies <= 1:
							w.system_message("You don't have enough armies here to move from this territory.")
						else:
							rp1 = True # rp1 = retreat part 1
							global retreat_from
							retreat_from = i
							return
		if rp1 == True and rp2 == False:
			for i in t_list:
				if i.owner == self.name:
					coords = w.w.coords(i.tag)
					if x >= coords[0]  and x <= coords[2] and y >= coords[1] and y <= coords[3]:
						if i.id in retreat_from.borders:
							global retreat_to
							retreat_to = i
							global rsb #retreat spin box
							global rb #retreat button
							global rbc # retreat button cancel
							new_list = range(0,retreat_from.armies)
							new_list = tuple(new_list[::-1])
							rsb = Spinbox(w.parent, values = new_list, width = 10)
							rsb.place(x = 850, y = 350)
							rb = Button(w.parent, text = 'retreat', command = self.retreat)
							rbc = Button(w.parent, text = 'cancel', command = self.endretreat)
							rb.place(x = 850, y = 375)
							rbc.place(x = 850, y = 400)

	def retreat(self):
		n_troops = int(rsb.get())
		retreat_from.armies -= n_troops
		retreat_to.armies += n_troops
		retreat_from.update_armies()
		retreat_to.update_armies()
		self.endretreat()

	def endretreat(self):
		global rp1
		global rp2
		global retreat_from
		global retreat_to
		rp1 = False
		rp2 = False
		retreat_to = None
		retreat_from = None
		end_retreat.destroy()
		rb.destroy()
		rsb.destroy()
		rbc.destroy()
		w.updateTurnArrow()
		self.end_turn()

	def endretreat2(self):
		global rp1
		global rp2
		global retreat_from
		global retreat_to
		global is_true2
		is_true2 = False
		rp1 = False
		rp2 = False
		retreat_to = None
		retreat_from = None
		end_retreat.destroy()
		w.updateTurnArrow()
		self.end_turn()


	def end_attack(self):
		w.updateTurnArrow()
		global end_attack
		end_attack.destroy()
		
	def battle(self, x, y):
		global attack
		global defend
		global a_territory
		global d_territory
		global is_true
		if defend == False and is_true == False:
			global end_attack
			end_attack = Button(w.parent, text = 'Stop Attacking', command = self.end_attack)
			end_attack.place(x = 850, y = 350)
			is_true = True
		if attack == False or attack == True:
			for i in t_list:
				if i.owner == self.name:
					coords = w.w.coords(i.tag)
					if x >= coords[0]  and x <= coords[2] and y >= coords[1] and y <= coords[3]:
						border_list = i.borders
						dont_own = 0
						for j in border_list:
							if t_list[j-1].owner != self.name:
								dont_own += 1
						if dont_own == 0:
							w.system_message("There are no nearby enemy territories to attack from here.")
						elif i.armies <= 1:
							w.system_message("You don't have enough armies here to attack from this territory.")
						else:
							attack = True
							global a_territory
							a_territory = i
							return
		if attack == True and defend == False:
			for i in t_list:
				if i.id in a_territory.borders and i.owner != self.name:
					coords = w.w.coords(i.tag)
					if x >= coords[0]  and x <= coords[2] and y >= coords[1] and y <= coords[3]:
						global d_territory
						d_territory = i
						defend = True
		global is_true3
		if attack == True and defend == True and is_true3 == False:
			end_attack.destroy()
			if a_territory.armies <= 1:
				w.system_message("You no longer have enough troops to attack from this territory.")
				w.system_message("This invasion is at an end.")
				return
			global a_spinbox
			global cb
			global ab
			spin_list = range(1, a_territory.armies)
			spin_list = tuple(spin_list[::-1])
			a_spinbox = Spinbox(w.parent, values = spin_list, width = 10)
			a_spinbox.place(x = 850, y = 350)
			cb = Button(w.parent, text = 'Cancel', command = self.cb_callback)
			cb.place(x = 900, y = 380)
			ab = Button(w.parent, text = 'Enter', command = self.ab_callback)
			ab.place(x = 830, y = 380)
			is_true3 = True
					
	def cb_callback(self):
		global d_territory
		global a_territory
		global attack
		global defend
		global is_true
		global is_true3
		attack = False
		defend = False
		a_territory = None
		d_territory = None
		a_spinbox.destroy()
		cb.destroy()
		ab.destroy()
		is_true = False
		is_true3 = False

	def ab_callback(self):
		global a_territory
		global d_territory
		attackers = int(a_spinbox.get())
		if attackers > 3:
			attackers = 3
		if attackers < 1:
			w.system_message('You do not have enough troops to attack from this territory.')
			return

		if d_territory.armies > 1:
			defenders = 2
		else:
			defenders = 1

		a_roll = [0] * attackers
		d_roll = [0] * defenders
		for i in range(attackers):
			a_roll[i] = random.randint(1, 6)
		for i in range(defenders):
			d_roll[i] = random.randint(1, 6)
		rollsort(a_roll)
		rollsort(d_roll)
		w.system_message(str(a_territory.owner) + " rolled " + str(a_roll))
		w.system_message(str(d_territory.owner) + " rolled " + str(d_roll))

		deaths = [0] * 2 # with deaths[0] == number of attackers killed, deaths[1] == number of defenders killed
		if a_roll[0] > d_roll[0]:
			deaths[1] += 1
		if a_roll[0] <= d_roll[0]:
			deaths[0] += 1
		if defenders == 2 and attackers >= 2:
			if a_roll[1] > d_roll[1]:
				deaths[1] += 1
			if a_roll[1] <= d_roll[1]:
				deaths[0] += 1

		if deaths[0] > 0:
			w.system_message(str(a_territory.owner) + " loses " + str(deaths[0]) + " armies.")
			a_territory.armies -= deaths[0]
			a_territory.update_armies()

		if deaths[1] > 0:
			w.system_message(str(d_territory.owner) + " loses " + str(deaths[1]) + " armies.")
			d_territory.armies -= deaths[1]
			d_territory.update_armies()

		if d_territory.armies == 0: # moves ownership if defending territory loses all armies
			attacking = False
			w.system_message(str(a_territory.owner) + " has won and claims " + str(d_territory.name) + ".")
			for i in pool:
				if i.name == d_territory.owner:
					losing_player = i
			d_territory.owner = a_territory.owner
			self.my_territories += [d_territory]
			d_territory.color = a_territory.color
			d_territory.update_color()


			# Removes conquered territory from owners list
			j = 0
			while j < len(losing_player.my_territories):
				if losing_player.my_territories[j].name == d_territory.name:
					del losing_player.my_territories[j]
				else:
					j += 1

			# Check to see if player has no remaining territories and remove them if so
			if len(losing_player.my_territories) == 0:
				w.system_message(str(losing_player.name) + " has been defeated.")
				i = 0
				while i < pool:
					if pool[i].name == losing_player.name:
						del i
					else:
						i +=1
				win_conditions()
			# Moving troops into newly conquered territory
			ab.config(text = 'Move', command = self.move_into_new_territory)
			cb.destroy()
		else:
			global a
			global b
			if a_territory.armies > 2:
				new_list = range(1, a_territory.armies)
				new_list = new_list[::-1]
			elif a_territory.armies == 2:
				new_list = [1]
			else:
				new_list = []
				w.system_message('You do not have sufficient armies to continue your attack.')
				self.passive_aggression()
			a_spinbox.config(values = new_list)
			ab.config(text = 'Again', command = self.ab_callback)
			cb.config(text = 'Stop', command = lambda: self.passive_aggression(False))


	def move_into_new_territory(self):
		invasion = int(a_spinbox.get())
		d_territory.armies = invasion
		a_territory.armies -= invasion
		d_territory.update_armies()
		a_territory.update_armies()
		self.passive_aggression()

	def passive_aggression(self, cb_destroyed = True):
		global d_territory
		global a_territory
		global attack
		global defend
		global is_true
		global is_true3
		attack = False
		defend = False
		a_territory = None
		d_territory = None
		a_spinbox.destroy()
		ab.destroy()
		if cb_destroyed == False:
			cb.destroy()
		is_true = False
		is_true3 = False


	def end_turn(self):
		w.system_message("This concludes " + str(self.name) + "'s turn. Please notify the next player.")
		global territory_num_start
		territory_num_end = len(self.my_territories)
		if territory_num_end > territory_num_start and len(self.my_cards) < 5:
			cards = [['cannon'], ['horse'], ['soldier']]
			self.my_cards += cards[random.randint(0, 2)] # a random card
		# get a card if you took a territory
		w.updateNameArrow()
		w.updateTurnArrow()
		if w.w.coords('name_arrow') == [820, 42]:
			pool[0].deploy_troops()
		elif w.w.coords('name_arrow') == [820, 67]:
			pool[1].deploy_troops()
		elif w.w.coords('name_arrow') == [820, 92]:
			pool[2].deploy_troops()
		elif w.w.coords('name_arrow') == [820, 117]:
			pool[3].deploy_troops()
		elif w.w.coords('name_arrow') == [820, 142]:
			pool[4].deploy_troops()
		elif w.w.coords('name_arrow') == [820, 167]:
			pool[5].deploy_troops()





# assign player names
def create_player_instances():
	global colors
	colors = ['snow', 'red', 'forest green', 'yellow', 'orange', 'blue']
	global pool
	pool = []
	for i in range(0, players):
		pool += [Player("turn", names[i], 1)] # pool becomes a list of the instances of the Player class


def turn_order():
	global pool
	order = random.sample(range(0, players), players)
	aux = [0] * players
	for i in range(0, players):
		aux[i] = pool[order[i]]
		pool[order[i]].turn = i + 1 # sets turns in the player class
		pool[order[i]].color = colors[i]
	pool = aux # makes the pool in order of turn (so that when it tells them what countries they own its in order)

def create_territories():
	# NA_territories
	alaska = Territory('Alaska', 'North America', 1, 'random owner', 1, [2, 6, 32], w.w, (61, 87))
	alberta = Territory('Alberta', 'North America', 2, 'random owner', 1, [1, 6, 7, 9], w.w, (132, 87))
	central_america = Territory('Central America', 'North America', 3, 'random owner', 1, [4, 9, 13], w.w, (141, 268))
	eastern_united_states = Territory('Eastern United States', 'North America', 4, 'random owner', 1, [3, 7, 8, 9], w.w, (188, 206))
	greenland = Territory('Greenland', 'North America', 5, 'random owner', 1, [6, 7, 8, 15], w.w, (278, 59))
	northwest_territory = Territory('Northwest Territory', 'North America', 6, 'random owner', 1, [1, 2, 5, 7], w.w, (124, 128))
	ontario = Territory('Ontario', 'North America', 7, 'random owner', 1, [2, 4, 5, 6, 8, 9], w.w, (180, 140))
	quebec = Territory('Quebec', 'North America', 8, 'random owner', 1, [4, 5, 7], w.w, (231, 139))
	western_united_states = Territory('Western United States', 'North America', 9, 'random owner', 1, [2, 3, 4, 6, 7], w.w, (128, 190))

	# SA_territories
	argentina = Territory('Argentina', 'South America', 10, 'random owner', 1, [11, 12], w.w, (206, 436))
	brazil = Territory('Brazil', 'South America', 11, 'random owner', 1, [10, 12, 13, 25], w.w, (247, 354))
	peru = Territory('Peru', 'South America', 12, 'random owner', 1, [10, 11, 13], w.w, (192, 370))
	venezuela = Territory('Venezuela', 'South America', 13, 'random owner', 1, [3, 11, 12], w.w, (188, 303))

	# EU_territories
	great_britain = Territory('Great Britain', 'Europe', 14, 'random owner', 1, [15, 16, 17, 20], w.w, (329, 181))
	iceland = Territory('Iceland', 'Europe', 15, 'random owner', 1, [5, 14, 17], w.w, (345, 121))
	northern_europe = Territory('Northern Europe', 'Europe', 16, 'random owner', 1, [14, 17, 18, 19, 20], w.w, (401, 183))
	scandinavia = Territory('Scandinavia', 'Europe', 17, 'random owner', 1, [14, 15, 16, 19], w.w, (403, 108))
	southern_europe = Territory('Southern Europe', 'Europe', 18, 'random owner', 1, [16, 19, 20, 23, 25, 33], w.w, (409, 238))
	ukraine = Territory('Ukraine', 'Europe', 19, 'random owner', 1, [16, 17, 18, 27, 33, 37], w.w, (477, 151))
	western_europe = Territory('Western Europe', 'Europe', 20, 'random owner', 1, [14, 16, 18, 25], w.w, (338, 258))

	# AF territories
	congo = Territory('Congo', 'Africa', 21, 'random owner', 1, [22, 25, 26], w.w, (432, 400))
	east_africa = Territory('East Africa', 'Africa', 22, 'random owner', 1, [21, 23, 24, 25, 26, 33], w.w, (460, 366))
	egypt = Territory('Egypt', 'Africa', 23, 'random owner', 1, [18, 22, 25, 33], w.w, (431, 310))
	madagascar = Territory('Madagascar', 'Africa', 24, 'random owner', 1, [22, 26], w.w, (505, 467))
	north_africa = Territory('North Africa', 'Africa', 25, 'random owner', 1, [11, 18, 20, 21, 22, 23], w.w, (368, 337))
	south_africa = Territory('South Africa', 'Africa', 26, 'random owner', 1, [21, 22, 24], w.w, (439, 475))

	# AS_territories
	afghanistan = Territory('Afghanistan', 'Asia', 27, 'random owner', 1, [19, 28, 29, 33, 37], w.w, (537, 214))
	china = Territory('China', 'Asia', 28, 'random owner', 1, [27, 29, 34, 35, 36, 37], w.w, (628, 246))
	india = Territory('India', 'Asia', 29, 'random owner', 1, [27, 28, 33, 35], w.w, (582, 287))
	irkutsk = Territory('Irkutsk', 'Asia', 30, 'random owner', 1, [32, 34, 36, 38], w.w, (638, 145))
	japan = Territory('Japan', 'Asia', 31, 'random owner', 1, [32, 34], w.w, (729, 201))
	kamchatka = Territory('Kamchatka', 'Asia', 32, 'random owner', 1, [1, 30, 31, 34, 38], w.w, (709, 83))
	middle_east = Territory('Middle East', 'Asia', 33, 'random owner', 1, [18, 19, 22, 23, 27, 29], w.w, (493, 295))
	mongolia = Territory('Mongolia', 'Asia', 34, 'random owner', 1, [28, 30, 31, 32, 36], w.w, (649, 194))
	siam = Territory('Siam', 'Asia', 35, 'random owner', 1, [28, 29, 40], w.w, (646, 314))
	siberia = Territory('Siberia', 'Asia', 36, 'random owner', 1, [28, 30, 34, 37, 38], w.w, (591, 100))
	ural = Territory('Ural', 'Asia', 37, 'random owner', 1, [19, 27, 28, 36], w.w, (549, 139))
	yakutsk = Territory('Yakutsk', 'Asia', 38, 'random owner', 1, [30, 32, 36], w.w, (648, 77))

	# AU_territories
	eastern_australia = Territory('Eastern Australia', 'Australia', 39, 'random owner', 1, [41, 42], w.w, (755, 464))
	indonesia = Territory('Indonesia', 'Australia', 40, 'random owner', 1, [35, 41, 42], w.w, (658, 394))
	new_guinea = Territory('New Guinea', 'Australia', 41, 'random owner', 1, [39, 40, 42], w.w, (723, 373))
	western_australia = Territory('Western Australia', 'Australia', 42, 'random owner', 1, [39, 40, 41], w.w, (687, 468))

	# create list of the instances of the territory class
	global t_list
	t_list = [alaska, alberta, central_america, eastern_united_states, greenland, northwest_territory, ontario, quebec, western_united_states, argentina, brazil, peru, venezuela, great_britain, iceland, northern_europe, scandinavia, southern_europe, ukraine, western_europe, congo, east_africa, egypt, madagascar, north_africa, south_africa, afghanistan, china, india, irkutsk, japan, kamchatka, middle_east, mongolia, siam, siberia, ural, yakutsk, eastern_australia, indonesia, new_guinea, western_australia]

def assign_ownership():
	w.system_message("Territories will be distributed randomly.")
	p_list = []
	for i in range(0, players):
		p_list += ([pool[i].name] * (42/players)) # makes a list of players names with copies of each name depending on how many territories they'll be given
	if players == 4 or players == 5: # if the territories don't divide evenly...
		p_list += pool[players - 2].name # give the people who go last the extra territories
		p_list += pool[players - 1].name
	random.shuffle(p_list)
	for i in range(0, 42):
		t_list[i].owner = p_list[i] # assigns territories
		t_list[i].update_color()
		for j in range(0, players):
			if p_list[i] == pool[j].name:
				pool[j].my_territories += [t_list[i]]

def distribute_and_assign_armies():
	global armies_to_place
	if players == 2:
		w.system_message("Each player will receive 19 additional armies to place.")
		armies_to_place = [3, 3, 0, 0, 0, 0] #19 not 3
	if players == 3:
		w.system_message("Each player will receive 21 additional armies to place.")
		armies_to_place = [21, 21, 21, 0, 0, 0]
	if players == 4:
		w.system_message("Each player will receive 19 or 20 additional armies to place (depeding on turn order).")
		armies_to_place = [20, 20, 19, 19, 0, 0]
	if players == 5:
		w.system_message("Each player will receive 16 or 17 additional armies to place (depeding on turn order).")
		armies_to_place = [17, 17, 17, 16, 16, 0]
	if players == 6:
		w.system_message("Each player will receive 13 additional armies to place.")
		armies_to_place = [13, 13, 13, 13, 13, 13]

def rollsort(rolls): # reorders rolls in order of highest to lowest roll
	if len(rolls) == 1:
		return rolls
	if len(rolls) == 2:
		if rolls[0] >= rolls[1]:
			return rolls
		else:
			aux = rolls[0]
			rolls[0] = rolls[1]
			rolls[1] = aux
			return rolls
	else:
		proper = False
		while proper == False:
			for i in range(2):
				proper = True
				if rolls[i] < rolls[i + 1]:
					swap = rolls[i]
					rolls[i] = rolls[i + 1]
					rolls[i + 1] = swap
					proper = False
		return rolls

def win_conditions():
	if len(pool) == 1:
		w.system_message("Game Over. " + str(pool[0].name) + " has won!")

if __name__ == '__main__':
	root = Tk()
	w = MainScreen(root)
	root.mainloop()
	sys.exit()