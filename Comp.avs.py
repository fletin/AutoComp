# ver 1.01
# .supports multitask simultaneously
import os,sys
import uuid


#Generate uuid to make sure filename unique
task_uuid=str(uuid.uuid1())

#tools path
x264_path=sys.path[0]+"\\x264\\x264.exe"
ffms2_path=sys.path[0]+"\\ffms2\\ffms2.dll"
bepipe_path=sys.path[0]+"\\BePipe\\BePipe.exe"
nero_path=sys.path[0]+"\\neroaac\\neroAacEnc.exe"
mp4box_path=sys.path[0]+"\\mp4box\\mp4box.exe"
work_path=sys.path[0]

#avs filters
newfps=0
newx=848
newy=480

#x264 para
x264_preset="veryslow" # faster normal slow veryslow, lower the speed, higher the compress ratio
x264_bitrate="2000"    # kb/s  *time(seconds)/8/1024/1024=MB
#x264_1passOutput="NUL" # one for no result while the other gets v2 for crf22
x264_1passOutput="\""+work_path+"\\temp\\"+task_uuid+".v.mp4\""
crf_value=24



# ffmpegsource2 function
ffms2_script="""function FFmpegSource2(string source, int "vtrack", int "atrack", bool "cache", \\
	string "cachefile", int "fpsnum", int "fpsden", int "threads", \\
	string "timecodes", int "seekmode", bool "overwrite", int "width", int "height", \\
	string "resizer", string "colorspace", int "rffmode", int "adjustdelay", \\
	bool "utf8", string "varprefix") {
	
	vtrack 		= default(vtrack,-1)
	atrack		= default(atrack,-2)
	cache		= default(cache,true)
	cachefile	= default(cachefile,source+".ffindex")
	fpsnum		= default(fpsnum,-1)
	fpsden		= default(fpsden,1)
	threads		= default(threads,-1)
	timecodes	= default(timecodes,"")
	seekmode	= default(seekmode,1)
	overwrite	= default(overwrite,false)
	width		= default(width,-1)
	height		= default(height,-1)
	resizer		= default(resizer,"BICUBIC")
	colorspace	= default(colorspace,"")
	rffmode		= default(rffmode,0)
	adjustdelay	= default(adjustdelay,-1)
	utf8		= default(utf8,false)
	varprefix	= default(varprefix, "")
	
	((cache == true) && (atrack <= -2)) ? ffindex(source=source, cachefile=cachefile, \\
		indexmask=0, overwrite=overwrite, utf8=utf8) : (cache == true) ? ffindex(source=source, \\
		cachefile=cachefile, indexmask=-1, overwrite=overwrite, utf8=utf8) : nop
	
	v = ffvideosource(source=source, track=vtrack, cache=cache, cachefile=cachefile, \\
		fpsnum=fpsnum, fpsden=fpsden, threads=threads, timecodes=timecodes, \\
		seekmode=seekmode, rffmode=rffmode, width=width, height=height, resizer=resizer, \\
		colorspace=colorspace, utf8=utf8, varprefix=varprefix)
	
	a = (atrack <= -2) ? blankclip(audio_rate=0) : ffaudiosource(source=source, \\
		track=atrack, cache=cache, cachefile=cachefile, adjustdelay=adjustdelay, \\
		utf8=utf8, varprefix=varprefix)
	
	return audiodubex(v,a)
}"""











print("Input File: "+sys.argv[1]+"\n\r")



#AviSource frameserving
avspath=""
ext_name=sys.argv[1].split(".")[-1]
if ext_name.upper()=="AVS":
	avspath=sys.argv[1]
else:
	avspath=work_path+"\\temp\\"+task_uuid+".avs"
	avsfile=open(avspath,"w+")

	if ext_name.upper()=="AVI":
		avsfile.write("AviSource(\""+sys.argv[1]+"\")\r\n")
	else:
		#avsfile.write("LoadPlugin(\""+ffms2_path+"\")\r\nAudioDub(FFVideoSource(\""+sys.argv[1]+"\"), FFAudioSource(\""+sys.argv[1]+"\"))\r\n")
		avsfile.write(ffms2_script+"\r\n\r\n\r\n")
		avsfile.write("LoadPlugin(\""+ffms2_path+"\")\r\nFFmpegSource2(\""+sys.argv[1]+"\")\r\n")

	if newfps>0:
		if newfps>20:
			avsfile.write("convertfps("+str(newfps)+")\r\n")
		else:
			avsfile.write("changefps("+str(newfps)+")\r\n")

	if (newx>0) & (newy>0):
		avsfile.write("lanczosresize("+str(newx)+","+str(newy)+")\r\n")

	avsfile.write("ConvertToYUY2()")
	avsfile.close()



#Video Section
#x264
os.system(x264_path+" --pass 1 --stats \""+sys.path[0]+"\\temp\\"+task_uuid+".stats\" --level 5.1 --preset "+x264_preset+" --tune psnr --crf "+str(crf_value)+" --output "+x264_1passOutput+" \""+avspath+"\"")
#os.system(x264_path+" --pass 2 --stats \""+sys.path[0]+"\\temp\\temp.stats\" --level 5.1 --preset "+x264_preset+" --tune psnr --bitrate "+x264_bitrate+" --output \""+work_path+"\\temp\\v.mp4\" \""+avspath+"\"")


#Audio Section - neroaac
os.system(bepipe_path+" --script \"Import(^"+avspath+"^)\" | \""+nero_path+"\" -lc -cbr 96000 -if - -of "+work_path+"\\temp\\"+task_uuid+".a.m4a\"")


#Muxing
os.system(mp4box_path+" -add \""+work_path+"\\temp\\"+task_uuid+".v.mp4\" -add \""+work_path+"\\temp\\"+task_uuid+".a.m4a\" \""+sys.argv[1]+".mp4\"")



#Finishing

print("Finished.")
os.system("pause")
os.system("del "+work_path+"\\temp\\*.* /q")

