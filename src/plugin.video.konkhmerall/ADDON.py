import urllib,urllib2,re
import os,sys
import base64
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui,xbmc
import json #For VIMEO
PLUGIN = xbmcaddon.Addon(id='plugin.video.konkhmerall')
addon_name = 'plugin.video.konkhmerall'
KONKHMER ='http://www.khmer6.com/'
USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1"
datapath = xbmc.translatePath('special://profile/addon_data/'+addon_name)
#cookiejar = os.path.join(datapath,'khmerstream.lwp')
ADDON_PATH = PLUGIN.getAddonInfo('path')
#append lib directory
sys.path.append( os.path.join( ADDON_PATH, 'resources', 'lib' ) )
from net import Net
from bs4 import BeautifulSoup
import CommonFunctions #For VIMEO
common = CommonFunctions
net = Net()

pluginhandle = int(sys.argv[1])

# example of how to get path to an image

JolchetImage = os.path.join(ADDON_PATH, 'resources', 'images','KonKhmer.png')
fanart = os.path.join(ADDON_PATH, 'resources', 'images','Angkor4.jpg')
def OpenURL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link 

def OpenSoup(url):
    req = urllib2.Request(url)
    req.add_unredirected_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0')
    response = urllib2.urlopen(req).read()
    return response

	
def HOME():####MODE===20
		addDir('Chinese Series',KONKHMER+'search/label/China%20Drama',21,'https://3.bp.blogspot.com/-OaCjFHjf8tU/VwtmwXS8h8I/AAAAAAAABLs/M4jW6P-IfMUff4-AW83lP8X0KYMY1BTAw/s227/AAA.png')
		addDir('Chinese Movie',KONKHMER+'search/label/China%20Movie',21,'https://3.bp.blogspot.com/-BPBp2ZHJSqY/VsfmZXfkVDI/AAAAAAAACpc/bl0n9dFSQQ0/s227/KKA02.jpg')
		addDir('Thai Lakorn',KONKHMER+'search/label/Thai%20Drama',21,'https://3.bp.blogspot.com/-DKHlKn0YxjA/Vwj7aH6faSI/AAAAAAAADJw/td7U4plYycgWhTU93Y0uTBE0ZwioDz3HQ/s227/BM42.png')
		addDir('Khmer Movie',KONKHMER+'search/label/Khmer%20Movie',21,'http://4.bp.blogspot.com/-ef9oN0E_YYs/VfQRt6d8MKI/AAAAAAAAAYA/tRfH3QWlub0/s227/Tek%2BChet%2BOv%2BPuk.jpg')
		
		xbmcplugin.endOfDirectory(pluginhandle)
		
