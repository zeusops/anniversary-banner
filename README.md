# Zeus Operations Anniversary 2020 banner

A banner for displaying points in TeamSpeak and Discord during the Zeus
Operations Anniversary 2020. Created by [Gehock](https://github.com/Gehock).

## How to use

Download a font you want to use, for example Typo Grotesk from
<https://www.dafont.com/typo-grotesk.font> and place
`Typo Grotesk Bold Demo.otf` under `banner/font.otf`.

### Font setup

```
curl "https://dl.dafont.com/dl/?f=typo_grotesk" > font.zip
mkdir tmp
unzip font.zip -d tmp
mv tmp/Typo\ Grotesk\ Demo.otf banner/font.otf
rm -r tmp
```

### Installing memcached

```
apt-install memcached
```

### Running

```
python3 -m virtualenv venv
source venv/bin/activate
cd banner
./manage.py runserver
```
