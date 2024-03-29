from random import randint

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from PIL import Image, ImageDraw, ImageFont

from .models import BannerConfigEntry, Side, Team

TEAMS_PER_COLUMN = 5
TEAMS_LIMIT = TEAMS_PER_COLUMN * 3
WHITE = (229, 229, 229)

def _get_config(name):
    config = BannerConfigEntry.objects.get(name=name)
    return config.x1, config.y1, config.x2, config.y2, config.size

def _draw_images(images, target, debug=False):
    for name, filename in images:
        image = Image.open(filename, 'r').convert('RGBA')
        x, y, w, h, _ = _get_config(name)
        if w > 0 and h > 0:
            image = image.resize((w, h))
        target.paste(image, box=(x, y), mask=image)
        if debug:
            draw = ImageDraw.Draw(target)
            draw.rectangle((x, y, x+image.width, y+image.height))

def _draw_points(target, side_left, side_right, debug=False):
    font_points = ImageFont.truetype('font.otf', 55)
    draw = ImageDraw.Draw(target)

    logo_left = BannerConfigEntry.objects.get(name='logo_left')
    logo_right = BannerConfigEntry.objects.get(name='logo_right')
    logo_left_r = logo_left.x1 + logo_left.x2
    points_middle = (
        logo_left_r + ((logo_right.x1 - (logo_left_r)) / 2),
        logo_left.y1 + (logo_left.y2 / 2)
    )
    # NOTE: The separator here is an en dash, not a minus
    points_text = "{} – {}".format(side_left.points, side_right.points)
    points_w, points_h = font_points.getsize(points_text)
    points_corner = (
        points_middle[0] - (points_w / 2),
        points_middle[1] - (points_h / 2),
    )
    if debug:
        draw.rectangle((
            points_corner,
            (points_corner[0]+points_w, points_corner[1]+points_h)))
        draw.point(points_middle, fill='red')
    draw.text(points_corner,
              points_text,
              font=font_points, align='center', fill=WHITE)

def _draw_leaderboard(target, debug=False):
    draw = ImageDraw.Draw(target)
    #draw.line((650, 50, 650, 350), fill=WHITE, width=2)
    wx, wy, wrx, wry, _ = _get_config('wins')
    nx, ny, nrx, nry, _ = _get_config('names')

    font_leaderboard = ImageFont.truetype('DejaVuSans-Bold.ttf', 40)
    font_headings = ImageFont.truetype('DejaVuSans-Bold.ttf', 18)
    #draw.text((700, 50), "Top teams", font=font_leaderboard, fill=WHITE)

    font_teams = ImageFont.truetype('DejaVuSans-Bold.ttf', 20)
    teams = Team.objects.filter(side__active=True)[:TEAMS_LIMIT]
    longest_name = ""
    for team in teams:
        if len(team.name) > len(longest_name):
            longest_name = team.name
    name_size = draw.textsize(longest_name, font_teams)
    padding = name_size[0] + 70 + 20
    #print(f"{padding=}")
    #print(f"{longest_name=}")
    team_chunks = _chunk_list(teams, TEAMS_PER_COLUMN)
    for i, chunk in enumerate(team_chunks):
        draw.text((wx + i * padding, wy), "points", fill='gray', font=font_headings, anchor="ls")
        draw.text((nx + i * padding, ny), "name", fill='gray', font=font_headings)
        for j, team in enumerate(chunk):
            wins = str(team.points)
            name = team.name
            colour = team.side.colour
            draw.text((wrx + i * padding, wry + j * 25), wins, fill=WHITE, font=font_teams)
            draw.text((nrx + i * padding, nry + j * 25), name, fill=colour, font=font_teams)

def _chunk_list(iterable, chunk_size):
    d = {}
    for i, x in enumerate(iterable):
        d.setdefault(i//chunk_size, []).append(x)
    return(d.values())

def generate_banner(debug=False, rainbow=False):
    sides = Side.objects.filter(active=True)
    side_left = sides[0]
    side_right = sides[1]

    logos = [
        ('logo_main', 'media/image/logo_text_wide_resize.png'),
        #('logo_left', side_left.logo),
        #('logo_right', side_right.logo),
    ]

    bgcolour = 'black'
    if rainbow:
        bgcolour = (randint(0, 255), randint(0, 255), randint(0, 255))
    banner = Image.new('RGB', (1000, 400), color = bgcolour)
    _draw_images(logos, banner, debug)
    #_draw_points(banner, side_left, side_right, debug)
    _draw_leaderboard(banner, debug)

    return banner

@cache_page(15)
def banner(request):
    debug = request.GET.get('debug', 'false') == "true"
    rainbow = 'rainbow' in request.GET
    img = generate_banner(debug, rainbow)
    extension = request.path.split('.')[-1]
    if extension == "jpg":
        response =  HttpResponse(content_type="image/jpeg")
        img.save(response, 'jpeg')
    elif extension == "png":
        response =  HttpResponse(content_type="image/png")
        img.save(response, 'png')
    return response

def index(request):
    return HttpResponse('<html><head><meta http-equiv="refresh" content="60"></head><body><style>* { background: black; }</style><img src="/image/banner.jpg"></body></html>')
