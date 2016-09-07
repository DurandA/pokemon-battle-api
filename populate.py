import random
from faker import Factory
fake = Factory.create('fr_CH')

from app import create_app
from app.modules.players.models import db, Player
from app.modules.teams.models import Team, TeamMember
from app.modules.matches.models import Match, Point

import datetime

app = create_app()

with app.app_context():
    #db.create_all(app)
    teams = []

    for i in range(10):
        new_team = Team(title=fake.company())
        db.session.add(new_team)
        teams.append(new_team)

        for j in range(10):
            is_male = random.getrandbits(1)
            p_args = {
                'first_name': fake.first_name_male() if is_male else fake.first_name_female(),
                'last_name': fake.last_name_male() if is_male else fake.last_name_female(),
                'country_code': fake.country_code(),
                'skill': random.randrange(100),
                'gender': 'male' if is_male else 'female',
            }
            new_player = Player(**p_args)
            print(new_player)
            db.session.add(new_player)
            team_member = TeamMember(team=new_team, player=new_player)
            db.session.add(team_member)

    db.session.commit()

    for i in range(10):
        team1, team2 = random.sample(teams, 2)
        new_match = Match(team1=team1, team2=team2, start_time=datetime.datetime.now() + datetime.timedelta(minutes = j*90))
        db.session.add(new_match)

        for j in range(random.randint(0, 10)):
            db.session.add(
                Point(match=new_match, team=team1, player=random.choice(team1.members).player)
            )

    db.session.commit()

# 'Adam'
# 'Lucy Cechtelar'
