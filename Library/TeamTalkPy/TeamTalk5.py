from ctypes import *
import sys
from time import sleep
from enum import IntEnum

dll = cdll.TeamTalk5

if sys.platform == "win32":
    TTCHAR = c_wchar
    TTCHAR_P = c_wchar_p
    from ctypes.wintypes import BOOL
else:
    TTCHAR = c_char
    TTCHAR_P = c_char_p
    BOOL = c_int
INT32 = c_int
INT64 = c_longlong
UINT32 = c_uint
_TTInstance = c_void_p
TT_STRLEN = 512
TT_SAMPLERATES_MAX = 16
TT_VIDEOFORMATS_MAX = 1024
TT_TRANSMITUSERS_MAX = 128
TT_TRANSMITQUEUE_MAX = 16
TT_CHANNELS_OPERATOR_MAX = 16

# make functionfactory accepting functionname, restype, argtypes

# bindings
class SoundSystem(INT32):
	SOUNDSYSTEM_NONE = 0
	SOUNDSYSTEM_WINMM = 1
	SOUNDSYSTEM_DSOUND = 2
	SOUNDSYSTEM_ALSA = 3
	SOUNDSYSTEM_COREAUDIO = 4
	SOUNDSYSTEM_WASAPI = 5
	SOUNDSYSTEM_OPENSLES_ANDROID = 7
	SOUNDSYSTEM_AUDIOUNIT = 8

class SoundDevice(Structure):
	_fields_ = [
	("nDeviceID", INT32),
	("nSoundSystem", INT32),
	("szDeviceName", TTCHAR*TT_STRLEN),
	("szDeviceID", TTCHAR*TT_STRLEN),
	("nWaveDeviceID", INT32),
	("bSupports3D", BOOL),
	("nMaxInputChannels", INT32),
	("nMaxOutputChannels", INT32),
	("inputSampleRates", INT32 * TT_SAMPLERATES_MAX),
	("outputSampleRates", INT32 * TT_SAMPLERATES_MAX),
	("nDefaultSampleRate", INT32)
	]

class SoundLevel(INT32):
	SOUND_VU_MAX = 100
	SOUND_VU_MIN = 0
	SOUND_VOLUME_MAX = 32000
	SOUND_VOLUME_DEFAULT = 1000
	SOUND_VOLUME_MIN = 0
	SOUND_GAIN_MAX = 32000
	SOUND_GAIN_DEFAULT = 1000
	SOUND_GAIN_MIN = 0

class AudioBlock(Structure):
	_fields_ = [
	("nStreamID", INT32),
	("nSampleRate", INT32),
	("nChannels", INT32),
	("lpRawAudio", c_void_p),
	("nSamples", INT32),
	("uSampleIndex", UINT32),
	]

class MediaFileStatus(INT32):
	MFS_CLOSED          = 0
	MFS_ERROR           = 1
	MFS_STARTED         = 2
	MFS_FINISHED        = 3
	MFS_ABORTED         = 4
	MFS_PAUSED          = 5
	MFS_PLAYING         = 6

class AudioFileFormat(INT32):
	AFF_NONE                 = 0
	AFF_CHANNELCODEC_FORMAT  = 1
	AFF_WAVE_FORMAT          = 2
	AFF_MP3_16KBIT_FORMAT    = 3
	AFF_MP3_32KBIT_FORMAT    = 4
	AFF_MP3_64KBIT_FORMAT    = 5
	AFF_MP3_128KBIT_FORMAT   = 6
	AFF_MP3_256KBIT_FORMAT   = 7

class AudioFormat(Structure):
	_fields_ = [
	("nAudioFmt", INT32),
	("nSampleRate", INT32),
	("nChannels", INT32)
	]

class FourCC(INT32):
	FOURCC_NONE   =   0
	FOURCC_I420   = 100
	FOURCC_YUY2   = 101
	FOURCC_RGB32  = 102

class VideoFormat(Structure):
	_fields_ = [
	("nWidth", INT32),
	("nHeight", INT32),
	("nFPS_Numerator", INT32),
	("nFPS_Denominator", INT32),
	("picFourCC", INT32)
	]

