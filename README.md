# Universidad Nacional de Rosario
## Tecnicatura Universitaria en Inteligencia Artifical
### IA3.5 Redes de Datos
## Trabajo Práctico Final

Trabajo practico de Redes de Datos de la TUIA. Consiste en un servidor REST api hecho en Python usando el framework FastAPI y consumieda mendiante un CLI tambien hecho en Python usando Click.

Enunciado: (IA3.5_RD_TP_enunciado.pdf)(IA3.5_RD_TP_enunciado.pdf)

DOCENTES:
- Michelino, Juan Pablo
- Toribio, Esteban

ALUMNO: Juan Wagner

---

### Database

The dataset [events_2023](events_2023.parquet) was build fetching all the events held in Rosario in 2023 from the URL https://ws.rosario.gob.ar/web/api/v1.0/ocurrencias. 

The Jupyter notebook [scrapper.ipynb](scrapper.ipynb) describes the process to fetch, transform and export this URL.

### Instalation
```bash
git clone --depth 1 https://github.com/wgnr/tuia-ia3.3-DB2.git
cd tuia-ia3.3-DB2
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

### Usage
Always run your command with the environment activated
```bash
source venv/Scripts/activate
```

#### Server
```bash
$ python server/server.py --help
usage: server [-h] [--host HOST] [--log_level LOG_LEVEL] [--port PORT]

options:
  -h, --help            show this help message and exit
  --host HOST
  --log_level LOG_LEVEL
  --port PORT
```

For running just `python server/server.py`, tt will serve the aplicattion on `http://localhost:8000`.


For running in local area network `python server/server.py --host 0.0.0.0 --port 80`.


Swagger Docs: `/docs`


#### CLI

```bash
# In case of remote host, write server websocket url
# $ export SERVER_WEB_SOCKET="http://192.168.100.107"

$ python client/cli.py --help
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  activity       Get events based on an activity number
  event          Get event by id
  event-create   Create a new event
  event-suspend  Suspends an event
  event-update   Updates event information based on the event id
  search         Serch for events based on several filters criteria
```

Examples:

Looking for one event in particular
```bash
$ python client/cli.py event 237999
[{'name': 'Taller Dibujando historias ¿Qué historias secretas esconde el Estevez?', 'date_start': '2023-07-28T15:00:00', 'date_end': '2023-07-28T17:00:00', 'ticket': 
'paga', 'text': None, 'ticket_value': '$400', 'eventual_name': 'Museo de Arte Decorativo Firma y Odilo Estevez', 'eventual_direccion': 'SANTA FE 748', 'eventual_coords': '5440805.12347424,6354961.3519457', 'eventual_distrito': '437', 'suspendida': False, 'actividad': 237998, 'regla': 0, 'regla_er': None, 'ticket_tipo': 'FIJO', 'ticket_valor': 400.0, 'ticket_paga_menor_4': True, 'id': 237999}]
```

Searching events that meet a condition
```bash
$ python client/cli.py search --help
Usage: cli.py search [OPTIONS]

  Serch for events based on several filters criteria

Options:
  --name TEXT                     Event name
  --ticket [gratis|paga|gorra]    Select one or more event type.
  --ticket_tipo [FIJO|DESDE|POR_MES|AGOTADAS|TOTAL|POR_VEZ|GRATIS]
                                  Select one or more ticket types.
  --ticket_valor_min FLOAT        Minimum ticket value
  --ticket_valor_max FLOAT        Maximum ticket value
  --ticket_paga_menor_4 BOOLEAN   Event free for children under 4 years-old
  --date_start PARSE_DATE         Event start date/time (YYYY-MM-DD or YYYY-
                                  MM-DDTHH:MM:SS)
  --date_end PARSE_DATE           Event etart date/time (YYYY-MM-DD or YYYY-
                                  MM-DDTHH:MM:SS)
  --eventual_direccion TEXT       Event address
  --actividad INTEGER             Activity Number
  --help                          Show this message and exit.
```
```bash
# Example
$ python client/cli.py search --ticket gratis --name Biblioteca --date_start 2023-06-23 --date_end 2023-06-24
{'ticket': ('gratis',), 'name': 'Biblioteca', 'date_start': '2023-06-23T00:00:00', 
'date_end': '2023-06-24T00:00:00'}
[{'name': 'Procesos de digitalización en bibliotecas', 'date_start': '2023-06-23T18:00:00', 'date_end': '2023-06-23T20:00:00', 'ticket': 'gratis', 'text': None, 'ticket_value': None, 'eventual_name': 'Biblioteca Argentina Dr. Juan Álvarez', 'eventual_direccion': 'ROCA PTE. JULIO ARGENTINO 731', 'eventual_coords': '5439709.56,6355215.2', 'eventual_distrito': '437', 'suspendida': False, 'actividad': 233651, 'regla': 0, 'regla_er': None, 'ticket_tipo': None, 'ticket_valor': 0.0, 'ticket_paga_menor_4': True, 'id': 233655}]
```

Creating a new event
```bash
$ python client/cli.py event-create --help
Usage: cli.py event-create [OPTIONS]

  Create a new event

Options:
  --name TEXT                     Event's name  [required]
  --date_start PARSE_DATE         Event's start date  [default: 2023-06-20]
  --date_end PARSE_DATE           Event's end date  [default: 2023-06-20]
  --ticket [gratis|paga|gorra]    Event type  [default: gratis; required]
  --text TEXT                     Event description
  --ticket_value TEXT             Ticket cost comments
  --eventual_name TEXT            Eventual Name
  --eventual_direccion TEXT       Eventual Direccion
  --eventual_coords TEXT          Eventual Coords
  --eventual_distrito [437|438|441|442|440|439]
                                  Eventual Distrito
  --suspendida                    Describe wether the current event is
                                  suspended
  --regla INTEGER                 Regla
  --regla_er INTEGER              Regla Er  [default: 0]
  --ticket_tipo [FIJO|DESDE|POR_MES|AGOTADAS|TOTAL|POR_VEZ|GRATIS|]
                                  Ticket type
  --ticket_valor FLOAT            Ticket cost  [default: 0]
  --ticket_paga_menor_4 BOOLEAN   Event free for children under 4 years-old
                                  [default: False]
  --help                          Show this message and exit.
```
```bash
# crate a new event entering prompts
$ python client/cli.py event-create
Name: Taller de Stand-Up
Date start [2023-06-21]: 2023-06-24T16:00:00
Date end [2023-06-21]: 2023-06-24T21:00:00
Ticket (gratis, paga, gorra) [gratis]: gratis
Text []: 
Ticket value []: 
Eventual name []: 
Eventual direccion []: 
Eventual coords []: 
Eventual distrito (437, 438, 441, 442, 440, 439) [437]: 
Suspendida [y/N]: 
Regla [0]: 
Regla er [0]: 
Ticket tipo (FIJO, DESDE, POR_MES, AGOTADAS, TOTAL, POR_VEZ, GRATIS, ) []: 
Ticket valor [0]: 
Ticket paga menor 4 [False]:      

{'name': 'Taller de Stand-Up', 'date_start': '2023-06-24T16:00:00', 'date_end': '2023-06-24T21:00:00', 'ticket': 'gratis', 'text': None, 'ticket_value': None, 'eventual_name': None, 'eventual_direccion': None, 'eventual_coords': None, 'eventual_distrito': '437', 'suspendida': False, 'actividad': 238001, 'regla': 0, 'regla_er': None, 'ticket_tipo': None, 'ticket_valor': None, 'ticket_paga_menor_4': True, 'id': 238002}
```