def INDEX_J(url):     
        link = OpenURL(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        #match=re.compile('<h2 class=\'post-title entry-title index\' itemprop=\'name headline\'>\n<a href=\'(.+?)\' itemprop=\'url\'>(.+?)</a>\n</h2>\n<meta content=\'(.+?)\' itemprop=\'image_url\'/>').findall(link)
        match=re.compile('<h2 class=\'post-title entry-title\' itemprop=\'name headline\'>\n<a href=\'(.+?)\' itemprop=\'url\'>(.+?)</a>\n</h2>').findall(link)
        for vurl,vname in match:
            addDir(vname,vurl,25,'')
        #match5=re.compile('<div class=\'loadingpost\'></div>\n<div class=\'blog-pager\' id=\'blog-pager\'>\n([^"]+?)\n</div>').findall(link)
        #if(len(match5)):
        pages=re.compile('<span id=\'.+?\'>\n<a class=\'.+?\' href=\'([^"]+?)\' id=\'.+?\' title=\'.+?\'>(.+?)</a>\n</span>').findall(link)
        for pageurl,pagenum in pages:
               addDir("[B][COLOR blue]<<<%s>>>[/B][/COLOR]"% pagenum,pageurl,21,"")                        
        xbmcplugin.endOfDirectory(pluginhandle)
 
def EPISODE_J(url,name):    
        link = OpenURL(url)
        #addLink(name.encode("utf-8"),url,3,'')
        #match=re.compile('{\s*"file":\s*"(.+?)",\s*"title":\s*"(.+?)",\s*"image":\s*"(.+?)"').findall(link)   		
        match=re.compile('{\s*"file":\s*"(.+?)",\s*"title":\s*"(.+?)",\s*"description": "",\s*"image":\s*"(.+?)"').findall(link)		
        if(len(match) > 0):      
         for vLink,vLinkName,vImage in match:                 
          addLink(vLinkName,vLink,4,vImage)
        else: 
         match=re.compile('<li class="v-item active" data-source=".+?" data-vid="(.+?)">').findall(link)
         if(len(match) > 0):
           counter = 0      
           for vLink in match:
               counter += 1 
               addLink(name.encode("utf-8") + " part " + str(counter),('https://vid.me/e/'+ vLink),4,'')
         else:
          match=re.compile(' playlist: "(.+?)",').findall(link)
          if(len(match) > 0):
           List = (urllib2.unquote(match[0]).decode("utf8"))
           link = OpenURL(List)
           OpenXML(link)
          else: 
           match=re.compile('<li class="v-item " data-vid="(.+?)">').findall(link)
           if(len(match) > 0):
            counter = 0      
            for vLink in match:
               counter += 1 
               addLink(name.encode("utf-8") + " part " + str(counter),('http://www.mp4upload.com/embed-%s.html'% vLink),4,'')
           #else:
             #addLink(name,url,3,'')		  
           else:
            match=re.compile('{\s*"file":\s*"(.+?)",\s*"title":\s*"(.+?)",\s*"description":\s*".+?",\s*"image":\s*"(.+?)"').findall(link)
            if(len(match)>0):
             for vLink,vLinkName,vImage in match:
              addLink(vLinkName,vLink,4,vImage)  		  
		  
        xbmcplugin.endOfDirectory(pluginhandle)
		
def OpenXML(Doc):
    document = xml.dom.minidom.parseString(Doc)      
    items = document.getElementsByTagName('item')
    for itemXML in items:
     vname=itemXML.getElementsByTagName('title')[0].childNodes[0].data
     vpart=itemXML.getElementsByTagName('description')[0].childNodes[0].data
     vImage=itemXML.getElementsByTagName('jwplayer:image')[0].childNodes[0].data
     vurl=itemXML.getElementsByTagName('jwplayer:source')[0].getAttribute('file')     
     addLink(vpart.encode("utf-8"),vurl.encode("utf-8"),4,"")           
############## END JOLCHET ****************** 

def VIDEOLINKS(url):       
           
           link=OpenNET(url)
           url = re.compile('Base64.decode\("(.+?)"\)').findall(link)
           if(len(url) > 0):
            host=url[0].decode('base-64')
            match=re.compile('<iframe frameborder="0" [^>]*src="(.+?)"[^>]*>').findall(host)[0]
            VIDEO_HOSTING(match)
            #Play_VIDEO(match)
           else:
           #match=re.compile("'file': '(.+?)',").findall(link)
            match=re.compile('<IFRAME SRC="\r\n(.+?)" [^>]*').findall(link)
            if(len(match) == 0):
             match=re.compile('file:\s*"([^"]+?)"').findall(link)# Good Link
             if(len(match) == 0):
                match=re.compile('<iframe frameborder="0" [^>]*src="(.+?)">').findall(link)
                if(len(match)==0):
                 match=re.compile('<IFRAME SRC="(.+?)" [^>]*').findall(link)
                 if(len(match) == 0):   
                   #match=re.compile('<iframe src="(.+?)" [^>]*').findall(link)
                   match=re.compile("'file': '(.+?)',").findall(link)
                   if(len(match) == 0):
                    match=re.compile('<div class="video_main">\s*<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
                    if(len(match) == 0):
                     match = re.compile("var flashvars = {file: '(.+?)',").findall(link)        
                     if(len(match) == 0):       
                      match = re.compile('swfobject\.embedSWF\("(.+?)",').findall(link)
                      if(len(match) == 0):
                       match = re.compile("'file':\s*'(.+?)'").findall(link)
                       if(len(match) == 0):                    
                        match = re.compile('<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
                        if(len(match)== 0):
                         match = re.compile('<source [^>]*src="([^"]+?)"').findall(link)
                         if(len(match) == 0):                    
                          match = re.compile('<script>\nvidId = \'(.+?)\'; \n</script>').findall(link)
                          for url in match:
                           vid = url[0].replace("['']", "")       
                           match ='https://docs.google.com/file/d/'+ (vid)+'/preview'
                           REAL_VIDEO_HOST(match)
                           print match
           VIDEO_HOSTING(match[0])
           xbmcplugin.endOfDirectory(pluginhandle)
   
def VIDEO_HOSTING(vlink):
          
           if 'dailymotion' in vlink:                
                VideoURL = DAILYMOTION(vlink)
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Dailymotion Loading selected video)")
                Play_VIDEO(VideoURL)
           elif 'facebook.com' in vlink:   
                VideoURL = FACEBOOK(vlink)
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Facebook Loading selected video)")
                Play_VIDEO(VideoURL)
                
           elif 'google.com' in vlink:   
                VideoURL = DOCS_GOOGLE(vlink)
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Google Loading selected video)")
                Play_VIDEO(VideoURL)
                
           elif 'vimeo' in vlink:
                 VideoURL = VIMEO(vlink)
                 print 'VideoURL: %s' % VideoURL
                 xbmc.executebuiltin("XBMC.Notification(Please Wait!,Vimeo Loading selected video)")
                 Play_VIDEO(VideoURL)

           elif 'vid.me' in vlink:                   
                VideoURL = VIDDME(vlink)
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Vid.me Loading selected video)")
                Play_VIDEO(VideoURL)
           elif 'sendvid.com' in vlink:
                VideoURL = SENDVID(vlink)
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Sendvid Loading selected video)")
                Play_VIDEO(VideoURL)
           elif 'viddme' in vlink:
                VideoURL = vlink
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Viddme Loading selected video)")
                Play_VIDEO(VideoURL)

           elif 'az665436' in vlink:
                VideoURL = vlink
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,AZ Loading selected video)")
                Play_VIDEO(VideoURL)

           elif 'd1wst0behutosd' in vlink:
                #link = OpenURL(vlink)   
                VideoURL = vlink
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,d1wst0behutosd Loading selected video)")
                Play_VIDEO(urllib2.unquote(VideoURL).decode("utf8"))# MP4
           #     Play_VIDEO(VideoURL)

           elif 'mp4upload.com' in vlink:
                VideoURL = MP4UPLOAD(vlink)
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,MP4UPLOAD Loading selected video)")
                Play_VIDEO(VideoURL)
           elif 'videobam' in vlink:  
                VideoURL = VIDEOBAM(vlink)
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Videobam Loading selected video)")                                
                Play_VIDEO(VideoURL)     

           elif 'sharevids.net' in vlink:
                VideoURL = vlink
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Sharevids Loading selected video)")
                Play_VIDEO(VideoURL)   
                    # d = xbmcgui.Dialog()
                    # d.ok('Not Implemented','Sorry videos on linksend.net does not work','Site seem to not exist')                
           elif 'videos4share.com' in vlink:
                VideoURL = vlink
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,videos4share Loading selected video)")
                #Play_VIDEO(VideoURL)
                Play_VIDEO(urllib2.unquote(VideoURL).decode("utf8"))# MP4
           elif 'youtu.be' in vlink:                   
                VideoURL = YOUTUBE(vlink)
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Youtube Loading selected video)")            
                Play_VIDEO(VideoURL)     

           elif 'youtube' in vlink:                   
                VideoURL = YOUTUBE(vlink)
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Youtube Loading selected video)")
                Play_VIDEO(VideoURL)
           else:
                #if 'grayshare.net' in vlink:
                if 'share.net' in vlink:    
                    VideoURL = vlink
                    print 'VideoURL: %s' % VideoURL
                    Play_VIDEO(urllib2.unquote(VideoURL).decode("utf8"))    
                      # d = xbmcgui.Dialog()
                      # d.ok('Not Implemented','Sorry videos on linksend.net does not work','Site seem to not exist')                
               
                else:
                    print 'VideoURL: %s' % vlink
                    xbmc.executebuiltin("XBMC.Notification(Please Wait!,Let Try to Play These Video)")
                    Play_VIDEO(urllib2.unquote(vlink).decode("utf8"))
                    #VideoURL = urlresolver.HostedMediaFile(url=vlink).resolve()
                    #Play_VIDEO(VideoURL)

