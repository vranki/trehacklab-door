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

from doorbackend import DoorBackend

class DoorBackendMySQL(DoorBackend):
	def __init__(self):
		DoorBackend.__init__(self)

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

		if database_query_result:
			DoorBackend.validationSuccess(self, database_query_result)
			return database_query_result
		else:
			DoorBackend.validationFailed(self)
			return None

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

	server = DoorBackendMySQL()
	server.runServer()