class VideoFrame(Structure):
	_fields_ = [
	("nWidth", INT32),
	("nHeight", INT32),
	("nStreamID", INT32),
	("bKeyFrame", BOOL),
	("frameBuffer", c_void_p),
	("nFrameBufferSize", INT32)
	]

class VideoCaptureDevice(Structure):
	_fields_ = [
	("szDeviceID", TTCHAR*TT_STRLEN),
	("szDeviceName", TTCHAR*TT_STRLEN),
	("szCaptureAPI", TTCHAR*TT_STRLEN),
	("videoFormats", VideoFormat*TT_VIDEOFORMATS_MAX),
	("nVideoFormatsCount", INT32)
	]

class SpeexCodec(Structure):
	_fields_ = [
	("nBandmode", INT32),
	("nQuality", INT32),
	("nTxIntervalMSec", INT32),
	("bStereoPlayback", BOOL)
	]

class SpeexVBRCodec(Structure):
	_fields_ = [
	("nBandmode", INT32),
	("nQuality", INT32),
	("nBitRate", INT32),
	("nMaxBitRate", INT32),
	("bDTX", BOOL),
	("nTxIntervalMSec", INT32),
	("bStereoPlayback", BOOL)
	]

SPEEX_NB_MIN_BITRATE = 2150
SPEEX_NB_MAX_BITRATE = 24600
SPEEX_WB_MIN_BITRATE = 3950
SPEEX_WB_MAX_BITRATE = 42200
SPEEX_UWB_MIN_BITRATE = 4150
SPEEX_UWB_MAX_BITRATE = 44000

class OpusCodec(Structure):
	_fields_ = [
	("nSampleRate", INT32),
	("nChannels", INT32),
	("nApplication", INT32),
	("nComplexity", INT32),
	("bFEC", BOOL),
	("bDTX", BOOL),
	("nBitRate", INT32),
	("bVBR", BOOL),
	("bVBRConstraint", BOOL),
	("nTxIntervalMSec", INT32),
	("nFrameSizeMSec", INT32),
	]

OPUS_APPLICATION_VOIP = 2048
OPUS_APPLICATION_AUDIO = 2049
OPUS_MIN_BITRATE = 6000
OPUS_MAX_BITRATE = 510000
OPUS_MIN_FRAMESIZE = 2
OPUS_MAX_FRAMESIZE = 60
OPUS_REALMAX_FRAMESIZE = 120

class Codec(INT32):
	NO_CODEC                    = 0
	SPEEX_CODEC                 = 1
	SPEEX_VBR_CODEC             = 2
	OPUS_CODEC                  = 3
	WEBM_VP8_CODEC              = 128

class ACodecUnion(Union):
	_fields_ = [
	("speex", SpeexCodec),
	("speex_vbr", SpeexVBRCodec),
	("opus", OpusCodec)
	]

class AudioCodec(Structure):
	_anonymous_ = ["u"]
	_fields_ = [
	("nCodec", INT32),
	("u", ACodecUnion)
	]

class AudioConfig(Structure):
	_fields_ = [
	("bEnableAGC", BOOL),
	("nGainLevel", INT32),
	]

class TTType(INT32):
	__NONE = 0
	__AUDIOCODEC = 1
	__BANNEDUSER              = 2
	__VIDEOFORMAT             =  3
	__OPUSCODEC               =  4
	__CHANNEL                 =  5
	__CLIENTSTATISTICS        =  6
	__REMOTEFILE              =  7
	__FILETRANSFER            =  8
	__MEDIAFILESTATUS         =  9
	__SERVERPROPERTIES        = 10
	__SERVERSTATISTICS        = 11
	__SOUNDDEVICE             = 12
	__SPEEXCODEC              = 13
	__TEXTMESSAGE             = 14
	__WEBMVP8CODEC            = 15
	__TTMESSAGE               = 16
	__USER                    = 17
	__USERACCOUNT             = 18
	__USERSTATISTICS          = 19
	__VIDEOCAPTUREDEVICE      = 20
	__VIDEOCODEC              = 21
	__AUDIOCONFIG             = 22
	__SPEEXVBRCODEC           = 23
	__VIDEOFRAME              = 24
	__AUDIOBLOCK              = 25
	__AUDIOFORMAT             = 26
	__MEDIAFILEINFO           = 27
	__CLIENTERRORMSG          = 28
	__TTBOOL                  = 29
	__INT32                   = 30
	__DESKTOPINPUT            = 31
	__SPEEXDSP                = 32
	__STREAMTYPE              = 33
	__AUDIOPREPROCESSORTYPE   = 34
	__AUDIOPREPROCESSOR       = 35
	__TTAUDIOPREPROCESSOR     = 36
	__MEDIAFILEPLAYBACK       = 37
	__CLIENTKEEPALIVE         = 38

