def getPrice(ripeness):
    if ripeness >=0 and ripeness <= 25:
        return "Rs. 30 - 35 /kg"
    elif ripeness >= 25 and ripeness <=50:
        return "Rs. 40 - 43 /kg"
    elif ripeness >= 50 and ripeness <=75:
        return "Rs.  53 - 60 /kg"
    else:
        return "Rs 63 - 70 /kg"