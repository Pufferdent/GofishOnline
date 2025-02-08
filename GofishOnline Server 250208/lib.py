#Diamond Heart Spade Clubs
cardArray = [["D8", "H8", "S8", "C8", "JB", "JS"],
         ["D2", "D3", "D4", "D5", "D6", "D7"],
         ["D9", "DT", "DJ", "DQ", "DK", "D1"],
         ["H2", "H3", "H4", "H5", "H6", "H7"],
         ["H9", "HT", "HJ", "HQ", "HK", "H1"],
         ["S2", "S3", "S4", "S5", "S6", "S7"],
         ["S9", "ST", "SJ", "SQ", "SK", "S1"],
         ["C2", "C3", "C4", "C5", "C6", "C7"],
         ["C9", "CT", "CJ", "CQ", "CK", "C1"]]

cards = []
for group in cardArray:
    for card in group:
        cards.append(card)


def groupID(goal):
    for group in cardArray:
        if goal in group:
            return (cardArray.index(group), group.index(goal))

