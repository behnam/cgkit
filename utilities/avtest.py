#!/usr/bin/env python
# Test the ffmpeg/mediafile modules.

import sys, optparse, ctypes, time
from cgkit.ffmpeg import avformat, avcodec, avutil, swscale, decls
from cgkit import mediafile
try:
    import pygame
    pygame_available = True
except ImportError:
    pygame_available = False


def duration2str(duration, timeBase):
    duration = int(round(float(duration*timeBase)))
    h = duration/(60*60)
    min = (duration%(60*60))/60
    secs = duration%60
    return "%d:%02d:%02d"%(h,min,secs)
    
def displayInfo(fileNames):
    """Display information about the ffmpeg libs.
    """
    major,minor,micro = avformat.avformat_version()
    print ("avformat: %s.%s.%s \t(cgkit build: %s.%s.%s)"%(major,minor,micro, decls.LIBAVFORMAT_VERSION_MAJOR, decls.LIBAVFORMAT_VERSION_MINOR, decls.LIBAVFORMAT_VERSION_MICRO))
    major,minor,micro = avcodec.avcodec_version()
    print ("avcodec:  %s.%s.%s \t(cgkit build: %s.%s.%s)"%(major,minor,micro, decls.LIBAVCODEC_VERSION_MAJOR, decls.LIBAVCODEC_VERSION_MINOR, decls.LIBAVCODEC_VERSION_MICRO))
    major,minor,micro = avutil.avutil_version()
    print ("avutil:   %s.%s.%s \t(cgkit build: %s.%s.%s)"%(major,minor,micro, decls.LIBAVUTIL_VERSION_MAJOR, decls.LIBAVUTIL_VERSION_MINOR, decls.LIBAVUTIL_VERSION_MICRO))
    major,minor,micro = swscale.swscale_version()
    print ("swscale:  %s.%s.%s \t(cgkit build: %s.%s.%s)"%(major,minor,micro, decls.LIBSWSCALE_VERSION_MAJOR, decls.LIBSWSCALE_VERSION_MINOR, decls.LIBSWSCALE_VERSION_MICRO))
    print ("sizeof(AVFormatContext): %s"%ctypes.sizeof(decls.AVFormatContext))
    print ("sizeof(AVCodecContext): %s"%ctypes.sizeof(decls.AVCodecContext))
    print ("sizeof(AVPicture): %s"%ctypes.sizeof(decls.AVPicture))
    print ("sizeof(SwsContext): %s"%ctypes.sizeof(decls.SwsContext))
    
    for fileName in fileNames:
        print ("\n%s"%fileName)
        avfile = mediafile.open(fileName)
        for stream in avfile.videoStreams:
            res = "%sx%s"%(stream.width, stream.height)
            pixelAspect = stream.pixelAspect
            if pixelAspect is not None and pixelAspect!=1:
                res += " (%sx%s)"%(int(round(float(pixelAspect*stream.width))), stream.height)
            print ('  Video Stream: %s, %s, %gfps, %s, %gkbit/s, codec: "%s" (%s)'%(duration2str(stream.duration, stream.timeBase), res,
                                                                                    stream.frameRate,
                                                                                    avutil.av_get_pix_fmt_name(stream._codecCtx.pix_fmt),
                                                                                    round(stream.bitRate/1000),
                                                                                    stream.codecLongName, stream.codecName))
        for stream in avfile.audioStreams:
            print ('  Audio Stream: %s, %s channels, %sHz, %gkbit/s, codec: "%s" (%s)'%(duration2str(stream.duration, stream.timeBase),
                                                                                        stream.numChannels, stream.sampleRate,
                                                                                        round(stream.bitRate/1000.0), stream.codecLongName, stream.codecName))
#            print stream._codecCtx.sample_fmt
        avfile.close()

def readPackets(fileName):
    """Read the packets of the given file and print them.
    
    Uses the ffmpeg module directly.
    """
    avformat.av_register_all()
   
    # Open the file
    formatCtx = avformat.av_open_input_file(fileName, None, 0, None)
    
    # Fill the 'streams' fields...
    avformat.av_find_stream_info(formatCtx)

    # Get the AVInputFormat object
    inputFormat = formatCtx.iformat.contents
    print ("Format: %s (%s)"%(inputFormat.long_name, inputFormat.name))
    print ("Duration: %s min"%(formatCtx.duration/decls.AV_TIME_BASE/60))
    
    # Iterate over the streams
    videoIdx = None
    for i in range(formatCtx.nb_streams):
        stream = formatCtx.streams[i].contents
        codecCtx = stream.codec.contents
        v = codecCtx.codec_tag
        fourCC = "%s%s%s%s"%(chr(v&0xff), chr((v>>8)&0xff), chr((v>>16)&0xff), chr((v>>24)&0xff))
        if codecCtx.codec_type==decls.CODEC_TYPE_VIDEO:
            videoIdx = i
            print ("Stream %s: Video '%s', %sx%s"%(i,fourCC, codecCtx.width, codecCtx.height))
        elif codecCtx.codec_type==decls.CODEC_TYPE_AUDIO:
            print ("Stream %s: Audio '%s'"%(i,fourCC))
        else:
            print ("Stream %s: Other"%i)

    if videoIdx is not None:
        stream = formatCtx.streams[videoIdx].contents
        codecCtx = stream.codec.contents
        
        codec = avcodec.avcodec_find_decoder(codecCtx.codec_id)
        if codec is None:
            raise RuntimeError("Could not find decoder")
        
        print ("Video Codec: %s"%codec.long_name)
        
        # Open the codec
        avcodec.avcodec_open(codecCtx, codec)
        
        avcodec.avcodec_close(codecCtx)
    
    # Read the packets...
    pkt = decls.AVPacket()
    eof = False
    idx = 0
    while not eof:
        # Read the next frame packet...
        try:
            eof = not avformat.av_read_frame(formatCtx, pkt)
            if not eof:
                print ("Packet %s, stream_idx:%s, pts:%s, dts:%s, size:%s, duration:%s"%(idx,pkt.stream_index, pkt.pts,pkt.dts,pkt.size,pkt.duration))
                idx += 1
        finally:
            avcodec.av_free_packet(pkt)
    
    avformat.av_close_input_file(formatCtx)


