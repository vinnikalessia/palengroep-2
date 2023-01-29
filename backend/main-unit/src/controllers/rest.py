from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from models.game_models import GameScore, GameConfigModel, GameStatusResponse, GamesResponse, CurrentGameStatus
from models.leaderboard_models import LeaderboardResponse
from routers.general import router as global_router
from services.game_service import GameService

tags_metadata = [
    {
        "name": "socketio",
        "description": "SocketIO routes so it is easier to test the game using swagger",
    }
]


class RestController:
    def __init__(self, game_service: GameService):
        self.game_service = game_service
        self.app = FastAPI(openapi_tags=tags_metadata)
        self.__setup_middleware()
        self.__include_routers()

    def __setup_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def __include_routers(self):
        self.app.include_router(router=global_router)

    def __setup_socketio_endpoints(self):
        # region REST api endpoints of socketio
        # handy for swagger
        @self.app.put("/sio/start_game", tags=["socketio"])
        def start_game_api():
            self.game_service.start_game()

        @self.app.put("/sio/pause_game", tags=["socketio"])
        def pause_game_api():
            self.game_service.pause_game()

        @self.app.put("/sio/resume_game", tags=["socketio"])
        def resume_game_api():
            self.game_service.resume_game()

        @self.app.put("/sio/stop_game", tags=["socketio"])
        def stop_game_api():
            self.game_service.stop_game()

    def setup_endpoints(self):
        self.__setup_socketio_endpoints()

        @self.app.get("/leaderboard/{game}")
        def get_leaderboard(game: str) -> LeaderboardResponse:
            return LeaderboardResponse(leaderboard=self.game_service.get_leaderboard(game))

        @self.app.get("/score")
        def get_score() -> GameScore:
            return self.game_service.get_score()

        @self.app.post("/game/setup")
        def setup(setup_config: GameConfigModel) -> GameStatusResponse:
            """
            post request which gets game name, team name(s), a duration and a difficulty setting from the body
            """

            current_game = self.game_service.setup_game(setup_config)
            return current_game

        @self.app.get("/game/status")
        def get_game_status() -> CurrentGameStatus:
            return self.game_service.get_current_game_status()

        @self.app.get("/games", description="Get all games")
        def get_games() -> GamesResponse:
            return GamesResponse(games=self.game_service.get_games())

        return self.app