def OpenNET(url):
    try:
       net = Net(cookie_file=cookiejar)
       #net = Net(cookiejar)
       try:
            second_response = net.http_GET(url)
       except:
            second_response = net.http_GET(url.encode("utf-8"))
       return second_response.content
    except:
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')
	

def Play_VIDEO(VideoURL):

    print 'PLAY VIDEO: %s' % VideoURL    
    item = xbmcgui.ListItem(path=VideoURL)
    return xbmcplugin.setResolvedUrl(pluginhandle, True, item)

###################### Resolver Start  ###################
def DAILYMOTION(SID):
        match=re.compile('(dailymotion\.com\/(watch\?(.*&)?v=|(embed|v|user|video)\/))([^\?&"\'>]+)').findall(SID)                
        SID = match[0][len(match[0])-1]
        vlink = 'http://www.dailymotion.com/embed/' + str(SID)
        link = OpenURL(vlink)
        matchFullHD = re.compile('"1080":.+?"url":"(.+?)"', re.DOTALL).findall(link)
        matchHD = re.compile('"720":.+?"url":"(.+?)"', re.DOTALL).findall(link)
        matchHQ = re.compile('"480":.+?"url":"(.+?)"', re.DOTALL).findall(link)
        matchSD = re.compile('"380":.+?"url":"(.+?)"', re.DOTALL).findall(link)
        matchLD = re.compile('"240":.+?"url":"(.+?)"', re.DOTALL).findall(link)
        if matchFullHD:
            VideoURL = urllib.unquote_plus(matchFullHD[0]).replace("\\", "/")
        elif matchHD:
            VideoURL = urllib.unquote_plus(matchHD[0]).replace("\\/", "/")
        elif matchHQ:
            VideoURL = urllib.unquote_plus(matchHQ[0]).replace("\\/", "/")
        elif matchSD:
            VideoURL = urllib.unquote_plus(matchSD[0]).replace("\\/", "/")
        elif matchLD:
            VideoURL = urllib.unquote_plus(matchLD[0]).replace("\\/", "/")
        return VideoURL

