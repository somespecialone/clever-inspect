# <p align="center">Clever inspect</p>

---

[![license](https://img.shields.io/github/license/somespecialone/clever-inspect)](https://github.com/somespecialone/clever-inspect/blob/master/LICENSE)
[![Tests](https://github.com/somespecialone/clever-inspect/actions/workflows/tests.yml/badge.svg)](https://github.com/somespecialone/clever-inspect/actions/workflows/tests.yml)
[![Docker Cloud Automated build](https://img.shields.io/docker/cloud/automated/somespecialone/clever-inspect)](https://hub.docker.com/r/somespecialone/clever-inspect)
[![Docker Image Size (latest by date)](https://img.shields.io/docker/image-size/somespecialone/clever-inspect)](https://hub.docker.com/r/somespecialone/clever-inspect)
[![Docker Image Version (latest by date)](https://img.shields.io/docker/v/somespecialone/clever-inspect)](https://hub.docker.com/r/somespecialone/clever-inspect)
[![CodeFactor](https://www.codefactor.io/repository/github/somespecialone/clever-inspect/badge)](https://www.codefactor.io/repository/github/somespecialone/clever-inspect)
[![codecov](https://codecov.io/gh/somespecialone/clever-inspect/branch/master/graph/badge.svg?token=H3JL81SL7P)](https://codecov.io/gh/somespecialone/clever-inspect)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![steam](https://shields.io/badge/steam-1b2838?logo=steam)](https://store.steampowered.com/)

Service for inspecting `CSGO` items - retrieving detail information (such as wear e.g. float value, customname,
paintseed, paintindex etc.) from `steam` game servers and enrich it with additional info from game schemas (phases,
cases, other possible stuff) from [csgo-items-db](https://github.com/somespecialone/csgo-items-db).

> This project was inspired most by [csgofloat-inspect](https://github.com/csgofloat/inspect) 💖

---
## Navigation
 - [Usage](#usage)
   - [Request params](#request-params)
   - [Response](#response)
   - [Health ➕](#health-)
 - [Integrity 🧾](#integrity-schema-)
 - [Docker 🐳](#docker-)
 - [TODO 📑](#todo-)
---

## Usage

> All info about params, responses and requests available in `openapi.json` schema on `/docs` or `/redoc` path ❗

### Request params:

| Param     | Definition                          |
|-----------|-------------------------------------|
| `s: int`  | `steamid64` of user who owns item   |
| `m: int`  | `market id` of item                 |
| `a: int`  | `asset id` of item                  |
| `d: int ` | special `d` param from inspect link |

> Params `s` and `m` are mutually exclusive ⚠.

**OR**

| Param      | Definition                                                                            |
|------------|---------------------------------------------------------------------------------------|
| `url: str` | inspect `url` (e.g. steam://rungame/730/.../+csgo_econ_action_preview%20M...A...D...) |

**Optional**

| Param       | Definition                                                                         |
|-------------|------------------------------------------------------------------------------------|
| `raw: bool` | return raw (_with decoded wear_), without additional info inspected item if `true` |

### Response

```json5
{
  "id": 1234567890,  // asset id
  "defindex": 33, 
  "rarity": 2,
  "quality": 12,
  "origin": 8,
  "paintindex": 15,  // optional
  "paintseed": 447,  // optional
  "paintwear": 0.335,  // optional
  "customname": "",  // optional
  "killeaterscoretype": null,  // optional
  "killeatervalue": null,  // optional
  "stickers": [  // optional
    {
      "slot": 0,
      "id": 5025,
      "wear": 0,  // optional
      "scale": 1,  // optional
      "rotation": 0,  // optional
      "tint_id": null,  // optional
      "sticker_kit": {
        "image": "https://steamcdn-a.akamaihd.net/apps/730/icons/econ/stickers/stockh2021/tyl_gold.92a91b7f13bb0022dd566ef608e5f118da644a8a.png",
        "name": "Tyloo (Gold) | Stockholm 2021"
      }
    }
  ],
  "item": {
    "image": "http://media.steampowered.com/apps/730/icons/econ/default_generated/weapon_mp7_hy_gelpen_light_large.e19dd688c21ae094ffc3649e80ee1c1f0959125a.png",
    "paint": {  // optional
      "name": "Gunsmoke",
      "wear_max": 0.8,
      "wear_min": 0.06
    },
    "rarity": {
      "color": "#5e98d9",
      "name": "Industrial Grade"  // optional (some agents doesn't have rarity name)
    },
    "type": {
      "category": "smg",
      "name": "MP7"
    }
  },
  "quality_name": "Souvenir",
  "wear_name": "Field-Tested",  // optional
  "origin_name": "Found in Crate"
}
```

### Health ➕

You can check health of app on `/health` path.

**Response:**

```json5
{
  "online": 2,  // count of bots working
  "total": 2,  // total count of bots
  "concurrency": 1,  //  ready to inspect item bots in queue
}
```

## Integrity schema 🧾

> From [csgo-items-db](https://github.com/somespecialone/csgo-items-db)


![integrity schema](https://github.com/somespecialone/csgo-items-db/blob/master/integrity.png?raw=true)

## Docker 🐳

Just copy content of [docker-public](docker-public)
dir to work directory on your host machine and place filled [cred.json](cred.example.json) file near.

To obtain secrets of steam account you can use [SDA](https://github.com/Jessecar96/SteamDesktopAuthenticator). Your bots
don't need to have CSGO license, service will automatically request free license for you 💌

Command to run:

```shell
docker-compose up
```

Docker spawns named volume `inspect-service-data` where `inspect-service` store cached items database. Feel free to
modify `docker-compose.yml` to provide your configuration.

List of possible **env variables** you can see in [config.py](app/core/config.py) `AppSettings`
class.

Service will be available on 80 default port ([localhost](http://localhost/) if you run it on local machine)

## TODO 📑

- [ ] Explicit error responses.
- [x] Omit `UserWarning` about api key from `steamio`.
- [x] Requesting free license for `CSGO` when started.
- [ ] Errors catching/logging when requesting free license.