class DesktopInput(Structure):
	_fields_ = [
	("uMousePosX", c_uint16),
	("uMousePosY", c_uint16),
	("uKeyCode", UINT32),
	("uKeyState", UINT32)
	]

class FileTransfer(Structure):
	_fields_ = [
	("nStatus", INT32),
	("nTransferID", INT32),
	("nChannelID", INT32),
	("szLocalFilePath", TTCHAR*TT_STRLEN),
	("szRemoteFileName", TTCHAR*TT_STRLEN),
	("nFileSize", INT64),
	("nTransferred", INT64),
	("bInbound", BOOL)
	]

class MediaFileInfo(Structure):
	_fields_ = [
	("nStatus", INT32),
	("szFileName", TTCHAR*TT_STRLEN),
	("audioFmt", AudioFormat),
	("videoFmt", VideoFormat),
	("uDurationMSec", UINT32),
	("uElapsedMSec", UINT32)
	]

class RemoteFile(Structure):
	_fields_ = [
	("nChannelID", INT32),
	("nFileID", INT32),
	("szFileName", TTCHAR*TT_STRLEN),
	("nFileSize", INT64),
	("szUsername", TTCHAR*TT_STRLEN)
	]

class ServerProperties(Structure):
	_fields_ = [
	("szServerName", TTCHAR*TT_STRLEN),
	("szMOTD", TTCHAR*TT_STRLEN),
	("szMOTDRaw", TTCHAR*TT_STRLEN),
	("nMaxUsers", INT32),
	("nMaxLoginAttempts", INT32),
	("nMaxLoginsPerIPAddress", INT32),
	("nMaxVoiceTxPerSecond", INT32),
	("nMaxVideoCaptureTxPerSecond", INT32),
	("nMaxMediaFileTxPerSecond", INT32),
	("nMaxDesktopTxPerSecond", INT32),
	("nMaxTotalTxPerSecond", INT32),
	("bAutoSave", BOOL),
	("nTcpPort", INT32),
	("nUdpPort", INT32),
	("nUserTimeout", INT32),
	("szServerVersion", TTCHAR*TT_STRLEN),
	("szServerProtocolVersion", TTCHAR*TT_STRLEN),
	("nLoginDelayMSec", INT32),
	("szAccessToken", TTCHAR*TT_STRLEN),
	]

class ServerStatistics(Structure):
	_fields_ = [
	("nTotalBytesTX", INT64),
	("nTotalBytesRX", INT64),
	("nVoiceBytesTX", INT64),
	("nVoiceBytesRX", INT64),
	("nVideoCaptureBytesTX", INT64),
	("nVideoCaptureBytesRX", INT64),
	("nMediaFileBytesTX", INT64),
	("nMediaFileBytesRX", INT64),
	("nDesktopBytesTX", INT64),
	("nDesktopBytesRX", INT64),
	("nUsersServed", INT32),
	("nUsersPeak", INT32),
	("nFilesTx", INT64),
	("nFilesRx", INT64),
	("nUptimeMSec", INT64)
	]

class BannedUser(Structure):
	_fields_ = [
	("szIPAddress", TTCHAR*TT_STRLEN),
	("szChannelPath", TTCHAR*TT_STRLEN),
	("szBanTime", TTCHAR*TT_STRLEN),
	("szNickname", TTCHAR*TT_STRLEN),
	("szUsername", TTCHAR*TT_STRLEN),
	("uBanTypes", UINT32)
	]

class AbusePrevention(Structure):
	_fields_ = [
	("nCommandsLimit", INT32),
	("nCommandsIntervalMSec", INT32)
	]