def DOCS_GOOGLE(Video_ID):
        req = urllib2.Request(Video_ID)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.3')
        response = urllib2.urlopen(req)
        link=response.read()
        #print 'VIDEO Link: %s' % link  
        response.close()
        vlink = 'https://docs.google.com/file/'+str(link)+ '?pli=1'
        stream_map= re.compile('fmt_stream_map","(.+?)"').findall(vlink)[0].replace("\/", "/")
       # stream_map= re.compile('fmt_stream_map":"(.+?)"').findall(vlink)[0].replace("\/", "/")
        formatArray = stream_map.split(',')
        for formatContent in formatArray:
            formatContentInfo = formatContent.split('|')
            qual = formatContentInfo[0]
           # VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            if(qual == '120'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '46'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '45'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '38'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '37'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '22'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '35'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '18'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '44'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '43'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '59'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '6'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '34'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '5'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '36'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            else:
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')     
        return VideoURL  

def FACEBOOK (SID):
       req = urllib2.Request(SID)
       req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.3')
       response = urllib2.urlopen(req)
       link=response.read()
       response.close()
       #vlink = 'http://www.facebook.com/video/video.php?v=' + str(link)
       vlink = re.compile('"params","([\w\%\-\.\\\]+)').findall(link)[0]
       html = urllib.unquote(vlink.replace('\u0025', '%')).decode('utf-8')
       html = html.replace('\\', '')
       videoUrl = re.compile('(?:hd_src|sd_src)\":\"([\w\-\.\_\/\&\=\:\?]+)').findall(html)
       if len(videoUrl) > 0:    
           VideoURL =  videoUrl[0]
       else:
           VideoURL =  videoUrl
       return  VideoURL  

