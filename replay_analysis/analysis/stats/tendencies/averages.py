from typing import List

import pandas as pd

from replay_analysis.generated.api import game_pb2
from replay_analysis.generated.api.player_pb2 import Player
from replay_analysis.generated.api.stats.events_pb2 import Hit


class Averages:
    @classmethod
    def get_averages_for_player(cls, player: Player, proto_game: game_pb2.Game, data_frames):
        goal_frames = data_frames.game.goal_number.notnull()
        player_data_frame = data_frames[player.name][goal_frames]

        speed: pd.Series = (player_data_frame.vel_x ** 2 +
                            player_data_frame.vel_y ** 2 +
                            player_data_frame.vel_z ** 2) ** 0.5

        average_speed = speed.mean()

        player.stats.averages.average_speed = average_speed

        player_hits: List[Hit] = [saltie_hit for saltie_hit in proto_game.game_stats.hits if
                                  saltie_hit.player_id.id == player.id]

        hit_distances = [saltie_hit.distance for saltie_hit in player_hits
                         if saltie_hit.distance is not None and not saltie_hit.dribble]
        if len(hit_distances) > 0:
            average_hit_distance = sum(hit_distances) / len(hit_distances)
            player.stats.averages.average_hit_distance = average_hit_distance
