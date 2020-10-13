from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
from random import randint

from .models import Side, Team, BannerConfigEntry

TEAMS_LIMIT = 8
WHITE = (229, 229, 229)

def _get_config(name):
    config = BannerConfigEntry.objects.get(name=name)
    return config.x1, config.y1, config.x2, config.y2, config.size

def _draw_images(images, target, debug=False):
    for name, filename in images:
        image = Image.open(filename, 'r')
        x, y, w, h, _ = _get_config(name)
        if w > 0 and h > 0:
            image = image.resize((w, h))
        target.paste(image, box=(x, y), mask=image)
        if debug:
            draw = ImageDraw.Draw(target)
            draw.rectangle((x, y, x+image.width, y+image.height))

def _draw_points(target, side_left, side_right, debug=False):
    # logo = Image.open('images/logo_text_resize.png', 'r')
    # logo_left = Image.open(side_left.logo, 'r')
    # logo_right = Image.open(side_right.logo, 'r')
    # banner.paste(logo, (x1, y1), mask=logo)
    # banner.paste(logo_left, (50, 240), mask=logo_left)
    # banner.paste(logo_right, (485, 240), mask=logo_right)
    # font_points = ImageFont.truetype('DejaVuSans-Bold.ttf', 80)
    font_points = ImageFont.truetype('Typo Grotesk Bold Demo.otf', 80)
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
    # points_corner = points_middle
    draw.text(points_corner,
              points_text,
              font=font_points, align='center', fill=WHITE)

def _draw_leaderboard(target, debug=False):
    draw = ImageDraw.Draw(target)
    draw.line((650, 50, 650, 350), fill=WHITE, width=2)

    font_leaderboard = ImageFont.truetype('DejaVuSans-Bold.ttf', 40)
    font_headings = ImageFont.truetype('DejaVuSans-Bold.ttf', 18)
    draw.text((700, 50), "Top teams", font=font_leaderboard, fill=WHITE)
    draw.text((700, 110), "wins", fill='gray', font=font_headings, anchor="ls")
    draw.text((770, 110), "name", fill='gray', font=font_headings)

    font_teams = ImageFont.truetype('DejaVuSans-Bold.ttf', 20)
    teams = Team.objects.filter(side__active=True)[:TEAMS_LIMIT]
    for i, team in enumerate(teams):
        wins = str(team.points)
        name = team.name
        colour = team.side.colour
        draw.text((715, 150 + i * 25), wins, fill=WHITE, font=font_teams)
        draw.text((770, 150 + i * 25), name, fill=colour, font=font_teams)

def generate_banner(debug=False):
    sides = Side.objects.filter(active=True)
    side_left = sides[0]
    side_right = sides[1]

    logos = [
        ('logo_main', 'images/logo_text_resize.png'),
        ('logo_left', side_left.logo),
        ('logo_right', side_right.logo),
    ]

    # bgcolour = (randint(0, 255), randint(0, 255), randint(0, 255))
    bgcolour = 'black'
    banner = Image.new('RGB', (1000, 400), color = bgcolour)
    _draw_images(logos, banner, debug)
    _draw_points(banner, side_left, side_right, debug)
    _draw_leaderboard(banner, debug)

    return banner

def banner(request):
    # colour_blufor = 'DodgerBlue'
    # colour_blufor = (0, 77, 153)
    # colour_blufor = (45, 101, 153)
    # colour_blufor = (50, 100, 165)
    # # colour_redfor = (128, 0, 0)
    # colour_redfor = (170, 0, 0)

    # sides = Side.objects.filter(active=True)
    # side_left = sides[0]
    # side_right = sides[1]

    # red_points = request.GET.get('red_points', 10)
    # blue_points = request.GET.get('blue_points', 4)
    # team_name = request.GET.get('team_name', "Old gang")
    # team_points = request.GET.get('team_points', 3)
    # team_side = request.GET.get('team_side', colour_blufor)
    debug = request.GET.get('debug', 'false') == "true"
    response =  HttpResponse(content_type="image/png")
    # teams = (
    #     (6, "Terry's 10heads", colour_redfor),
    #     (4, "Monkey men", colour_blufor),
    #     (4, "Charlies", colour_redfor),
    #     (3, "Yonkee donkey", colour_redfor),
    #     (team_points, team_name, team_side),
    # )
    img = generate_banner(debug)
    img.save(response, 'png')
    return response

def index(request):
    return HttpResponse("Hello there")
