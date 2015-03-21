#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#
# Copyright 2014 Paavo Hartikainen <pahartik@iki.fi>
#
# Lisensoitu EUPL-lisenssillä, versio 1.1, tai – heti kun Euroopan 
# komissio on hyväksynyt ne – EUPL-lisenssin seuraavilla versioilla 
# (jäljempänä ”lisenssi”). Tätä teosta saa käyttää vain lisenssin 
# mukaisesti. Lisenssijäljennös on saatavissa osoitteesta:
#
# http://ec.europa.eu/idabc/eupl
#
# Ellei sovellettava laki muuta edellytä tai ellei toisin ole 
# kirjallisesti sovittu, lisenssin nojalla levitettävä ohjelmisto 
# levitetään ”sellaisena kuin se on”, ILMAN MINKÄÄNLAISIA TAKUITA TAI 
# EHTOJA, sen enempää nimenomaisia kuin konkludenttisia. Katso lisenssin 
# mukaisia lupia ja rajoituksia koskevat erityismääräykset lisenssistä.
#

from gi.repository import Gtk
from gi.repository import GObject
import random
import time
import socket
import zmq
import zerorpc

key_characters_allowed = "0123456789abcdef"
key_characters = []
for character in range(len(key_characters_allowed)):
	key_characters.append(key_characters_allowed[character])

DEBUG=0

main_window_size = {'x': 800, 'y': 600}
key_character_pad_size = {'x': 400, 'y': 400}
control_button_pad_size = {'x': 400, 'y': 100}

