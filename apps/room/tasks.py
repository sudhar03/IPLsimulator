from iplsimulator.celery import app
from django.utils import timezone
from .models import Room, AuctionPlayer, TeamState
import random
import logging
import time
logger = logging.getLogger(__name__)

@app.task
def auction_tick_all_rooms():
    rooms = Room.objects.filter(completed=False)

    for room in rooms:
        try:
            current_player = AuctionPlayer.objects.filter(room=room, status="ACTIVE").first()
            print(current_player)

            if not current_player:
                start_next_player(room)
                continue

            # Check if the player has been idle too long (no bid for N seconds)
            now = timezone.now()
            time_since_last_bid = (now - current_player.modified).total_seconds()
            if time_since_last_bid >= 30:
                finalize_player(current_player)
                continue

            ai_teams = TeamState.objects.filter(room=room, is_user=False).exclude(team=current_player.current_bid_team)
            ai_teams = list(ai_teams)
            random.shuffle(ai_teams)
            print(ai_teams)

            for team in ai_teams:
                if team.purse < current_player.current_bid + 10_00_000:
                    continue
                if team.players.count() >= 15:
                    continue

                max_bid = calculate_max_bid(team, current_player)
                if current_player.current_bid >= max_bid:
                    continue

                chance = calculate_bid_chance(team, current_player)
                print("chance", chance)
                print("random", random.random())

                if random.random() < chance:
                    bid_amount = get_next_bid_amount(current_player.current_bid)
                    current_player.current_bid = bid_amount
                    current_player.current_bid_team = team
                    current_player.save()
                    print("bid_amount", bid_amount)
                    break

        except Exception as e:
            logger.error(f"Error in auction tick for room {room.id}: {str(e)}")


def finalize_player(player):
    if player.current_bid_team:
        print("player.current_bid_team", player.current_bid_team)
        team = player.current_bid_team
        player.status = "SOLD"
        player.final_price = player.current_bid
        player.final_team = team
        player.save()

        # Deduct bid amount from team purse
        team.purse -= player.current_bid
        team.players_count += 1
        team.save()

    else:
        print("player", player)
        player.status = "UNSOLD"
        player.save()


def calculate_bid_chance(team, player):
    score = player.overall_percentage / 100

    if player.player_type in ['Batter', 'wk-Batter']:
        score += float(player.batting_average) / 100
    elif player.player_type == 'Bowler':
        score += (40 - float(player.bowling_average)) / 100
    elif player.player_type == 'Allrounder':
        score += (float(player.batting_average) + (40 - float(player.bowling_average))) / 200

    personality_weights = {
        "Aggressive": 1.2,
        "Superstar": 1.15,
        "High Potential": 1.1,
        "Experienced": 1.05,
        "Consistent": 1.0,
        "Potential": 0.95,
        "Underdog": 0.85,
        "Inconsistent": 0.75,
    }
    score *= personality_weights.get(player.personality, 1.0)

    if team.players_count >= 13:
        score *= 0.7
    elif team.purse < player.current_bid + 20_00_000:
        score *= 0.6

    score += random.uniform(-0.1, 0.1)
    return max(0.0, min(score, 1.0))


def calculate_max_bid(team, player):
    base = player.base_price
    multiplier = {
        "Superstar": 4,
        "High Potential": 3,
        "Experienced": 2.5,
        "Aggressive": 2.5,
        "Consistent": 2,
        "Potential": 1.75,
        "Underdog": 1.5,
        "Inconsistent": 1.2,
    }
    weight = multiplier.get(player.personality, 1.5)
    max_bid = base * weight
    return min(max_bid, team.purse - 500_000_000)


def get_next_bid_amount(current_bid):
    return current_bid + 500_000_000



def next_bid_flow(auction_player):
    if not auction_player.current_bid == 0:
        return auction_player.current_bid + 500_000_000
    else:
        return auction_player.base_price + 500_000_000


def start_next_player(room):
    auction_player = AuctionPlayer.objects.filter(room=room, status="PENDING")
    player = random.choice(auction_player)
    player.status = "ACTIVE"
    player.save()   


def auction_tick_all_rooms():
    rooms = Room.objects.filter(completed=False)

    for room in rooms:
        try:
            current_player = AuctionPlayer.objects.filter(room=room, status="ACTIVE").first()
            print(current_player)

            if not current_player:
                start_next_player(room)
                continue

            # Check if the player has been idle too long (no bid for N seconds)
            now = timezone.now()
            time_since_last_bid = (now - current_player.modified).total_seconds()
            if time_since_last_bid >= 50:
                finalize_player(current_player)
                continue

            ai_teams = TeamState.objects.filter(room=room, is_user=False)
            if current_player.current_bid_team:
                ai_teams = ai_teams.exclude(id=current_player.current_bid_team.id)
            ai_teams = list(ai_teams)
            random.shuffle(ai_teams)
            print(ai_teams)

            for team in ai_teams:
                print(team.team.name)
                if team.purse < current_player.current_bid + 50_000_000:
                    print("team.purse", team.purse)
                    continue
                if team.players_count >= 15:
                    print("team.players_count", team.players_count)
                    continue

                max_bid = calculate_max_bid(team, current_player)
                if current_player.current_bid >= max_bid:
                    print("max_bid", max_bid)
                    continue

                chance = calculate_bid_chance(team, current_player)
                print("chance", chance)
                print("random", random.random())

                if random.random() < chance:
                    bid_amount = get_next_bid_amount(current_player.current_bid)
                    current_player.current_bid = bid_amount
                    current_player.current_bid_team = team
                    current_player.save()
                    print("bid_amount", bid_amount)
                    break
                time.sleep(3)

        except Exception as e:
            logger.error(f"Error in auction tick for room {room.id}: {str(e)}")
            print(e)