class UserAccount(Structure):
	_fields_ = [
	("szUsername", TTCHAR*TT_STRLEN),
	("szPassword", TTCHAR*TT_STRLEN),
	("uUserType", UINT32),
	("uUserRights", UINT32),
	("nUserData", INT32),
	("szNote", TTCHAR*TT_STRLEN),
	("szInitChannel", TTCHAR*TT_STRLEN),
	("autoOperatorChannels", INT32*TT_CHANNELS_OPERATOR_MAX),
	("nAudioCodecBpsLimit", INT32),
	("abusePrevent", AbusePrevention)
	]

class ClientErrorMsg(Structure):
	_fields_ = [
	("nErrorNo", INT32),
	("szErrorMsg", TTCHAR*TT_STRLEN)
	]

class User(Structure):
	_fields_ = [
	("nUserID", INT32),
	("szUsername", TTCHAR * TT_STRLEN),
	("nUserData", INT32),
	("uUserType", UINT32),
	("szIPAddress", TTCHAR * TT_STRLEN),
	("uVersion", UINT32),
	("nChannelID", INT32),
	("uLocalSubscriptions", UINT32),
	("uPeerSubscriptions", UINT32),
	("szNickname", TTCHAR * TT_STRLEN),
	("nStatusMode", INT32),
	("szStatusMsg", TTCHAR * TT_STRLEN),
	("szMediaStorageDir", TTCHAR * TT_STRLEN),
	("uUserState", UINT32),
	("nVolumeVoice", INT32),
	("nVolumeMediaFile", INT32),
	("nStoppedDelayVoice", INT32),
	("nStoppedDelayMediaFile", INT32),
	("soundPositionVoice", c_float*3),
	("soundPositionMediaFile", c_float*3),
	("stereoPlaybackVoice", BOOL*2),
	("stereoPlaybackMediaFile", BOOL*2),
	("nBufferMSecVoice", INT32),
	("nBufferMSecMediaFile", INT32),
	("szClientName", TTCHAR * TT_STRLEN)
	]

class UserStatistics(Structure):
	_fields_ = [
	("nVoicePacketsRecv", INT64),
	("nVoicePacketsLost", INT64),
	("nVideoCapturePacketsRecv", INT64),
	("nVideoCaptureFramesRecv", INT64),
	("nVideoCaptureFramesLost", INT64),
	("nVideoCaptureFramesDropped", INT64),
	("nMediaFileAudioPacketsRecv", INT64),
	("nMediaFileAudioPacketsLost", INT64),
	("nMediaFileVideoPacketsRecv", INT64),
	("nMediaFileVideoFramesRecv", INT64),
	("nMediaFileVideoFramesLost", INT64),
	("nMediaFileVideoFramesDropped", INT64),
	]

class TextMsgType(INT32):
	MSGTYPE_USER      = 1
	MSGTYPE_CHANNEL   = 2
	MSGTYPE_BROADCAST = 3
	MSGTYPE_CUSTOM    = 4

class TextMessage(Structure):
	_fields_ = [
	("nMsgType", INT32),
	("nFromUserID", INT32),
	("szFromUsername", TTCHAR*TT_STRLEN),
	("nToUserID", INT32),
	("nChannelID", INT32),
	("szMessage", TTCHAR*TT_STRLEN),
	]

class Channel(Structure):
	_fields_ = [
	("nParentID", INT32),
	("nChannelID", INT32),
	("szName", TTCHAR*TT_STRLEN),
	("szTopic", TTCHAR*TT_STRLEN),
	("szPassword", TTCHAR*TT_STRLEN),
	("bPassword", BOOL),
	("uChannelType", UINT32),
	("nUserData", INT32),
	("nDiskQuota", INT64),
	("szOpPassword", TTCHAR*TT_STRLEN),
	("nMaxUsers", INT32),
	("audiocodec", AudioCodec),
	("audiocfg", AudioConfig),
	("transmitUsers", (INT32*2)*TT_TRANSMITUSERS_MAX),
	("transmitUsersQueue", INT32*TT_TRANSMITQUEUE_MAX)
	]

