import re

def extract_menu_items(menu_string):
    items = []
    if menu_string:
        # 쉼표(,)로 메뉴를 분리
        menu_list = menu_string.split(',')
        for menu_item in menu_list:
            # 괄호()로 메뉴 이름과 가격을 분리
            start_index = menu_item.find('(')
            end_index = menu_item.find(')')
            if start_index != -1 and end_index != -1:
                menu_name = menu_item[:start_index].strip()  # 메뉴 이름
                menu_price_str = menu_item[start_index+1:end_index].strip()  # 메뉴 가격 문자열
                patterns = [
                    r"(\d*)만(\d*)천",
                    r"(\d+)만(\d+)천",
                    r"(\d*)천",
                    r"(\d+)천"
                ]
                index=0
                matched_value = None
                for pattern in patterns:
                    index=index+1
                    match = re.search(pattern, menu_price_str)
                    if match:
                        matched_value = match.group()
                        break

                if matched_value:
                    if(index<2):
                        total_price=int(match.group(1)) * 10000+int(match.group(2)) * 1000
                    else:
                        total_price = int(match.group(1)) * 1000

                    items.append((menu_name, total_price))
                else:
                    items.append((menu_name, 0))

    return items







