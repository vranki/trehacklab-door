trehacklab-door
===============

Access control software for Tampere Hacklab. Possibly more generic in future.

Used hardware:

* Raspberry Pi
* PiFace board
* Touchscreen monitor (VGA / Serial)


Software
========

Software is split into several python processes which can be easily replaced
with another implementation. These are the current ones:

* doordaemon - Controls the actual door relay using piface. Listens to zerorpc messages.
* local-backend - Backend for checking authentication. Uses local text file database.
* mysql-backend - Backend for checking authentication. Uses a MySQL database connection.
* doorui-gtk - A GUI written in GTK for authentication.

See source code for details.

Installing
==========

apt-get install python-pip python-dev python-virtualenv python-dev libmysqlclient-dev

pip install -r requirements.txt

You could use virtualenv, but getting Gtk to work with it is pain.
For more info on virtualenv, see http://docs.python-guide.org/en/latest/dev/virtualenvs/

Running
=======

For MySQL connection, edit /home/cosmo/.netrc and write:

machine keycode-mysql login <user> account <database> password <password>

Then run any of the apps. Start (in order): doordaemon, backend and gui for a working setup.