class TTMessageUnion(Union):
	_fields_ = [
	("channel", Channel),
	("clienterrormsg", ClientErrorMsg),
	("desktopinput", DesktopInput),
	("filetransfer", FileTransfer),
	("mediafileinfo", MediaFileInfo),
	("remotefile", RemoteFile),
	("serverproperties", ServerProperties),
	("serverstatistics", ServerStatistics),
	("textmessage", TextMessage),
	("user", User),
	("useraccount", UserAccount),
	("banneduser", BannedUser),
	("bActive", BOOL),
	("nBytesRemain", INT32),
	("nStreamID", INT32),
	("nPayloadSize", INT32),
	("nStreamType", INT32),
	("date", c_char*1)
	]

class TTMessage(Structure):
	_anonymous_ = [
	"u"
	]

	_fields_ = [
	("nClientEvent", INT32),
	("nSource", INT32),
	("ttType", INT32),
	("uReserved", UINT32),
	("u", TTMessageUnion)
	]

class ClientFlags(UINT32):
	CLIENT_CLOSED = 0x00000000
	CLIENT_SNDINPUT_READY = 0x00000001
	CLIENT_SNDOUTPUT_READY = 0x00000002
	CLIENT_SNDINOUTPUT_DUPLEX = 0x00000004
	CLIENT_SNDINPUT_VOICEACTIVATED = 0x00000008
	CLIENT_SNDINPUT_VOICEACTIVE = 0x00000010
	CLIENT_SNDOUTPUT_MUTE = 0x00000020
	CLIENT_SNDOUTPUT_AUTO3DPOSITION = 0x00000040
	CLIENT_VIDEOCAPTURE_READY = 0x00000080
	CLIENT_TX_VOICE = 0x00000100
	CLIENT_TX_VIDEOCAPTURE = 0x00000200
	CLIENT_TX_DESKTOP = 0x00000400
	CLIENT_DESKTOP_ACTIVE = 0x00000800
	CLIENT_MUX_AUDIOFILE = 0x00001000
	CLIENT_CONNECTING = 0x00002000
	CLIENT_CONNECTED = 0x00004000
	CLIENT_CONNECTION               = CLIENT_CONNECTING or CLIENT_CONNECTED
	CLIENT_AUTHORIZED = 0x00008000
	CLIENT_STREAM_AUDIO = 0x00010000
	CLIENT_STREAM_VIDEO = 0x00020000

