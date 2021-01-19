![MaIDS Logo](res/logo_colored.svg)
# MaIDS - Mamede Industrial Data System <!-- omit in toc -->

# Table of contents <!-- omit in toc -->

- [1. Introduction](#1-introduction)
  - [1.1. Machines](#11-machines)
  - [1.2. Backup Control](#12-backup-control)
  - [1.3. Password manager](#13-password-manager)
- [2. The API](#2-the-api)
  - [2.1. Authentication](#21-authentication)
- [3. Roadmap](#3-roadmap)
- [4. How to run](#4-how-to-run)
  - [4.1. Dotenv](#41-dotenv)
  - [4.2. App](#42-app)
- [5 Todo](#5-todo)

# 1. Introduction

This project was created for my TCE (internship conclusion project), this is an API providing data about machines, a backup control, and a password manager. A mobile app will be used to view these info and update the database. And a QR Code will be placed on an exposed and easy to find part of the machine which the user will be able to scan and have the data they need.

## 1.1. Machines

People who are working on a machine often don't know what to expect until they open it, technicians will have to juggle back and forth between doing research on the PC and working on the machine. The idea here is to have easy to get info at your disposal.

## 1.2. ~Backup Control~

Update: Right, so this has much more requirements than I thought it would have, I think I'm going to scrape this idea, for now, I'm jumping to the password management system

One of the necessities of the automation area is guaranteeing that we always have up to date machine backups, for that we need a system that handles the backup routine. The technician will execute the job and then confirm it was done, the system will handle the rest.

## 1.3. Password manager

Another necessity of automation is managing user passwords of every applicable machine, these passwords should be changed regularly and a central database would be very useful. These passwords can also be shown for the user through reading the QR Code

# 2. The API

The API is a restful flask python app, using the SQLAlchemy ORM.

## 2.1. Authentication

The authentication is done by `POST`ing user credentials (`username` and `password`) to the `/api/auth` route, it will return a JWT token which will be used for authentication.
Every subsequent request that requires authentication will have to include the token on an `auth-token` header, the server will now know your permissions and your user id.

# 3. Roadmap

- [x] User manager
- [x] Authentication
- [x] Equipment system
- [ ] Password manager
- [ ] Backup control - To be scraped

# 4. How to run

## 4.1. Dotenv

Create a file named `.env` at the root of the project with the following variables:

- `FLASK_ENV`: either **development** or **production**, turns on/off Flask development features,
- `SQL_LOGS`: either **TRUE** or **FALSE**, turns on SQLAlchemy's SQL logs, useful for debugging,
- `DATABASE`: SQLAlchemy's database system, I usually use `sqlite:///db.sqlite3`,
- `SECRET_KEY`: Key used to create **JWT** tokens,
- `MASTER_TOKEN`: Token used to access all systems without need for authentication.

## 4.2. App

- Start the app with `> python3 start.py`
- Run tests with `> python -m unittest discover tests`

# 5 Todo

- Username and Password validation
- Changes history / Audit trail
