#!/usr/bin/env python2
# -*- encoding: utf-8 -*-

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

# speksi: bool avataankoOvi(koodi)

# Ovikooditietokanta täytyy olla sijainnissa ::1 3306, "SSH 
# LocalForward" käyttöön jos tietokanta ei ole paikallisessa 
# järjestelmässä.

# Käyttäjä, tietokanta ja salasana luetaan tiedostosta "~/.netrc": 
# "machine keycode-mysql login <user> account <database> password 
# <password>"

import sys
import os
import zerorpc
import zmq
import MySQLdb
import netrc

class DoorControlRPC(object):
	def __init__(self):
		self.door = zerorpc.Client()
		#self.door._events.setsockopt(zmq.IPV6, 1)
		self.door._events.setsockopt(zmq.IPV4ONLY, 0)
		self.door.connect("tcp://[::1]:4143")

	def toggle_door_state(self, key):
		if self.validate(key):
			self.door.open()
			print("Keycode '%s' accepted" % (key))
			return True
		else:
			print("Keycode '%s' rejected" % (key))
		    	return False

	def validate(self, key):
		sql = MySQLdb.connect(
			user=local_config.authenticators(databasehost)[0],
			db=local_config.authenticators(databasehost)[1],
			passwd=local_config.authenticators(databasehost)[2],
			host="::1",
			port=3306
		)

		sql_cursor = sql.cursor()
		key = key.lower()
		sql_cursor.execute('''SELECT username FROM doorUsers WHERE doorUsers.key=%s''', key)
		database_query_result = sql_cursor.fetchone()
		sql.close()

		if not database_query_result:
			print("No match in database")
			return False
		else:
			print("User: %s" % (database_query_result))
			return True

if __name__ == '__main__':
	try:
		local_config = netrc.netrc()
	except IOError, message:
		print(message)
		exit(2)
	databasehost = "keycode-mysql"

	try:
	        local_config.hosts[databasehost]
	except KeyError:
	        print("database credentials for '%s' missing" % (databasehost))
	        exit(2)

	srv = zerorpc.Server(DoorControlRPC())
	#srv._events.setsockopt(zmq.IPV6, 1)
	srv._events.setsockopt(zmq.IPV4ONLY, 0)
	srv.bind("tcp://[::1]:4142")
	srv.run()

