localhost = '127.0.0.1'
SERVER_PORT = 8008
CHATROOM_PORT = 8009
STREAMER_PORT = 8010
INVALID_PORTS = [SERVER_PORT, CHATROOM_PORT, STREAMER_PORT]
server_to_port = {
    'choghondar': CHATROOM_PORT,
    'shalgham': STREAMER_PORT
}
VIDEO_NAMES = ['Pat & Mat Song', 'Tom & Jerry']
VIDEO_PATHS = [
    'videos/Pat_Mat_Theme.mp4',
    'videos/Tom_and_Jerry.mp4',
]

VIDEO_DELAY = [0.005, 0.03]