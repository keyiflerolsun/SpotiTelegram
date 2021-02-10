# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from pyrogram import Client, __version__
from pyrogram.raw.functions.users import GetFullUser
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from sys import version_info
import os, asyncio
from dotenv import load_dotenv
from KekikTaban import KekikTaban

taban = KekikTaban(
    baslik   = "@KekikAkademi SpotiTelegram",
    aciklama = "SpotiTelegram Başlatıldı..",
    banner   = "SpotiTelegram",
    genislik = 75
)

konsol = taban.konsol

if (taban.bellenim_surumu.split('-')[-1] != 'aws') and (not os.path.exists("ayar.env")): # Heroku Geçmek için aws
    konsol.print("\n[bold red]Lütfen ayar.env dosyanızı oluşturun..\n", width=taban.genislik, justify="center")
    quit(1)

load_dotenv("ayar.env")

# Yapılandırmanın önceden kullanılan değişkeni kullanarak düzenlenip düzenlenmediğini kontrol edin.
# Temel olarak, yapılandırma dosyası için kontrol.
AYAR_KONTROL = os.environ.get("___________LUTFEN_______BU_____SATIRI_____SILIN__________", None)

if AYAR_KONTROL:
    konsol.print("\n\t[bold red]Lütfen ayar.env dosyanızı düzenlediğinize emin olun /veya\n\tilk hashtag'de belirtilen satırı kaldırın..[/]\n")
    quit(1)


CLIENT_ID       = str(os.environ.get("CLIENT_ID", str))
CLIENT_SECRET   = str(os.environ.get("CLIENT_SECRET", str))
REDIRECT_URI    = str(os.environ.get("REDIRECT_URI", str))
KULLANICI       = str(os.environ.get("KULLANICI", str))

API_ID          = str(os.environ.get("API_ID", str))
API_HASH        = str(os.environ.get("API_HASH", str))
STRING_SESSION  = str(os.environ.get("STRING_SESSION", str))
SESSION_ADI     = str(os.environ.get("SESSION_ADI", "SpotiTelegram"))

def calan_sarki():
    kimlik = SpotifyOAuth(
        client_id     = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        redirect_uri  = REDIRECT_URI,
        username      = KULLANICI,
        scope         = "user-read-currently-playing",
        open_browser  = False,
        show_dialog   = True
    )

    if not os.path.exists(f".cache-{KULLANICI}"):
        yetkilendirme_linki = kimlik.get_authorize_url()

        konsol.print(f"\n[bold red][!] Spotify Yetkilendirmesi Yapılmamış..![/]", width=taban.genislik, justify="center")
        konsol.print(f"\n\n[yellow]Lüften link'e gidip yetkilendirmeyi tamamlayınız..[/]\n\n{yetkilendirme_linki}")

        kimlik_onay = konsol.input(f'\n[bold blue]Link ([magenta]{REDIRECT_URI}?code=QWEQWE[/]) »» :[/] ')

        try:
            token = kimlik.parse_auth_response_url(url=kimlik_onay)
            kimlik.get_access_token(token, as_dict=False, check_cache=False)
        except Exception as hata:
            konsol.print(f"\n[bold red][!] {type(hata).__name__} | {hata}[/]", width=taban.genislik, justify="center")
            exit()

        taban.temizle
        taban.logo_yazdir()
        taban.bilgi_yazdir()

        konsol.print("\n[bold green][+] Spotify Yetkilendirme Başarılı..[/]\n", width=taban.genislik, justify="center")

    spoti       = Spotify(auth_manager=kimlik)
    calan_sarki = spoti.current_user_playing_track()
    if calan_sarki:
        sarki_adi   = calan_sarki["item"]["name"]
        sanatci     = calan_sarki["item"]["artists"][0]["name"]
        return f"🎧 {sanatci} - {sarki_adi}"
    else:
        return None

try:
    SpotiTelegram       = Client(
        STRING_SESSION,
        api_id          = API_ID,
        api_hash        = API_HASH
    )
except ValueError:
    konsol.print("\n[bold red]Lütfen ayar.env dosyanızı DÜZGÜNCE! oluşturun..[/]\n", width=taban.genislik, justify="center")
    quit(1)

VAR_OLAN_BIO = ''

async def baslangic():
    await SpotiTelegram.start()

    global VAR_OLAN_BIO
    benim_varlik  = await SpotiTelegram.resolve_peer("me")
    benim_kisilik = await SpotiTelegram.send(GetFullUser(id=benim_varlik))
    VAR_OLAN_BIO  = benim_kisilik.about

    await SpotiTelegram.send_message('me', f"""__Merhaba, Ben **{SESSION_ADI}** Tarafından Gönderildim!__

__Senin Bilgilerin;__

<u>**🗂 Spotify**</u>
**CLIENT_ID     :** `{CLIENT_ID}`
**CLIENT_SECRET :** `{CLIENT_SECRET}`

<u>**🗂 Telegram**</u>
**API_ID         :** `{API_ID}`
**API_HASH       :** `{API_HASH}`
**STRING_SESSION :** `{STRING_SESSION}`

**Kendi gizliliğin için bunları kimseyle paylaşma..**""")

    surum = f"{str(version_info[0])}.{str(version_info[1])}"
    konsol.print(f"[gold1]@{SESSION_ADI}[/] [yellow]:bird:[/] [bold red]Python: [/][i]{surum}[/]\n", width=taban.genislik, justify="center")

    await SpotiTelegram.stop()

from apscheduler.schedulers.asyncio import AsyncIOScheduler

GUNCEL_BIO = ""
async def bio_guncelle():
    global GUNCEL_BIO, VAR_OLAN_BIO

    ne_dinliyorum = calan_sarki()[:71] if calan_sarki() else VAR_OLAN_BIO

    if (not GUNCEL_BIO) or (ne_dinliyorum != GUNCEL_BIO):
        GUNCEL_BIO = ne_dinliyorum

        await SpotiTelegram.update_profile(bio=f"{ne_dinliyorum}")
        konsol.print(f"[bold yellow][[bold green]+[/]][/] [bold cyan]{ne_dinliyorum}[/]")

zamanlayici = AsyncIOScheduler()
# zamanlayici.add_job(bio_guncelle, "interval", seconds=15)
zamanlayici.add_job(bio_guncelle, "interval", minutes=1)

if __name__ == "__main__":
    calan_sarki()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(baslangic())
    zamanlayici.start()
    SpotiTelegram.run()