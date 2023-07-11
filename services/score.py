from lib.utils import dt_utcnow
from models import AccountsFilteredDetailModel, VerticalKeywordGroupModel, FollowerGroupModel, FavouriteAccountModel
import re
from datetime import timezone

class ScoreService:
    
    @staticmethod
    def get_alnum(string):
        if not string:
            return ''
        return ''.join(e for e in string if e.isalnum())
    
    # Check if username is website url, or discord url in description or user url
    @classmethod
    def name_in_url(cls, user_profile):
        username = cls.get_alnum(user_profile["username"].replace("0x", "")).lower()
        name = cls.get_alnum(user_profile["name"]).lower()
        if not name or not username:
            return 0

        # Check url in user url
        from_url = 1 if "user_url" in user_profile and user_profile["user_url"] and (username in user_profile["user_url"].lower() or name in user_profile["user_url"].lower()) else 0
        if from_url:
            return 1

        # Check url in description
        if user_profile["description"] and (username in user_profile["description"].lower() or name in user_profile["description"].lower()):
            # ex: a protocol for trading and automated liquidity provision on Ethereum at uniswap.org
            _data = user_profile["description"].split(username)
            for sub in _data:
                domains = re.split('; |, |\*|\n', sub)
                for domain in domains:
                    if "." in domain and len(domain) >= 3:
                        return 1

            _data = user_profile["description"].split(name)
            for sub in _data:
                domains = re.split('; |, |\*|\n', sub)
                for domain in domains:
                    if "." in domain and len(domain) >= 3:
                        return 1
                    
        return 0
    
    @staticmethod
    def valid_description(user_profile):
        # Check len
        valid = 1
        #     if len(user_profile["description"]) < 20:
        #         valid = 0
        
        # Check if description contain only link tele
        data = user_profile["description"].split(" ")
        if len(data) == 1 and "t.me" in data[0]:
            #Sample https://twitter.com/GOLDHEARTBnB
            valid = 0
        
        # Check more
        return valid
    
    @staticmethod
    def get_keyword_list():
        _keywords_list = VerticalKeywordGroupModel.find({
            'name_slugify': 'keyword-relevance'
        })
        for i in _keywords_list:
            keywords_list = set(i["keywords"])
        return keywords_list
        
    @staticmethod
    def keywords_in_description(user_profile, keywords_list):
        if not user_profile["description"]:
            return 0
        count = 0
        for word in keywords_list:
            if word.lower() in user_profile["description"].lower() :
                count += 1
        return count

    @staticmethod
    def get_people_keywords():
        return ["writer", "engineer", "researcher", "manager", "professor", "speaker", "technology company", "shipping", "merch", "consult", "i am", "i'm", "memecoin", "meme coin"]
    
    @staticmethod
    def people_keywords_in_description(user_profile, people_keywords):
        
        if not user_profile["description"]:
            return 0
        
        if any(word.lower() in user_profile["description"].lower() for word in people_keywords):
            return 1

        return 0
    
    @staticmethod
    def get_social_keywords():
        return ["news", "trends", "talk", "podcast", "research", "course", "summit", "referral", "informative", "insight", "education", "invest", "nft collection", "nfts"]
    
    @staticmethod
    def social_keywords_in_description(user_profile, social_keywords):
        if not user_profile["description"]:
            return 0
        
        if any(word.lower() in user_profile["description"].lower() for word in social_keywords):
            return 1

        return 0
    
    # Check if user have url
    def have_url(user_profile):
        return 1 if user_profile["user_url"] else 0

    @classmethod
    def is_protocol(cls, user_profile):
        if not user_profile["description"]:
            return 0
        if not cls.name_in_url(user_profile):
            return 0
        
        return 1

    @staticmethod
    def get_account_list():
        _account_list = FollowerGroupModel.find({"name_slugify" : "full-follower"})
        for i in _account_list:
            account_list = set(i["accounts"])
            
        return account_list
        
    @staticmethod
    def number_friendship(user_profile, account_list):
        friendship = user_profile["friendship"]
        valid_friendship = list(set(friendship) & set(account_list))
                                
        return len(valid_friendship)

    @classmethod
    def scoring(cls, 
        user_profiles_ext,
        max_keyword_relevance,
        max_follower_quality,
        max_verification_status,
        max_recency
    ):
        for i in user_profiles_ext:
            i['in_watch_account'] = cls.check_favoutrite_account(i['username'])
            i["score_keyword_relevance"] = i["keyword_relevance"] * 100 / max_keyword_relevance
            i["score_follower_quality"] = i["follower_quality"] * 100 / max_follower_quality
            i["score_verification_status"] = i["verification_status"] * 100 / max_verification_status
            i["score_recency"] = (i["recency"]/86400 - 1672444800/86400) * 100 / (max_recency/86400 - 1672444800/86400)
            
            i["total_score"] = 0.25 * i["score_keyword_relevance"] + 0.25 * i["score_follower_quality"] + 0.25 * i["score_verification_status"] +  0.25 * i["score_recency"]

        return user_profiles_ext
    
    @staticmethod
    def check_favoutrite_account(username):
        return True if FavouriteAccountModel.find({
            'username': username
        }) else False
        
    @classmethod
    def get_top_score(cls, from_time=0):
        _now = dt_utcnow().timestamp()
        if from_time == 0:
            from_time = _now - 86400 * 365
        
        print('* From time = ', from_time)
        _filter = {
            'created_at': {
                '$gte': from_time
            }
        }

        _user_profiles = AccountsFilteredDetailModel.find(filter=_filter)
        print("Total: ", len(_user_profiles))
        
        account_list = cls.get_account_list()
        keywords_list = cls.get_keyword_list()
        people_keywords = cls.get_people_keywords()
        social_keywords = cls.get_social_keywords()
    
        _output = []
        max_keyword_relevance = 0
        max_follower_quality = 0
        max_verification_status = 0
        max_recency = 0

        for i in _user_profiles:
            # if i['username'] != 'settlefi':
            #     continue
            if cls.valid_description(i) and cls.is_protocol(i) and (cls.number_friendship(i, account_list) > 0 or cls.keywords_in_description(i, keywords_list) > 0) and not cls.people_keywords_in_description(i, people_keywords) and not cls.social_keywords_in_description(i, social_keywords):
                
                url = "https://twitter.com/" + i["username"]
                keywords_in_description = cls.keywords_in_description(i, keywords_list)
                number_of_friendship = cls.number_friendship(i, account_list)
                
                _item = {
                    'username': i['username'],
                    'twitter_url': url,
                    'keyword_relevance': keywords_in_description,
                    'follower_quality': number_of_friendship,
                    'verification_status': 100 if i['verified_type'] == 'gold' else (40 if i['verified_type'] == 'blue' else 10),
                    'recency': i['created_at']
                }
                _output.append(_item)
                
                if _item["keyword_relevance"] > max_keyword_relevance:
                    max_keyword_relevance = _item["keyword_relevance"]
                    
                if _item["follower_quality"] > max_follower_quality:
                    max_follower_quality = _item["follower_quality"]
                    
                if _item["verification_status"] > max_verification_status:
                    max_verification_status = _item["verification_status"]
                    
                if _item["recency"] > max_recency:
                    max_recency = _item["recency"]
                    
        # print("---- OUTPUTS = ", _output)
        # print(max_keyword_relevance,
        #     max_follower_quality,
        #     max_verification_status,
        #     max_recency)
        
        sorted_user_profiles = sorted(cls.scoring(
            _output,
            max_keyword_relevance,
            max_follower_quality,
            max_verification_status,
            max_recency
        ), key=lambda x: x['total_score'], reverse=True)
    
                    
        
        return {
            'items': sorted_user_profiles,
            'status': 'success'
        }