def playVideo(fileName):
    vid = mediafile.open(fileName)
    print ("%s video streams, %s audio streams"%(vid.numVideoStreams(), vid.numAudioStreams()))
    if vid.numVideoStreams()==0:
        print ("No video stream found")
        return

    if not pygame_available:
        raise RuntimeError("pygame is not installed")

    pygame.init()
    
    stream = vid.videoStreams[0]
    print ("Video resolution: %sx%s"%(stream.width, stream.height))
    print (stream._codecCtx.time_base.num, stream._codecCtx.time_base.den)
    
    screen = pygame.display.set_mode((stream.width,stream.height))

    t1 = time.time()
    for i,data in enumerate(vid.iterData()):
        imgArr = data.numpyArray(pixelFormat=mediafile.RGB, colorAccess=mediafile.SEPARATE_CHANNELS)
#        img = data.pilImage()
        print ("frame %s - shape:%s strides:%s"%(i, imgArr.shape, imgArr.strides))
        pygame.surfarray.blit_array(screen, imgArr)

        pygame.display.flip()
#        if i==30:
#            break

    print "time:",time.time()-t1 

    exit_flag = False
    while not exit_flag:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_flag = True
            elif event.type==pygame.KEYDOWN:
                if event.key==27:
                    exit_flag = True

    vid.close()

def playAudio(fileName):
    avfile = mediafile.open(fileName)
    print ("%s video streams, %s audio streams"%(avfile.numVideoStreams(), avfile.numAudioStreams()))
    if avfile.numAudioStreams()==0:
        print ("No audio stream found")
        return

    if not pygame_available:
        raise RuntimeError("pygame is not installed")
    
    stream = avfile.audioStreams[0]
    print "%s channels, %sHz"%(stream.numChannels, stream.sampleRate)
    print stream._codecCtx.sample_fmt
    print "Duration",stream.duration
    
    # SEEK TEST
#    dstPos = stream.duration-400000000L
#    dstPos = 0
#    avformat.av_seek_frame(avfile._formatCtx, 0, ctypes.c_longlong(dstPos), 0)
    
    pygame.mixer.init(frequency=stream.sampleRate, channels=stream.numChannels)
    pygame.init()
    
    channel = pygame.mixer.Channel(0)
    channel.set_endevent(pygame.USEREVENT)
    
    bufSize = 100000
    buf = (bufSize*ctypes.c_short)()

    offset = 0
    exit_flag = False
    for i,data in enumerate(avfile.iterData([stream])):
#        print i, float(data.pts*stream.timeBase), float(stream.duration*stream.timeBase)
        size = data.sampleSize/2

        end = offset+size
        remaining = 0
        if end>bufSize:
            remaining = end-bufSize
            end = bufSize
        buf[offset:end] = data.samples[:end-offset]
        offset = end
        if end==bufSize:
            sound = pygame.mixer.Sound(buf)
            if channel.get_queue() is not None:
                # Wait until the queued sound is played...
                while 1:
                    evt = pygame.event.wait()
                    if evt.type==pygame.USEREVENT:
                        break
                    elif evt.type==pygame.KEYDOWN:
                        if evt.key==27:
                            exit_flag = True
                            break
                while channel.get_queue() is not None:
                    pass
            channel.queue(sound)
            offset = remaining
            buf[0:remaining] = data.samples[size-remaining:size]
            

        if exit_flag:
            break
        
#    sound = pygame.mixer.Sound(buf)
#    sound2 = pygame.mixer.Sound(buf)
#    channel.play(sound)
#    channel.queue(sound2)
    
    avfile.close()
    


############################################################################

def main():
    """Main function.
    """
    parser = optparse.OptionParser(usage="%prog [options] files")
    parser.add_option("-i", "--info", default=False, action="store_true", help="Display infos about ffmpeg libs")
    
    opts,args = parser.parse_args()
    
    if len(args)>0:
        fileName = args[0]
    else:
        fileName = None
    
    if opts.info:
        displayInfo(args)
        return 0
    else:
#        readPackets(fileName)
        playVideo(fileName)
#        playAudio(fileName)

############################################################################

ret = main()
sys.exit(ret)
