#!/usr/bin/env python
# -*- coding: utf-8 -*-
# email_scrapper.py
# Script to scrape email addresses.

# Copyright (c) 2021, Ulises M. Alvarez
# All rights reserved.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Based on an email scrapper by Vanessa Leung
# https://medium.com/swlh/how-to-scrape-email-addresses-from-a-website-and-export-to-a-csv-file-c5d1becbd1a0

# Librerias
import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd
import sys, os, subprocess, time, shlex
import os.path as path

# Fecha y hora
# Copyright (c) 2020, Marco Antonio Martínez García
from datetime import datetime
ahora = datetime.now()
anio = ahora.year
mes = '{:02d}'.format(ahora.month)
dia = '{:02d}'.format(ahora.day)
hora = '{:02d}'.format(ahora.hour)
minutos = '{:02d}'.format(ahora.minute)
segundos = '{:02d}'.format(ahora.second)

# Fecha y Hora
pfecha = str(anio) + str(mes) + str(dia)  # modified to 20210413
phora = str(hora) + str(minutos) + str(segundos)

original_url = input("Enter the website url: ") 

unscraped = deque([original_url])  

scraped = set()  

emails = set()  

while len(unscraped):
    url = unscraped.popleft()  
    scraped.add(url)

    parts = urlsplit(url)
        
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    if '/' in parts.path:
      path = url[:url.rfind('/')+1]
    else:
      path = url

    print("Crawling URL %s" % url)
    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        continue

    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.mx", response.text, re.I))
    emails.update(new_emails) 

    soup = BeautifulSoup(response.text, 'lxml')

    for anchor in soup.find_all("a"):
      if "href" in anchor.attrs:
        link = anchor.attrs["href"]
      else:
        link = ''

        if link.startswith('/'):
            link = base_url + link
        
        elif not link.startswith('http'):
            link = path + link

        if not link.endswith(".gz"):
          if not link in unscraped and not link in scraped:
              unscraped.append(link)

df = pd.DataFrame(emails, columns=["email"])
df.to_csv('email' + '_' + pfecha + '_' + phora + '.csv', index=False)