class MyWindow(Gtk.Window):
	backend = zerorpc.Client()
	backend._events.setsockopt(zmq.IPV4ONLY, 0)
	backend.connect("tcp://[::1]:4142")

	def __init__(self):
		Gtk.Window.__init__(self, title="Hexadecimal Code Lock")
		self.connect("delete-event", Gtk.main_quit)
		self.key_label_markup = '<span size="32000">%s</span>'
		self.set_default_size(main_window_size['x'], main_window_size['y'])
		self.set_decorated(False)
		self.keycode_input = ""
		#self.fullscreen()

		self.timestamp_format = "%Y-%m-%d %H:%M"

		self.key_buttons = []
		self.key_labels = []
		for key_character in key_characters:
			button = Gtk.Button()
			label = Gtk.Label()
			button.add(label)
			button.connect("clicked", self.on_button_clicked)
			self.key_buttons.append(button)
			self.key_labels.append(label)
		self.key_character_pad = Gtk.Table(4, 4, True)
		self.key_character_pad.set_size_request(key_character_pad_size['x'], key_character_pad_size['y'])
		for row in [0, 1, 2, 3]:
			for column in [0, 1, 2, 3]:
				button = self.key_buttons[row + (column * 4)]
				self.key_character_pad.attach(button, row, row+1, column, column+1)

		renderer_text = Gtk.CellRendererText()
		self.messages = Gtk.ListStore(str, str)
		self.messages_view = Gtk.TreeView(self.messages)
		self.messages_view.set_headers_visible(False)
		column = Gtk.TreeViewColumn(False, renderer_text, text=0)
		self.messages_view.append_column(column)
		column = Gtk.TreeViewColumn(False, renderer_text, text=1)
		self.messages_view.append_column(column)
		self.messages_view.set_fixed_height_mode(True)
		messages_view_scrolled = Gtk.ScrolledWindow()
		messages_view_scrolled.set_size_request(400, 100)
		messages_view_scrolled.add_with_viewport(self.messages_view)

		self.control_button_pad = Gtk.Table(1, 4, True)
		self.control_button_pad.set_size_request(control_button_pad_size['x'], control_button_pad_size['y'])
		self.counter_button = Gtk.Button(label="()")
		self.counter_button.set_sensitive(False)
		self.counter_button.connect("clicked", self.on_button_clicked)
		self.control_button_pad.attach(self.counter_button, 0, 1, 0, 1)
		clear_button = Gtk.Button(label="Clear")
		clear_button.connect("clicked", self.on_button_clicked)
		self.control_button_pad.attach(clear_button, 2, 3, 0, 1)
		enter_button = Gtk.Button(label="Enter")
		enter_button.connect("clicked", self.on_button_clicked)
		self.control_button_pad.attach(enter_button, 3, 4, 0, 1)
		self.control_button_pad.show()

		self.action_button_pad = Gtk.Table(1, 4, True)
		self.action_button_pad.set_size_request(400, 100)
		exit_button = Gtk.Button(label="Exit")
		exit_button.connect("clicked", self.on_button_clicked)
		self.action_button_pad.attach(exit_button, 2, 3, 0, 1)
		activate_button = Gtk.Button(label="Activate")
		activate_button.connect("clicked", self.on_button_clicked)
		activate_button.hide()
		self.action_button_pad.attach(activate_button, 3, 4, 0, 1)
		self.action_button_pad.set_no_show_all(True)

		self.grid = Gtk.Grid()
		self.grid.set_size_request(400, 600)
		self.grid.attach(messages_view_scrolled, 0, 1, 1, 1)
		self.grid.attach(self.key_character_pad, 0, 2, 1, 1)
		self.grid.attach(self.control_button_pad, 0, 3, 1, 1)
		self.grid.attach(self.action_button_pad, 0, 4, 1, 1)
		self.add(self.grid)

		self.log_activity("User interface started")

	def shuffle_buttons(self):
		random.shuffle(key_characters)
		for index in range(len(key_characters)):
			self.key_labels[index].set_markup(self.key_label_markup % (key_characters[index]))

	def counter_button_update(self):
		self.counter_button.set_label("(%s)" % (len(self.keycode_input)))

	def on_button_clicked(self, widget):
		self.activity_timestamp = time.time()
		if len(widget.get_child().get_text()) == 1:
			self.key_character_pad.set_sensitive(False)
			self.keycode_input = self.keycode_input + widget.get_child().get_text()
			self.log_activity(widget.get_child().get_text(), debug=1)
			self.shuffle_buttons()
			self.key_character_pad.set_sensitive(True)
			self.counter_button_update()
		elif widget.get_child().get_text() == "Exit":
			self.action_button_pad.set_no_show_all(True)
			self.control_button_pad.set_no_show_all(False)
		elif widget.get_child().get_text() == "Enter":
			if self.backend.validate(self.keycode_input):
				self.enable_door_control(self.keycode_input)
		elif widget.get_child().get_text() == "Clear":
			self.keycode_input = ""
			self.counter_button_update()
			#Gtk.main_quit()

	def enable_door_control(self, keycode):
		self.control_button_pad.set_no_show_all(True)
		self.action_button_pad.set_no_show_all(False)
		self.log_activity(keycode, debug=1)
		#self.log_activity(response[1])
		#if response == True:
		#	self.enable_door_control(response[1])
		#elif response == False:
		#
		#	self.log_activity("Authentication failure")
		#pass

	def toggle_door_state(self, authenticated_user):
		pass

	def server_request(self, request_type, request_data):

		backend.validate()

		s = None
		for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
			af, socktype, proto, canonname, sa = res
			try:
				s = socket.socket(af, socktype, proto)
				s.settimeout(4)
			except socket.error as msg:
				self.log_activity(str(msg))
				s = None
				continue
			try:
				s.connect(sa)
			except socket.error as msg:
				self.log_activity(str(msg))
				s.close()
				s = None
				continue
			break
		if s is not None:
			try:
				s.sendall("%s: %s\n" % (request_type, request_data))
				response = ("OK", s.recv(1024))
			except socket.timeout:
				response = ("ERROR", "Socket timeout")
			s.close()
			return(response)
		else:
			self.log_activity("Socket failed")

	def log_activity(self, message, debug=0):
		if debug <= DEBUG:
			print("%s %s" % (time.strftime(self.timestamp_format), message))
		if debug == 0:
			self.messages.append([time.strftime(self.timestamp_format), message])

	def periodic_poll(self):
		self.log_activity("periodic poll", debug=1)
		return True

win = MyWindow()
win.shuffle_buttons()
win.show_all()
GObject.timeout_add(1000, win.periodic_poll)
GObject.threads_init()
Gtk.main()
