import requests
from pyrogram import *
from pyrogram.types import *
from SUKOONXCHATBOT import app
from config import RAPIDAPI_KEY

@app.on_message(filters.command(["bin", "ccbin", "bininfo"], [".", "!", "/"]))
async def check_ccbin(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "<b>Please Give Me a Bin To\nGet Bin Details !</b>"
        )
    try:
        await message.delete()
    except:
        pass
    aux = await message.reply_text("<b>Checking ...</b>")
    bin_code = message.text.split(None, 1)[1]
    if len(bin_code) < 6:
        return await aux.edit("<b>❌ Wrong Bin❗...</b>")
    
    url = "https://bin-ip-checker.p.rapidapi.com/"
    querystring = {"bin": bin_code}

    if not RAPIDAPI_KEY:
        return await aux.edit("<b>RapidAPI key missing. Set RAPIDAPI_KEY in environment to use BIN lookup.</b>")

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "bin-ip-checker.p.rapidapi.com"
    }
    
    try:
        response = requests.post(url, headers=headers, params=querystring)
        data = response.json()
        
        if data.get("success", False):
            bin_info = data.get("BIN", {})
            await aux.edit(f"""
<b> 𝗩𝗔𝗟𝗜𝗗 𝗕𝗜𝗡 ✅</b>

<b>┏━◆</b>
<b>┣〖🏦 ʙᴀɴᴋ</b> ⇾<tt>{bin_info.get('issuer', {}).get('name', 'N/A')}</tt>
<b>┣〖💳 ʙɪɴ</b> ⇾<tt>`{bin_code}`</tt>
<b>┣〖🏡 ᴄᴏᴜɴᴛʀʏ</b> ⇾<tt>{bin_info.get('country', {}).get('country', 'N/A')}</tt>
<b>┣〖🇮🇳 ғʟᴀɢ</b> ⇾<tt>{bin_info.get('country', {}).get('alpha2', 'N/A')}</tt>
<b>┣〖🧿 ɪsᴏ</b> ⇾<tt>{bin_info.get('country', {}).get('alpha3', 'N/A')}</tt>
<b>┣〖⏳ ʟᴇᴠᴇʟ</b> ⇾<tt>{bin_info.get('level', 'N/A')}</tt>
<b>┣〖🔴 ᴘʀᴇᴘᴀɪᴅ</b> ⇾<tt>{'Yes' if bin_info.get('type') == 'DEBIT' else 'No'}</tt>
<b>┣〖🆔 ᴛʏᴘᴇ</b> ⇾<tt>{bin_info.get('type', 'N/A')}</tt>
<b>┣〖ℹ️ ᴠᴇɴᴅᴏʀ</b> ⇾<tt>{bin_info.get('brand', 'N/A')}</tt>
<b>┗━━━◆</b>
""")
        else:
            await aux.edit("🚫 BIN not recognized. Please enter a valid BIN.")
    except Exception as e:
        print(e)
        await aux.edit("❌ An error occurred while fetching BIN information.")

