from flask import Flask, render_template, request, redirect, url_for, flash

import requests
import json
import os


app = Flask(__name__)

tipos_v = []
mov_v = []
imgs_v = []
front_images = []
back_images = []

def get_img(url, n):
    if url:
        response = requests.get(url, stream=True) # stream para descargar obj binario
        if response.status_code == 200:
            with open('static/' +n + url[-4::], 'wb') as file:
                for chunk in response.iter_content():
                    file.write(chunk)
                imgs_v.append(n + url[-4::])

        response.close()
        

def get_pokemons_img(url ='https://pokeapi.co/api/v2/pokemon-form', offset = 0, name = ''):
    response = requests.get(url)
    lista = response.json()
    results = lista.get('results', [])
    next = lista.get('next',[])
    if response.status_code == 200:
        for p in results:
            if p['name'] == name:
                response = requests.get(p['url'])
                lista = response.json()
                if response.status_code == 200:
                    for i in lista['sprites']:
                        #print(lista['sprites'][i])
                        if lista['sprites'][i]:
                            get_img(lista['sprites'][i], i)
                return
        if next:
            get_pokemons_img(url = next, name=name)
                    

def get_mov(url ='https://pokeapi.co/api/v2/pokemon-form', offset = 0, name = ''):
    response = requests.get(url)
    lista = response.json()
    results = lista.get('results', [])
    next = lista.get('next',[])
    if response.status_code == 200:
        for p in results:
            if p['name'] == name:
                response = requests.get(p['url'])
                lista = response.json()
                if response.status_code == 200:
                    response = requests.get(lista['pokemon']['url'])
                    lista = response.json()
                    if response.status_code == 200:
                        for m in lista['moves']:
                            mov_v.append(m['move']['name'])
                            #print(m['move']['name'])
                        for t in lista['types']:
                            tipos_v.append(t['type']['name'])
                            print(t['type']['name'])

                    return

        if next:
            get_mov(url = next, name=name)



def separate_imgs(imgs):
    for i in imgs:
        if i[0] == 'f':
            front_images.append('static/' +i)
        if i[0] == 'b':
            back_images.append('static/'+i)

def startw():
    tipos_v = []
    mov_v = []
    imgs_v = []
    front_images = []
    back_images = []

@app.route('/')
def index():
    startw()

    return render_template('index.html')
    # return 'Hola mundo'


@app.route('/show_info', methods = ['POST'])
def add_user():
    if request.method == 'POST':
        pk = request.form['pokemon']
        startw()
        get_mov(name = pk)
        get_pokemons_img(name = pk)
        separate_imgs(imgs_v)
        print(tipos_v)
        print(mov_v)
        print(back_images)
        return render_template('result.html', tipos_v = tipos_v, mov_v = mov_v, front_images = front_images, back_images= back_images, pk = pk)


if __name__ == '__main__':
    app.run(port=4000,debug=True)