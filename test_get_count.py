#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print("First state: {}".format(storage.get(State, first_state_id)))


second_state_id = list(storage.all(State).values())[1].id
print("second state: {}".format(storage.get(State, second_state_id)))

usr = State(name="darb ghalaf")
id = usr.id
usr.save()
print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))
print("new state: {}".format(storage.get(State, id)))
