import json

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_user_list_from_followers(followers_json):
    users = []
    for entry in followers_json:
        try:
            data = entry["string_list_data"][0]
            users.append({
                "username": data["value"],
                "profile_url": data["href"]
            })
        except (KeyError, IndexError):
            continue
    return users

def extract_user_list_from_following(following_json):
    users = []
    following_list = following_json.get("relationships_following", [])
    for entry in following_list:
        try:
            data = entry["string_list_data"][0]
            users.append({
                "username": data["value"],
                "profile_url": data["href"]
            })
        except (KeyError, IndexError):
            continue
    return users

def find_not_following_back(following, followers):
    follower_usernames = {user["username"] for user in followers}
    return [user for user in following if user["username"] not in follower_usernames]

def main():
    followers_raw = load_json("followers_1.json")
    following_raw = load_json("following.json")

    followers = extract_user_list_from_followers(followers_raw)
    following = extract_user_list_from_following(following_raw)

    not_following_back = find_not_following_back(following, followers)

    with open("not_following_back.json", "w", encoding="utf-8") as f:
        json.dump(not_following_back, f, indent=2)

    print(f"✅ Done: {len(not_following_back)} profiles not following you back written to not_following_back.json")

if __name__ == "__main__":
    main()
