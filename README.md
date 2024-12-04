# LABS_VIDEO

## Seminari 1

Tenim tres fitxers:

- Seminari1.py: Aquí tenim totes les classes i mètodes

- our_test.py: Aquí hem fet el nostre propi test, cridant als mètodes i observant els resultats.

- unit_test.py: Apliquem el test proporcionat per la IA. No hem solucionat el dos testos amb error. 

Comentaris de cada exercici:

2) En el nostre test, veiem que de rgb a yuv funciona però de yuv a rgb no. Hem seguit la fórmula proporcionada.

3) Pel resize, en el nostre test,  hem reduït la imatge a dues escales diferents. Les imatges resultants estan penjades al repositori com a nudibraqui_R1.jpg i nudibraqui_R2.jpg

4) Pel nostre test, hem creat una matriu de números que llegits amb serpentina surten en ordre.

5.1) Imatge resultant penjada al git com a nudibranqui_blw.jpg

6) Pel nostre test, hem comprovat la funció creada amb el resultat de la llibreria fftpack

7) Obtenim quatre imatges amb la combinació d’aplicar low-pass i high-pass filters. Per tenir les imatges hem executat el codi en un jupyternotebook. Hem penjat al git el resultat com a DWT_results

## Practica 1
Tenim dos endpoints `service1` i `service2` creats amb `FastAPI`:
- Service1: implemeta tres funcionalitats
  - `/`: retorna `{"Hello": "World"}`
  - `/rgb_to_yuv/{R}/{G}/{B}`: transforma cordenades RGB a YUV
  - `/ffmpeg_resize/{scale_x}/{scale_y}`: escala una imatge (fitxer passat a traves de l'API)
 
- Service2: implementa una funcionalitat
  - `/ffmpeg_bw/`: transforma una imatge a blanc i negre (fitxer passat a traves de l'API)
 
Per crear les imatges docker, en el terminal a la carpeta de cada servei:

```
docker build -t service1 .
```

```
docker build -t service2 .
```

Per engegar els containers:

```
docker run -d --name service1_container -p 80:80 service1
```

```
docker run -d --name service2__container -p 80:80 service2
```
Per provar les diferents funcionalitats:
Utilitzar en el navegador `http://127.0.0.1/docs`

Per executar els dos serveis amb el compose, anar a la carpeta principal i executar:

```
docker-compose up -d --build
```

Utilitzar en el navegador `http://127.0.0.1:8001/docs` i `http://127.0.0.1:8000/docs`

## Seminari 2
Service1: implementa tots els exercicis. A continuació trobem explicació de què fa cada punt.
  - `ffmpeg_resize_v`: modifica resolució del vídeo proporcionat
  - `ffmpeg_chroma`: canvia chroma sampling ( no veiem diferència en el color del vídeo de sortida).
  - `ffmpeg_i`: retorna nom del codec, amplada, alçada, durada i bit rate del vídeo.
  - ffmpeg_audio: extreu 20s de video sense audio i l'audio de 20s de video en `aac`, `mp3` i `ac3`. Després ho trona ajuntar tot.
  - `ffmpeg_tracks`: retorna els tracks del fitxer proporcionat
  - `ffmpeg_motion`: retorna el vídeo amb motion vectors
  - `ffmpeg_histogram`: retorna el vídeo amb histograma YUV
 
Per crear la imatga docker, en el terminal a la carpeta de servei1:

```
docker build -t service1 .
```
Per engegar el container:

```
docker run -d --name service1_container -p 80:80 service1
```
Utilitzar en el navegador `http://127.0.0.1/docs`
