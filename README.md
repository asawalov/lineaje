# Parking Lot Management System

## Overview
This folder contains the implementation of a Parking Lot Management System, 
designed to efficiently manage parking spaces across multiple lots and floors. 
The system is built using Django and Django REST Framework, featuring a suite
of APIs that handle parking sessions, spot occupancy, and payment processing.

Imp -> As discussed to create the overview for overallparkingstatus and byfloorparkingstatus i have not created that, as this
model is not customer centric and all this view will be needed if model is customer centric .
I created the views such as the whole system is automated .

## Login Api
input -> license_plate and vehicle_type
We will check first if any spot is available or not according to vehicle type and if spot is available on any floor
we will fetch the spot make that occupied and then create a session with license plate and the spot_obj and then return
the free_spot_number and the session_id (for our use case) on the slip.
Response - > {'floor': floor.floor_number, 'free_spot_id': free_spot_id, 'session_id': session_obj.id}

## Logout Api
input -> session_id (We have mentioned this on the slip provided to user)
From the session_id we will fetch session obj and now we have start_time and end_time,
so according to that we will calculate the cost , cost being mentioned in rate class and 
finally return cost on the slip,i.e. user can pay and left the parking log
and as soon as user has paid we will mark that spot occupied = False.
Response - > {'message': 'Successfully logged out', 'total_cost': total_cost}

## Rate change api
To change rhe rate for the vehicle api
input -> spot_type and rate_per_hour
Response -> {'message': 'Rate changed successfully'}

## Features
Real-time tracking of parking spot availability.
User session management for parking (login/logout).
Payment processing based on parking duration and vehicle type.
Admin functionalities to adjust parking rates.


## Getting Started
Prerequisites
Python 3.x
Django
Django REST Framework


## API Endpoints
POST /api/login/ - Start a parking session.
POST /api/logout/ - End a parking session.
POST /api/rate-change/ - Admin endpoint to change parking rates.