_GetVersion = dll.TT_GetVersion
_GetVersion.restype = TTCHAR_P
_InitTeamTalkPoll = dll.TT_InitTeamTalkPoll
_InitTeamTalkPoll.restype = _TTInstance
_CloseTeamTalk = dll.TT_CloseTeamTalk
_CloseTeamTalk.restype = BOOL
_CloseTeamTalk.argtypes = [_TTInstance]
_GetMessage = dll.TT_GetMessage
_GetMessage.restype = BOOL
_GetMessage.argtypes = [_TTInstance, POINTER(TTMessage), POINTER(INT32)]
_GetFlags = dll.TT_GetFlags
_GetFlags.restype = UINT32
_GetFlags.argtypes = [_TTInstance]
_SetLicenseInformation = dll.TT_SetLicenseInformation
_SetLicenseInformation.restype = BOOL
_SetLicenseInformation.argtypes = [TTCHAR_P, TTCHAR_P]
_GetDefaultSoundDevices = dll.TT_GetDefaultSoundDevices
_GetDefaultSoundDevices.restype = BOOL
_GetDefaultSoundDevices.argtypes = [POINTER(INT32), POINTER(INT32)]
_GetDefaultSoundDevicesEx = dll.TT_GetDefaultSoundDevicesEx
_GetDefaultSoundDevicesEx.restype = BOOL
_GetDefaultSoundDevicesEx.argtypes = [SoundSystem, POINTER(INT32), POINTER(INT32)]
_GetSoundDevices = dll.TT_GetSoundDevices
_GetSoundDevices.restype = BOOL
_GetSoundDevices.argtypes = [POINTER(SoundDevice), POINTER(INT32)]
_InitSoundInputDevice = dll.TT_InitSoundInputDevice
_InitSoundInputDevice.restype = BOOL
_InitSoundInputDevice.argtypes = [_TTInstance, INT32]
_InitSoundOutputDevice = dll.TT_InitSoundOutputDevice
_InitSoundOutputDevice.restype = BOOL
_InitSoundOutputDevice.argtypes = [_TTInstance, INT32]
_EnableVoiceTransmission = dll.TT_EnableVoiceTransmission
_EnableVoiceTransmission.restype = BOOL
_EnableVoiceTransmission.argstype = [_TTInstance, BOOL]
_EnableVoiceActivation = dll.TT_EnableVoiceActivation
_EnableVoiceActivation.restype = BOOL
_EnableVoiceActivation.argstype = [_TTInstance, BOOL]
_SetVoiceActivationLevel = dll.TT_SetVoiceActivationLevel
_SetVoiceActivationLevel.restype = BOOL
_SetVoiceActivationLevel.argstype = [_TTInstance, INT32]
_GetVoiceActivationLevel = dll.TT_GetVoiceActivationLevel
_GetVoiceActivationLevel.restype = INT32
_GetVoiceActivationLevel.argstype = [_TTInstance]
_SetVoiceActivationStopDelay = dll.TT_SetVoiceActivationStopDelay
_SetVoiceActivationStopDelay.restype = BOOL
_SetVoiceActivationStopDelay.argstype = [_TTInstance, INT32]
_GetVoiceActivationStopDelay = dll.TT_GetVoiceActivationStopDelay
_GetVoiceActivationStopDelay.restype = INT32
_GetVoiceActivationStopDelay.argstype = [_TTInstance]
_Connect = dll.TT_Connect
_Connect.restype = BOOL
_Connect.argtypes = [_TTInstance, TTCHAR_P, INT32, INT32, INT32, INT32, BOOL]
_ConnectSysID = dll.TT_ConnectSysID
_ConnectSysID.restype = BOOL
_ConnectSysID.argtypes = [_TTInstance, TTCHAR_P, INT32, INT32, INT32, INT32, BOOL, TTCHAR_P]
_ConnectEx = dll.TT_ConnectEx
_ConnectEx.restype = BOOL
_ConnectEx.argtypes = [_TTInstance, TTCHAR_P, INT32, INT32, TTCHAR_P, INT32, INT32, BOOL]
_Disconnect = dll.TT_Disconnect
_Disconnect.restype = BOOL
_Disconnect.argtypes = [_TTInstance]
_QueryMaxPayload = dll.TT_QueryMaxPayload
_QueryMaxPayload.restype = BOOL
_QueryMaxPayload.argstype = [_TTInstance, INT32]
_DoPing = dll.TT_DoPing
_DoPing.restype = INT32
_DoPing.argstype = [_TTInstance]
_DoLogin = dll.TT_DoLogin
_DoLogin.restype = INT32
_DoLogin.argtypes = [_TTInstance, TTCHAR_P, TTCHAR_P, TTCHAR_P]
_DoLoginEx = dll.TT_DoLoginEx
_DoLoginEx.restype = INT32
_DoLoginEx.argtypes = [_TTInstance, TTCHAR_P, TTCHAR_P, TTCHAR_P, TTCHAR_P]
_DoLogout = dll.TT_DoLogout
_DoLogout.restype = INT32
_DoLogout.argstype = [_TTInstance]
_DoJoinChannelByID = dll.TT_DoJoinChannelByID
_DoJoinChannelByID.restype = INT32
_DoJoinChannelByID.argtypes = [_TTInstance, INT32, TTCHAR_P]
_DoLeaveChannel = dll.TT_DoLeaveChannel
_DoLeaveChannel.restype = INT32
_DoLeaveChannel.argstype = [_TTInstance]
_DoChangeNickname = dll.TT_DoChangeNickname
_DoChangeNickname.restype = INT32
_DoChangeNickname.argstype = [_TTInstance, TTCHAR_P]
_DoChangeStatus = dll.TT_DoChangeStatus
_DoChangeStatus.restype = INT32
_DoChangeStatus.argstype = [_TTInstance, INT32, TTCHAR_P]
_DoTextMessage = dll.TT_DoTextMessage
_DoTextMessage.restype = INT32
_DoTextMessage.argtypes = [_TTInstance, POINTER(TextMessage)]
_GetServerProperties = dll.TT_GetServerProperties
_GetServerProperties.restype = BOOL
_GetServerProperties.argtypes = [_TTInstance, POINTER(ServerProperties)]
_GetServerUsers = dll.TT_GetServerUsers
_GetServerUsers.restype = BOOL
_GetServerUsers.argtypes = [_TTInstance, POINTER(User), POINTER(INT32)]
_GetRootChannelID = dll.TT_GetRootChannelID
_GetRootChannelID.restype = INT32
_GetRootChannelID.argtypes = [_TTInstance]
_GetMyChannelID = dll.TT_GetMyChannelID
_GetMyChannelID.restype = INT32
_GetMyChannelID.argtypes = [_TTInstance]
_GetChannel = dll.TT_GetChannel
_GetChannel.restype = BOOL
_GetChannel.argtypes = [_TTInstance, INT32, POINTER(Channel)]
_GetChannelPath = dll.TT_GetChannelPath
_GetChannelPath.restype = BOOL
_GetChannelPath.argtypes = [_TTInstance, INT32, POINTER(TTCHAR*TT_STRLEN)]
_GetChannelIDFromPath = dll.TT_GetChannelIDFromPath
_GetChannelIDFromPath.restype = INT32
_GetChannelIDFromPath.argtypes = [_TTInstance, TTCHAR_P]
_GetChannelUsers = dll.TT_GetChannelUsers
_GetChannelUsers.restype = BOOL
_GetChannelUsers.argtypes = [_TTInstance, INT32, POINTER(User), POINTER(INT32)]
_GetChannelFiles = dll.TT_GetChannelFiles
_GetChannelFiles.restype = BOOL
_GetChannelFiles.argtypes = [_TTInstance, INT32, POINTER(RemoteFile), POINTER(INT32)]
_GetServerChannels = dll.TT_GetServerChannels
_GetServerChannels.restype = BOOL
_GetServerChannels.argtypes = [_TTInstance, POINTER(Channel), POINTER(INT32)]
_GetMyUserID = dll.TT_GetMyUserID
_GetMyUserID.restype = INT32
_GetMyUserID.argtypes = [_TTInstance]
_GetMyUserAccount = dll.TT_GetMyUserAccount
_GetMyUserAccount.restype = BOOL
_GetMyUserAccount.argtypes = [_TTInstance, POINTER(UserAccount)]
_GetMyUserData = dll.TT_GetMyUserData
_GetMyUserData.restype = INT32
_GetMyUserData.argtypes = [_TTInstance]
_GetUser = dll.TT_GetUser
_GetUser.restype = BOOL
_GetUser.argtypes = [_TTInstance, INT32, POINTER(User)]
_GetUserStatistics = dll.TT_GetUserStatistics
_GetUserStatistics.restype = BOOL
_GetUserStatistics.argtypes = [_TTInstance, INT32, POINTER(UserStatistics)]
_GetUserByUsername = dll.TT_GetUserByUsername
_GetUserByUsername.restype = BOOL
_GetUserByUsername.argtypes = [_TTInstance, TTCHAR_P, POINTER(User)]
_GetErrorMessage = dll.TT_GetErrorMessage
_GetErrorMessage.restype = c_void_p
_GetErrorMessage.argtypes = [INT32, POINTER(TTCHAR*TT_STRLEN)]


