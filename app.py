from flask import Flask, request, jsonify
import requests
from datetime import datetime, timezone

app = Flask(__name__)

@app.route('/api/account/', methods=['GET'])
def get_account_info():
    uid = request.args.get('uid')
    region = request.args.get('region')

    if not uid or not region:
        return jsonify({'error': 'Missing uid or region'}), 400

    headers = {
        'authority': 'ff-hl-gaming-official-api-account-v2-latest-bay.vercel.app',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://www.hlgamingofficial.com',
        'referer': 'https://www.hlgamingofficial.com/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; M2006C3MG)',
    }

    json_data = {
        'uid': uid,
        'region': region,
        'key': 'FFwlx',
    }

    response = requests.post(
        'https://ff-hl-gaming-official-api-account-v2-latest-bay.vercel.app/api/account',
        headers=headers,
        json=json_data,
    )

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data'}), 500

    data = response.json()

    account_info = data.get('AccountInfo', {})
    captain_info = data.get('captainBasicInfo', {})
    guild_info = data.get('GuildInfo', {})
    pet_info = data.get('petInfo', {})
    social_info = data.get('socialinfo', {})
    credit_info = data.get('creditScoreInfo', {})

    def format_time(ts):
        try:
            return datetime.fromtimestamp(int(ts), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return 'N/A'

    result = {
        "account": {
            "name": account_info.get('AccountName', 'N/A'),
            "id": uid,
            "region": account_info.get('AccountRegion', 'N/A'),
            "level": account_info.get('AccountLevel', 'N/A'),
            "exp": account_info.get('AccountEXP', 'N/A'),
            "likes": account_info.get('AccountLikes', 'N/A'),
            "bp_badges": account_info.get('AccountBPBadges', 'N/A'),
            "last_login": format_time(account_info.get('AccountLastLogin')),
            "type": "Normal" if account_info.get('AccountType') == 1 else "VIP",
            "br_rank": account_info.get('BrRankPoint', 'N/A'),
            "br_max": account_info.get('BrMaxRank', 'N/A'),
            "cs_rank": account_info.get('CsRankPoint', 'N/A'),
            "cs_max": account_info.get('CsMaxRank', 'N/A'),
            "version": account_info.get('ReleaseVersion', 'N/A'),
        },
        "captain": {
            "nickname": captain_info.get('nickname', 'N/A'),
            "id": captain_info.get('accountId', 'N/A'),
            "level": captain_info.get('level', 'N/A'),
            "br_rank": captain_info.get('rank', 'N/A'),
            "br_max": captain_info.get('maxRank', 'N/A'),
            "cs_rank": captain_info.get('csRank', 'N/A'),
            "cs_max": captain_info.get('csMaxRank', 'N/A'),
            "created": format_time(captain_info.get('createAt')),
            "last_login": format_time(captain_info.get('lastLoginAt')),
        },
        "guild": {
            "name": guild_info.get('GuildName', 'N/A'),
            "id": guild_info.get('GuildID', 'N/A'),
            "level": guild_info.get('GuildLevel', 'N/A'),
            "members": f"{guild_info.get('GuildMember', 'N/A')}/{guild_info.get('GuildCapacity', 'N/A')}",
            
        },
        "pet": {
            "name": pet_info.get('name', 'N/A'),
            "id": pet_info.get('id', 'N/A'),
            "level": pet_info.get('level', 'N/A'),
            "exp": pet_info.get('exp', 'N/A'),
        },
        "social": {
            "language": social_info.get('AccountLanguage', 'N/A'),
            "signature": social_info.get('AccountSignature', 'N/A'),
            "owner": guild_info.get('GuildOwner', 'N/A'),
        },
        "credit_score": {
            "score": credit_info.get('creditScore', 'N/A'),
            "reward": "Eligible" if credit_info.get('rewardState') == 1 else "Not Eligible"
        },
        "developer": "@YU_z2"
    }

    return jsonify(result), 200
    
    
    
if __name__ == '__main__':
    app.run(debug=True)    
    