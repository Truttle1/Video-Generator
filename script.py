import gensim
import yake
import nltk
from nltk import tokenize
from icrawler.builtin import BingImageCrawler
from gtts import gTTS
import os
import shutil
from PIL import Image
from random import randint
from mutagen.mp3 import MP3
import sys
from pydub import AudioSegment
          

print('gensim Version: %s' % (gensim.__version__))


f = open(sys.argv[1],"r")
text = f.read()
print(text)
content = tokenize.sent_tokenize(text)

language = "en"
max_ngram_size = 3
deduplication_threshold = .9
numOfKeywords = 1
extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)

count = 0
if(os.path.isdir("videoproj")):
    shutil.rmtree("videoproj")

os.mkdir("videoproj")


for i in content:
    
    google_crawler = BingImageCrawler(
        feeder_threads=1,
        parser_threads=2,
        downloader_threads=4,
        storage={'root_dir': "videoproj/" + str(count)})
        
    filters = dict(size='large')
    keywords = extractor.extract_keywords(i)
    
    if(len(keywords) > 0):
        print(keywords[0][0])
        google_crawler.crawl(keyword=keywords[0][0], filters=filters, max_num=8, file_idx_offset=0)
    else:
        print(i)
        google_crawler.crawl(keyword=i, filters=filters, max_num=8, file_idx_offset=0)
    
    found = False
    while(found == False):
        try:
            image = Image.open("videoproj/"+str(count)+"/00000"+str(randint(1,8))+".jpg");
            found = True
            break
        except:
            found = False


    image = image.resize((1280,720))
    image.save("videoproj/"+str(count)+"/image.jpg")
    
    tts = gTTS(i.replace("DinoWorld","Dino-World"),lang='en',tld='co.uk')
    #os.mkdir("videoproj/"+str(count))
    
    tts.save("videoproj/"+str(count) + "/line.mp3")
    stereo_audio = AudioSegment.from_file("videoproj/"+str(count) + "/line.mp3",format="mp3")
    mono_audios = stereo_audio.split_to_mono()
    mono_left = mono_audios[0].export("videoproj/"+str(count) + "/line.mp3",format="mp3")
    
    audio = MP3("videoproj/"+str(count) + "/line.mp3")
    
    frames = round(audio.info.length*15)
    os.mkdir("videoproj/"+str(count)+"/frames/")
    for _ in range(frames):
        image = image.crop((1,1,1279,719))
        image = image.resize((1280,720))
        image.save("videoproj/"+str(count)+"/frames/f"+str(_).zfill(6)+".jpg");
    
    os.system("ffmpeg -r 15 -f image2 -s 1280x720 -i videoproj/"+str(count)+"/frames/f%06d.jpg -vcodec libx264 -crf 25  -pix_fmt yuv420p videoproj/"+str(count)+"_nosound.mp4");
    os.system("ffmpeg -i videoproj/"+str(count)+"_nosound.mp4 -i videoproj/"+str(count)+"/line.mp3 -c:v copy -c:a aac videoproj/"+str(count)+".mp4")
    
    count += 1
    
    


f = open("videoproj/list.txt", "a")
for _ in range(count):
	f.write("file "+str(_)+".mp4'\n")

f.close()

music = randint(0,4)

os.system("ffmpeg -f concat -safe 0 -i videoproj/list.txt -c copy final.mp4")
os.system("ffmpeg -i music_use/"+str(music)+".wav -i final.mp4 -filter_complex \"[0:a][1:a]amerge,pan=stereo|c0<c0+c2|c1<c1+c3[out]\" -map 1:v -map \"[out]\" -c:v copy -shortest "+sys.argv[1]+"_stereo.mp4")
os.system("ffmpeg -i "+sys.argv[1]+"_stereo.mp4 -ac 1 "+sys.argv[1]+"_final.mp4")
os.system("rm final.mp4")