def MP4UPLOAD(SID):
       req = urllib2.Request(SID)
       req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.3')
       response = urllib2.urlopen(req)
       link=response.read()
       response.close()    
       VideoURL=re.compile('\'file\': \'(.+?)\'').findall(link)[0]
       return VideoURL

def SENDVID(SID):
        #Video_ID = urllib.unquote_plus(SID).replace("//", "http://")
        VID = urllib2.unquote(SID).replace("//", "http://")
        req = urllib2.Request(VID)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match = re.compile('<source src="([^"]+?)"').findall(link)
        #match = re.compile('<meta property="og:video:secure_url" content="([^"]+?)"').findall(link)
        #VideoURL = (match[0]).decode("utf-8")
        VideoURL =  urllib2.unquote(match[0]).replace("//", "http://")
        return VideoURL

def VIDDME(Video_ID):
        #req = urllib2.Request(Video_ID)
        #req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.3')
        #response = urllib2.urlopen(req)
        #link=response.read()
        #response.close()
        #match = re.compile('"(https://vid.me/[^"]+)"').findall(link)
       #for Video_ID in match:
            req = urllib2.Request(Video_ID)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.3')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()    
            #VideoURL=re.compile('<source src="([^"]+?)"').findall(link)
            match = re.compile('<source src="([^"]+mp4[^"]+)"').findall(link)
            for URL in match:
                VideoURL =urllib2.unquote(URL).replace('&amp;','&')
            return VideoURL       

def VIDEOBAM(Video_ID):        
        req = urllib2.Request(Video_ID)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()               
        match=re.compile('"url"\s*:\s*"(.+?)","').findall(link)               
        for URL in match:
            if(URL.find("mp4") > -1):
               VideoURL = URL.replace("\\","")
        return VideoURL       

def VIMEO(Video_ID):
        HomeURL = ("http://"+Video_ID.split('/')[2])
        if 'player' in Video_ID:
            vlink =re.compile("//player.vimeo.com/video/(.+?)\?").findall(Video_ID+'?')
        elif 'vimeo' in Video_ID:
              vlink =re.compile("//vimeo.com/(.+?)\?").findall(Video_ID+'?')
        result = common.fetchPage({"link": "http://player.vimeo.com/video/%s/config?type=moogaloop&referrer=&player_url=player.vimeo.com&v=1.0.0&cdn_url=http://a.vimeocdn.com" % vlink[0],"refering": HomeURL})
        print 'Resultcommon: %s' % result
        collection = {}
        if result["status"] == 200:
            html = result["content"]
            print 'HTMLresult: %s' % html
            collection = json.loads(html)
            print 'COLLcommon: %s' % collection
            #codec = collection["request"]["files"]["codecs"][0]
            #video = collection["request"]["files"][codec]
            video = collection["request"]["files"]["progressive"]
            print 'VideoColl: %s' % video
            #if video.get("hd"):
            if(len(video) > 2):    
               #VideoURL = video['hd']['url']
               VideoURL = video[2]['url']
               print 'VideoSD: %s' % VideoURL
            else: 
               #VideoURL = video['sd']['url']
               VideoURL = video[0]['url']
               print 'VideoLD: %s' % VideoURL
        return VideoURL
