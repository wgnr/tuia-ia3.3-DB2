from datetime import datetime
import click
import requests
from os import environ


def parse_date(d: str) -> str:
    try:
        return datetime.strptime(d, '%Y-%m-%d').isoformat()
    except:
        return datetime.strptime(d, '%Y-%m-%dT%H:%M:%S').isoformat()


@click.group()
def cli():
    pass


EVENT_TYPES = ['gratis', 'paga', 'gorra']
DISTRITO_CODES = ['437', '438', '441', '442', '440', '439']
TICKET_TYPES = ['FIJO', 'DESDE', 'POR_MES',
                'AGOTADAS', 'TOTAL', 'POR_VEZ', 'GRATIS', '']


@cli.command()
@click.option('--name', prompt=True, required=True, help="Event's name")
@click.option('--date_start', prompt=True, show_default=True,  default=datetime.now().date().isoformat(), type=parse_date, help="Event's start date")
@click.option('--date_end', prompt=True, show_default=True,  default=datetime.now().date().isoformat(), type=parse_date, help="Event's end date")
@click.option('--ticket', prompt=True, show_default=True, required=True, default=EVENT_TYPES[0], type=click.Choice(EVENT_TYPES), help="Event type")
@click.option('--text', prompt=True, show_default=False, default="", help="Event description")
@click.option('--ticket_value', prompt=True, show_default=False, default="", help="Ticket cost comments")
@click.option('--eventual_name', prompt=True, show_default=False, default="", help="Eventual Name")
@click.option('--eventual_direccion', prompt=True, show_default=False, default="", help="Eventual Direccion")
@click.option('--eventual_coords', prompt=True, show_default=False, default="", help="Eventual Coords")
@click.option('--eventual_distrito', prompt=True, show_default=False, default=DISTRITO_CODES[0], type=click.Choice(DISTRITO_CODES), help="Eventual Distrito")
@click.option('--suspendida', prompt=True, show_default=True, default=False, is_flag=True, help="Describe wether the current event is suspended")
@click.option('--regla', prompt=True, show_default=False, default=0, type=int, help="Regla")
@click.option('--regla_er', prompt=True, default=0, show_default=True, help="Regla Er")
@click.option('--ticket_tipo', prompt=True, show_default=False, required=False, default=TICKET_TYPES[-1], type=click.Choice(TICKET_TYPES), help="Ticket type")
@click.option('--ticket_valor', prompt=True, show_default=True,  default=0, type=float, help="Ticket cost")
@click.option('--ticket_paga_menor_4', prompt=True, show_default=True,  default=False, type=bool, help="Event free for children under 4 years-old")
def event_create(**kwards):
    """Create a new event"""
    data = {k: v for k, v in kwards.items() if v}
    if not data:
        click.echo(
            "You sould specify at least one criteria. type '--help' for more information.")
        return
    response = requests.post(f"{API_BASE}/event", json=data)
    click.echo(response.json())


@cli.command()
@click.argument('event_id', type=int)
def event(event_id):
    """Get event by id"""
    response = requests.get(f'{API_BASE}/event/{event_id}')
    click.echo(response.json())


@cli.command()
@click.argument('event_id', type=int)
@click.option('--data', prompt='Event data in JSON format.', help='The event data to be updated.')
def event_update(event_id, data):
    """Updates event information based on the event id"""
    response = requests.put(f'{API_BASE}/event/{event_id}', data=data)
    click.echo(response.json())


@cli.command()
@click.argument('event_id', type=int)
def event_suspend(event_id):
    """Suspends an event"""
    response = requests.delete(f'{API_BASE}/event/{event_id}')
    click.echo(response.json())


@cli.command()
@click.argument('activity_id', type=int)
def activity(activity_id):
    """Get events based on an activity number"""
    response = requests.get(f'{API_BASE}/activity/{activity_id}')
    click.echo(response.json())


@cli.command()
@click.option('--name', default=None, help='Event name')
@click.option('--ticket', default=None, type=click.Choice(['gratis', 'paga', 'gorra']), multiple=True, help='Select one or more event type.')
@click.option('--ticket_tipo', default=None, type=click.Choice(['FIJO', 'DESDE', 'POR_MES', 'AGOTADAS', 'TOTAL', 'POR_VEZ', 'GRATIS']), multiple=True, help='Select one or more ticket types.')
@click.option('--ticket_valor_min', default=None, type=float, help='Minimum ticket value')
@click.option('--ticket_valor_max', default=None, type=float, help='Maximum ticket value')
@click.option('--ticket_paga_menor_4', default=None, type=bool, help='Event free for children under 4 years-old')
@click.option('--date_start', default=None, type=parse_date, help='Event start date/time (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)')
@click.option('--date_end', default=None, type=parse_date, help='Event etart date/time (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)')
@click.option('--eventual_direccion', default=None, help='Event address')
@click.option('--actividad', default=None, type=int, help='Activity Number')
def search(**kwards):
    """Serch for events based on several filters criteria"""
    data = {k: v for k, v in kwards.items() if v}
    if not data:
        click.echo(
            "You sould specify at least one criteria. type '--help' for more information.")
        return
    response = requests.post(f'{API_BASE}/search', json=data)
    click.echo(response.json())


if __name__ == '__main__':
    try:
        API_BASE = environ["APP_WEB_SOCKET"]
    except KeyError:
        API_BASE = 'http://127.0.0.1:8000'
    cli()
