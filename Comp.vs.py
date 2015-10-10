import os,sys


#tools path
x264_path=sys.path[0]+"\\x264\\x264_64.exe"
bepipe_path=sys.path[0]+"\\BePipe\\BePipe.exe"
nero_path=sys.path[0]+"\\neroaac\\neroAacEnc.exe"
mp4box_path=sys.path[0]+"\\mp4box\\mp4box.exe"
ffms2_path=sys.path[0]+"\\ffms2\\ffms2.dll"
work_path=sys.path[0]



print("Input File: "+sys.argv[1]+"\n\r")
input_filetype=sys.argv[1].split(".")[-1]
print(input_filetype)



# AviSource frameserving
# vspath=work_path+"\\temp\\temp.avs"
# avsfile=open(vspath,"w+")
# avsfile.write("avisource(\""+sys.argv[1]+"\").changefps("+newfps+")")
# avsfile.close()



# VapourSynth Generate
vspath=work_path+"\\temp\\temp.vpy"
vsfile=open(vspath,"w+")
vsfile.write("import vapoursynth as vs\r\ncore = vs.get_core()\r\n")
vsfile.write("core.std.LoadPlugin(r\"C:\\avsplugins_x64\\ffms2.dll\")\r\n")
vsfile.write("ret = core.ffms2.Source(source=r\""+sys.argv[1]+"\")\r\n")
vsfile.write("ret = core.resize.Bicubic(ret, format=vs.YUV422P10)\r\nret.set_output()\r\nenable_v210 = True")
vsfile.close()



#Video Section
#x264 para
x264_preset="veryslow" # faster normal slow veryslow, lower the speed, higher the compress ratio
x264_bitrate="2450"    # kb/s  *time(seconds)/8/1024/1024=MB
x264_1passOutput="NUL" # one for no result while the other gets v2 for crf22
#x264_1passOutput="\""+work_path+"\\temp\\v2.mp4\""

#x264 automatic 2pass bitrate
#os.system(x264_path+" --pass 1 --stats \""+sys.path[0]+"\\temp\\temp.stats\" --level 5.1 --preset "+x264_preset+" --tune psnr --crf 22 --output "+x264_1passOutput+" \""+vspath+"\"")
#os.system(x264_path+" --pass 2 --stats \""+sys.path[0]+"\\temp\\temp.stats\" --level 5.1 --preset "+x264_preset+" --tune psnr --bitrate "+x264_bitrate+" --output \""+work_path+"\\temp\\v.mp4\" \""+vspath+"\"")
os.system("vspipe.exe \""+vspath+"\" --y4m - | \""+x264_path+"\" - --demuxer y4m --level 5.1 --preset "+x264_preset+" --tune psnr --crf 24 --deblock 1:1 --me tesa --vbv-bufsize 300000 --vbv-maxrate 300000 --psy-rd 0:0 -o \""+work_path+"\\temp\\v.mp4\"")



#Audio Section - neroaac
os.system(bepipe_path+" --script \"Import(^"+vspath+"^)\" | \""+nero_path+"\" -lc -cbr 96000 -if - -of "+work_path+"\\temp\\a.m4a\"")



#Muxing
os.system(mp4box_path+" -add \""+work_path+"\\temp\\v.mp4\" -add \""+work_path+"\\temp\\a.m4a\" \""+sys.argv[1]+".mp4\"")



#Finishing
os.system("del "+work_path+"\\temp\\*.* /q")
print("Finished.")
os.system("pause")