def VIMEO1(Video_ID):
        HomeURL = ("http://"+Video_ID.split('/')[2])
        if 'player' in Video_ID:
            vlink =re.compile("//player.vimeo.com/video/(.+?)\?").findall(Video_ID+'?')
        elif 'vimeo' in Video_ID:
              vlink =re.compile("//vimeo.com/(.+?)\?").findall(Video_ID+'?')
        #result = common.fetchPage({"link": "http://player.vimeo.com/video/%s/config?type=moogaloop&referrer=&player_url=player.vimeo.com&v=1.0.0&cdn_url=http://a.vimeocdn.com" % vlink[0],"refering": HomeURL})
        result = common.fetchPage({"link": "http://player.vimeo.com/video/%s?title=0&byline=0&portrait=0" % vlink[0],"refering": HomeURL})        
        print 'Result: %s' % result
        collection = {}
        if result["status"] == 200:
            html = result["content"]
            html = html[html.find('={"cdn_url"')+1:]
            html = html[:html.find('}};')]+"}}"
            #print html
            collection = json.loads(html)
            print 'Collection: %s' %collection
            #codec = collection["request"]["files"]["codecs"][0]
            #print codec            
            video = collection["request"]["files"]["progressive"]#[0]
            #isHD = collection["request"]["files"][video]
            print 'VideoCOLL1: %s' % video
            if(len(video) > 2):
            #if video.get("720p"):
                VideoURL = video[2]['url']
                print 'VideoSD: %s' % VideoURL
            #elif(len(video) > 1):
            #    VideoURL = video[1]['url']
            #    print 'VideoSD: %s' % VideoURL
            else: 
               VideoURL = video[0]['url']
               print 'VideoLD: %s' % VideoURL
        return VideoURL
def YOUTUBE(SID):
        match=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(SID)
        if(len(match) > 0):
             URL = match[0][len(match[0])-1].replace('v/','')
        else:   
             match = re.compile('([^\?&"\'>]+)').findall(SID)
             URL = match[1].replace('v=','')
        VideoURL = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' +URL.replace('?','')     
        return VideoURL
###################### Resolver End  ###################        
def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultImage", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
		
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="https://scontent.xx.fbcdn.net/hprofile-xtp1/v/t1.0-1/p160x160/12938085_1871469499746640_4241685066872276999_n.jpg?oh=9c3a0e13803dda361d97919a3291c6c2&oe=57BFECBB", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param    



params=get_params()
url=None
name=None
mode=None
play=None
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass	

		
sysarg=str(sys.argv[1]) 
if mode==None or url==None or len(url)<1:
        #OtherContent()
        HOME()
elif mode==3:
        VIDEOLINKS(url)
elif mode==4:
        VIDEO_HOSTING(url)
        
elif mode==10:
        MERLKONS()
elif mode==11:
        print ""+url
        INDEX_MERLKON(url)       
elif mode==12:
        INDEX_KHMERSTREAM(url)
elif mode==13:
        INDEX_KHMERAVE(url)
elif mode==15:
        EPISODE_MERLKON(url,name)

elif mode==20:
        JOLCHET()
elif mode==21:
        INDEX_J(url)
elif mode==23:
        INDEX_JJ(url)        
elif mode==22:
        MOVIE_J(url)
elif mode==25:
        EPISODE_J(url,name)
elif mode==26:
        EPISODE_MOVIEJ(url,name)

elif mode==30:
        VIDEO4YOU()
elif mode==31:
        INDEX_VIDEO4U(url)
elif mode==35:
        EPISODE_VIDEO4U(url,name)

elif mode==40:
        FILM2US()
elif mode==41:
        INDEX_FILM2US(url)        
elif mode==45:
        EPISODE_FILM2US(url)
elif mode==50:
        KHDRAMA2()
elif mode==51:
        INDEX_KHDRAMA(url)
elif mode==55:
        EPISODE_KHDRAMA(url,name)
elif mode==80:
        K8MERHD()
elif mode==81:
        INDEX_K8MERHD(url)
elif mode==85:
        EPISODE_K8MERHD(url,name)
elif mode==110:
        MUSIC_MENU(url,name)
elif mode==111:
        MUSIC_VIDEO(url)
elif mode==115:
        MUSIC_EP(url,name)       
elif mode==100:
        PLAYLIST_VIDEOLINKS(url)

elif mode==120:
        KHMERLOVES_MENU(url)
elif mode==121:
        INDEX_KHMERLOVES(url)
elif mode==125:
        EPISODE_KHMERLOVES(url,name)        
xbmcplugin.endOfDirectory(int(sysarg))
        
