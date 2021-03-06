#!/usr/bin/python
# coding: utf-8

import os
import ctypes
import cv2
from glob import iglob

this_dir = os.path.dirname(__file__)

DLL_PATH = os.path.join(this_dir,'lib', 'libtesseract.so' )
TESSDATA_PREFIX = os.path.join(this_dir,'tessdata' )
lang = 'chi_sim+eng'
# lang = 'eng'

tesseract = ctypes.cdll.LoadLibrary(DLL_PATH)
tesseract.TessBaseAPICreate.restype = ctypes.c_uint64   #由于系统为64位,这里类型需指明为c_uint64
api = tesseract.TessBaseAPICreate()
def tessInit():
    rc = tesseract.TessBaseAPIInit3(ctypes.c_uint64(api), TESSDATA_PREFIX, lang)
    if rc:
        tesseract.TessBaseAPIDelete(ctypes.c_uint64(api))
        print('Could not initialize tesseract.\n')
        exit(3)

def tessRecognitionFromFile(img_name):
    tesseract.TessBaseAPIProcessPages(
        ctypes.c_uint64(api), img_name, None, 0, None)
    tesseract.TessBaseAPIGetUTF8Text.restype = ctypes.c_uint64
    text_out = tesseract.TessBaseAPIGetUTF8Text(ctypes.c_uint64(api))
    return ctypes.string_at(text_out)

def cleanup(temp_name):
    ''' Tries to remove files by filename wildcard path. '''
    for filename in iglob(temp_name + '*' if temp_name else temp_name):
        try:
            os.remove(filename)
        except OSError:
            pass

def tessRecognition(img, tmp_dir):
    img_name = os.path.join(tmp_dir, 'img.png')
    cv2.imwrite(img_name, img)
    text_out = tessRecognitionFromFile(img_name)
    cleanup(img_name)
    return text_out

# def from_file(path):
#     tesseract.TessBaseAPIProcessPages(
#         ctypes.c_uint64(api), path, None, 0, None)
#     tesseract.TessBaseAPIGetUTF8Text.restype = ctypes.c_uint64
#     text_out = tesseract.TessBaseAPIGetUTF8Text(ctypes.c_uint64(api))
#     return ctypes.string_at(text_out)

if __name__ == '__main__':
    image_file_path = b'/home/cvrsg/JpHu/TestGround/tesseract/build/bin/pics/1.png'
    # result = from_file(image_file_path)
    tessInit()
    result = tessRecognition(image_file_path)
    print(result)





# lang = "eng"
# filename = "/home/cvrsg/JpHu/TestGround/tesseract/testing/eurotext.tif"
# libname = "/home/cvrsg/JpHu/TestGround/tesseract/build/libtesseract.so.4.0.0"
# #TESSDATA_PREFIX = os.environ.get('TESSDATA_PREFIX')
# #if not TESSDATA_PREFIX:
# TESSDATA_PREFIX = "/home/cvrsg/JpHu/TestGround/MingPaiProject/tesseract/tessdata/"
#
# tesseract = ctypes.cdll.LoadLibrary(libname)
# tesseract.TessVersion.restype = ctypes.c_char_p
# tesseract_version = tesseract.TessVersion()
# api = tesseract.TessBaseAPICreate()
# rc = tesseract.TessBaseAPIInit3(api, TESSDATA_PREFIX, lang)
# if (rc):
#     tesseract.TessBaseAPIDelete(api)
#     print("Could not initialize tesseract.\n")
#     exit(3)
#
# text_out = tesseract.TessBaseAPIProcessPages(api, filename, None, 0)
# result_text = ctypes.string_at(text_out)
#
# print 'Tesseract-ocr version', tesseract_version
# print result_text


# import os
# import cffi  # requires "pip install cffi"
#
# this_dir = os.path.dirname(__file__)
# PATH_TO_LIBTESS = os.path.join(this_dir, 'lib', 'libtesseract.so') #'/path/to/development/libtesseract.so'
#
#
# ffi = cffi.FFI()
# ffi.cdef("""
# struct Pix;
# typedef struct Pix PIX;
# PIX * pixRead (const char *filename);
# char * getLeptonicaVersion ();
#
# typedef struct TessBaseAPI TessBaseAPI;
# typedef int BOOL;
#
# const char* TessVersion();
#
# TessBaseAPI* TessBaseAPICreate();
# int TessBaseAPIInit3(TessBaseAPI* handle, const char* datapath, const char* language);
#
# void TessBaseAPISetImage2(TessBaseAPI* handle, struct Pix* pix);
#
# BOOL   TessBaseAPIDetectOrientationScript(TessBaseAPI* handle, char** best_script_name,
#                                                             int* best_orientation_deg, float* script_confidence,
#                                                             float* orientation_confidence);
# """)
#
# libtess = ffi.dlopen(PATH_TO_LIBTESS)
# from ctypes.util import find_library
# liblept = ffi.dlopen(find_library('lept'))
#
# ffi.string(libtess.TessVersion())
#
# ffi.string(liblept.getLeptonicaVersion())
#
# api = libtess.TessBaseAPICreate()
#
# def tessInit():
#     #data_path = os.path.join(this_dir, 'tessdata')
#     data_path = ffi.new('char []', '/home/cvrsg/JpHu/TestGround/MingPaiProject/tesseract/tessdata')
#     lang = ffi.new('char []', 'chi_sim')
#     #libtess.TessBaseAPIInit3(api, ffi.NULL, ffi.NULL)
#     libtess.TessBaseAPIInit3(api, data_path, lang)
#
# def tessRecognition(img_name):
#     pix = liblept.pixRead(img_name)
#     libtess.TessBaseAPISetImage2(api, pix)
#
#     script_name = ffi.new('char **')
#     orient_deg = ffi.new('int *')
#     script_conf = ffi.new('float *')
#     orient_conf = ffi.new('float *')
#     libtess.TessBaseAPIDetectOrientationScript(api, script_name, orient_deg, script_conf, orient_conf)
#
#     print(script_name[0])
#     print(orient_deg[0])
#     print(script_conf[0])
#     print(orient_conf[0])
