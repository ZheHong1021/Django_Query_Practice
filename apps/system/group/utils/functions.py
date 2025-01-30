# 內建 Group 添加的 Serializers
def get_profile_and_validated_data(validated_data):
    group_validated_data = {}

    # Django內建的column只有 name
    # 先確保傳遞進來的欄位有 name
    if validated_data.get("name"):
        name = validated_data.pop('name') # 透過 pop將 profile給取出並重新定義為一個變數
        group_validated_data = {"name": name}


    # 剩下的欄位就會是 profile的
    profile_data = validated_data

    return profile_data['profile'], group_validated_data