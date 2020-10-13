from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
from random import randint

from .models import Side, Team


def generate_banner():
    sides = Side.objects.filter(active=True)
    side_left = sides[0]
    side_right = sides[1]


    # bgcolor = (randint(0, 255), randint(0, 255), randint(0, 255))
    bgcolour = 'black'
    banner = Image.new('RGB', (1000, 400), color = bgcolour)
    logo = Image.open('images/logo_text_resize.png', 'r')
    logo_left = Image.open(side_left.logo, 'r')
    logo_right = Image.open(side_right.logo, 'r')
    banner.paste(logo, (50, 40), mask=logo)
    banner.paste(logo_left, (50, 240), mask=logo_left)
    banner.paste(logo_right, (485, 240), mask=logo_right)

    font_points = ImageFont.truetype('DejaVuSans-Bold.ttf', 80)
    draw = ImageDraw.Draw(banner)
    draw.text((200, 245),
              "{} - {}".format(side_left.points, side_right.points),
              font=font_points)

    draw.line((650, 50, 650, 350), fill='white', width=2)

    font_leaderboard = ImageFont.truetype('DejaVuSans-Bold.ttf', 40)
    font_headings = ImageFont.truetype('DejaVuSans-Bold.ttf', 18)
    draw.text((710, 50), "Top teams", font=font_leaderboard)
    draw.text((700, 110), "wins", fill='gray', font=font_headings, anchor="ls")
    draw.text((855, 110), "name", fill='gray', font=font_headings)

    font_teams = ImageFont.truetype('DejaVuSans-Bold.ttf', 23)
    teams = Team.objects.filter(side__active=True)
    for i, team in enumerate(teams):
        wins = str(team.points)
        name = team.name
        colour = team.side.colour
        draw.text((715, 150 + i * 40), wins, fill=colour, font=font_teams)
        draw.text((770, 150 + i * 40), name, fill=colour, font=font_teams)
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
    response =  HttpResponse(content_type="image/png")
    # teams = (
    #     (6, "Terry's 10heads", colour_redfor),
    #     (4, "Monkey men", colour_blufor),
    #     (4, "Charlies", colour_redfor),
    #     (3, "Yonkee donkey", colour_redfor),
    #     (team_points, team_name, team_side),
    # )
    img = generate_banner()
    img.save(response, 'png')
    return response

def index(request):
    return HttpResponse("Hello there")
