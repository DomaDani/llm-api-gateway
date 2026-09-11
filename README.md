# LLM-API-gateway

## Note

A projekt az egyetem belső GitLab szerverén készült, a CI/CD pipeline ezáltal GitLab környezetre lett elkészítve. Ez a repozitórium archiválási célokat szolgál.
\
This project was developed on the university's internal GitLab server. As such, the CI/CD pipeline was made for a GitLab environment. This repository is for archival purposes.

## Description
> BSc Szakdolgozat, ELTE IK, Gulyás Domokos Dániel\
> BSc Thesis, ELTE IK, Domokos Dániel Gulyás

Adminisztrációs felület és API gateway lokális LLM szolgáltatásokhoz. Egy konténerizált alkalmazás, amely képes kapcsolódni egy lokálisan futatott LLM-hez. Az adminisztrációs felületen létrehozhatóak API kulcsok, valamint megszabhatóak a kulcsokhoz, projektekhez és globális térhez tartózó kvóták. Az API gateway ellenőrzi a kulcsokat, betartatja a kvótákat és proxyként működik a felhasználó és az LLM között.\
\
Dashboard and API gateway for local LLM services. This is a containerised application, capable of connecting to a locally run LLM. On the administrative dashboard, API keys can be created and quotas can be set for keys, projects and for the global scope. The gateway verifies API keys, enforces the limits and acts as a proxy between the user and the LLM.

## Installation
A projekt a Docker Compose segítségével, konténerizáltan futtatható. Első futtatás előtt létre kell hozni és a gyökérkönyvtárban el kell helyezni a `.env` konfigurációs fájlt. Ehhez sabloként használható a `.env.example` fájl használható.
```console
docker compose up
```
\
This project can be run containerised using Docker Compose. Before the first run, you need to create a `.env` file and place it at repo root. `.env.example` is provided as an example for this.
```console
docker compose up
```

## Authors and acknowledgment
Készítette / Created by: Gulyás Domokos Dániel\
Témavezető / Thesis supervisor: Gyöngyössy Natabara\
\
Eötvös Loránd Tudományegyetem, Informatikai Kar, Programtervező Informatikus BSc\
Eötvös Loránd University, Faculty of Informatics, Computer Science BSc

## License
Ez a projekt a GNU GPLv3 licenc alatt áll.
\
This project is licensed under GNU GPLv3.

## Project status
A projekt a BSc szakdolgozat részeként elkészült. A teljes funkcionalitáshoz szükséges követelmények teljesülnek, a rendszer stabil állapotban van.
\
The project has been completed as part of the BSc thesis. The project meets the requirements for full functionality and is in a stable state.