# main code

def getVersion():
	return _GetVersion()

def setLicense(name, key):
	return _SetLicenseInformation(name, key)

class TeamTalkError(Exception):
    pass

class TeamTalk(object):

	def __init__(self):
		self._tt = _InitTeamTalkPoll()
		if not self._tt:
			raise TeamTalkError("failed to initialize")

	def closeTeamTalk(self):
		return _CloseTeamTalk(self._tt)

	def __del__(self):
		self.closeTeamTalk()

	def getMessage(self, nWaitMS=-1):
		msg = TTMessage()
		nWaitMS = INT32(nWaitMS)
		_GetMessage(self._tt, byref(msg), byref(nWaitMS))
		return msg

	def getFlags(self):
		return _GetFlags(self._tt)

	def getDefaultSoundDevices(self):
		indevid = INT32()
		outdevid = INT32()
		_GetDefaultSoundDevices(byref(indevid), byref(outdevid))
		return indevid, outdevid

	def getSoundDevices(self):
		count = c_int()
		_GetSoundDevices(None, byref(count))
		soundDevs = (SoundDevice*count.value)()
		_GetSoundDevices(soundDevs, byref(count))
		return soundDevs

	def initSoundInputDevice(self, indev):
		return _InitSoundInputDevice(self._tt, indev)

	def initSoundOutputDevice(self, outdev):
		return _InitSoundOutputDevice(self._tt, outdev)

	def enableVoiceTransmission(self, bEnable):
		return _EnableVoiceTransmission(self._tt, bEnable)

	def Connect(self, szHostAddress, nTcpPort, nUdpPort, nLocalTcpPort=0, nLocalUdpPort=0, bEncrypted=False):
		return _Connect(self._tt, szHostAddress, nTcpPort, nUdpPort, nLocalTcpPort, nLocalUdpPort, bEncrypted)

	def Disconnect(self):
		return _Disconnect(self._tt)

	def doPing(self):
		return _DoPing(self._tt)

	def DoLogin(self, szNickname, szUsername="", szPassword="", szClientname="python"):
		return _DoLoginEx(self._tt, szNickname, szUsername, szPassword, szClientname)

	def doLogout(self):
		return _DoLogout(self._tt)

	def DoJoinChannelByID(self, nChannelID, szPassword=""):
		return _DoJoinChannelByID(self._tt, nChannelID, szPassword)

	def doLeaveChannel(self):
		return _DoLeaveChannel(self._tt)

	def doChangeNickname(self, szNewNick):
		return _DoChangeNickname(self._tt, szNewNick)

	def doChangeStatus(self, nStatusMode, szStatusMessage):
		return _DoChangeStatus(self._tt, nStatusMode, szStatusMessage)

	def doTextMessage(self, msg):
		return _DoTextMessage(self._tt, msg)

	def getServerProperties(self):
		srvprops = ServerProperties()
		_GetServerProperties(self._tt, srvprops)
		return srvprops

	def getServerUsers(self):
		count = c_int()
		_GetServerUsers(self._tt, None, byref(count))
		users = (User*count.value)()
		_GetServerUsers(self._tt, users, byref(count))
		return users

	def getRootChannelID(self):
		return _GetRootChannelID(self._tt)

	def getMyChannelID(self):
		return _GetMyChannelID(self._tt)

	def getChannel(self, nChannelID):
		channel= Channel()
		_GetChannel(self._tt, nChannelID, channel)
		return channel

	def getChannelPath(self, nChannelID):
		szChannelPath = (TTCHAR*TT_STRLEN)()
		_GetChannelPath(self._tt, nChannelID, szChannelPath)
		return szChannelPath.value

	def getChannelIDFromPath(self, szChannelPath):
		return _GetChannelIDFromPath(self._tt, szChannelPath)

	def getChannelUsers(self, nChannelID):
		count = c_int()
		_GetChannelUsers(self._tt, nChannelID, None, byref(count))
		users = (User*count.value)()
		_GetChannelUsers(self._tt, nChannelID, users, byref(count))
		return users

	def getChannelFiles(self, nChannelID):
		count = c_int()
		_GetChannelFiles(self._tt, nChannelID, None, byref(count))
		files = (RemoteFile*count.value)()
		_GetChannelFiles(self._tt, nChannelID, files, byref(count))
		return files

	def getServerChannels(self):
		count = c_int()
		_GetServerChannels(self._tt, None, byref(count))
		channels = (Channel*count.value)()
		_GetServerChannels(self._tt, channels, byref(count))
		return channels

	def getMyUserID(self):
		return _GetMyUserID(self._tt)

	def getMyUserAccount(self):
		account = UserAccount()
		_GetMyUserAccount(self._tt, account)
		return account

	def getMyUserData(self):
		return _GetMyUserData(self._tt)

	def getUser(self, nUserID):
		user = User()
		_GetUser(self._tt, nUserID, user)
		return user

	def getUserStatistics(self, nUserID):
		stats = UserStatistics()
		_GetUserStatistics(self._tt, nUserID, stats)
		return stats

	def getUserByUsername(self, szUsername):
		user = User()
		_GetUserByUsername(self._tt, szUsername, user)
		return user

	def getErrorMessage(self, nError):
		szErrorMsg = (TTCHAR*TT_STRLEN)()
		_GetErrorMessage(nError, szErrorMsg)
		return szErrorMsg.value