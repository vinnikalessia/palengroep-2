from fastapi_socketio import SocketManager

from services.game_service import GameService


class SocketIOController:
    def __init__(self, app, game_service: GameService):
        self.game_service = game_service
        self.app = app
        self.sio = SocketManager(app=app, cors_allowed_origins="*")

    def setup_endpoints(self):
        @self.sio.on("connect")
        def connect(sid, environ):
            print("connect ", sid)

        @self.sio.on('disconnect')
        def disconnect(sid):
            print('disconnect ', sid)

        @self.sio.on('start_game')
        def start_game(sid):
            self.game_service.start_game()
            print('start_game ', sid)
            self.sio.emit('game_started')

        @self.sio.on('pause_game')
        def pause_game(sid):
            print('pause_game ', sid)
            self.game_service.pause_game()
            self.sio.emit('game_paused')

        @self.sio.on('resume_game')
        def resume_game(sid):
            print('resume_game ', sid)
            self.game_service.resume_game()
            self.sio.emit('game_resumed')

        @self.sio.on('stop_game')
        async def stop_game(sid):
            print('stop_game ', sid)
            self.game_service.stop_game()
            self.sio.emit('game_stopped')

        return self.sio
