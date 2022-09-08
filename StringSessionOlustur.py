# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

import os, asyncio
from dotenv    import load_dotenv
from Kekik.cli import konsol

if not os.path.exists("ayar.env"):
    konsol.print("\n[bold red]Lütfen ayar.env dosyanızı oluşturun..\n", width=70, justify="center")
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

from pyrogram import Client

async def session_olustur():
    async with Client(SESSION_ADI, api_id=int(API_ID), api_hash=API_HASH, in_memory=True) as app:
        print("\n\n")
        print(await app.export_session_string())
        print("\n")

if __name__ == "__main__":
    try:
        asyncio.run(session_olustur())
    except Exception:
        konsol.print("\n[bold red]Lütfen ayar.env dosyanızı DÜZGÜNCE! oluşturun..[/]\n", width=70, justify="center")
        quit(1)