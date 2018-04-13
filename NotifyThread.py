#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import random
import telebot
import json
from threading import Thread, Lock


USERS_FILE = 'dataDir/users.json'

class NotifyThread(Thread):
    def __init__(self, bot, dictionary):
        super(NotifyThread, self).__init__()
        self.bot = bot
        self.last_time = 0
        self.daemon = True
        self.users_topics = {}
        self.users_intervals = {}
        self.users_last_times = {}
        self.dictionary = dictionary
        self.running = True
        self.loadUserData()
        print (self.users_topics)
        self.last_save_time = 0;
        self.data_lock = Lock()
        self.start()

    def loadUserData(self):
        with open(USERS_FILE, 'rw') as f:
            try:
                user_data = json.loads(f.readline())
                for u, ud in user_data.items():
                    self.users_intervals[u] = ud['interval']
                    self.users_topics[u] = ud['topics']
                    self.users_last_times[u] = 0
            except Exception as e:
                return


    def saveUserData(self):
        with open(USERS_FILE, 'w') as f:
            try:
                data = {}
                for u, top in self.users_topics.items():
                    data[u] = {}
                    data[u]['topics'] = top
                    data[u]['interval'] = self.users_intervals[u]

                print data
                f.write(json.dumps(data))
            except Exception as e:
                print ('save UserData error ' + str(e))
                return

    def stop(self):
        self.data_lock.acquire()
        try:
            self.saveUserData()
            self.running = False
        finally:
            self.data_lock.release()


    def addUserTime(self, user_id, time):
        self.data_lock.acquire()
        user_id = str(user_id)
        print ('add')
        try:
            self.users_intervals[user_id] = time
            self.users_last_times[user_id] = 0
        finally:
            self.data_lock.release()

    def addUserTopic(self, user_id, topic):
        user_id = str(user_id)
        self.data_lock.acquire()
        try:
            if not (user_id in self.users_topics.keys()):
                self.users_topics[user_id] = []
            if not (topic in self.users_topics[user_id]):
                self.users_topics[user_id].append(topic)
        finally:
            self.data_lock.release()


    def get_words(self, user_id):
        user_id = str(user_id)
        all_cnt = 0
        print (self.users_topics)
        for t in self.users_topics[user_id]:
            all_cnt = all_cnt + len(self.dictionary[t])
        idx = random.randint(0, all_cnt - 1)

        temp = 0
        for t in self.users_topics[str(user_id)]:
            if idx >= temp + len(self.dictionary[t]):
                temp = temp + len(self.dictionary[t])
                continue
            return self.dictionary[t][idx - temp]

    def run(self):
        while True:
            fl = True
            self.data_lock.acquire()
            try:
                fl = self.running
            finally:
                self.data_lock.release()
            if not fl:
                break

            print ('run')
            t = time.time()

            self.data_lock.acquire()
            print self.users_topics
            print self.users_intervals
            print self.users_last_times
            try:
                if t - self.last_save_time >= 1200:
                    self.saveUserData()
                    self.last_save_time = t

                for u, ut in self.users_last_times.items():
                    if t - ut > self.users_intervals[u]:
                        print ('I want to send')
                        self.users_last_times[u] = t
                        self.bot.send_message(u, self.get_words(u))

            finally:
                self.data_lock.release()
            time.sleep(5)
        # print p.stdout.readlines()
# print err