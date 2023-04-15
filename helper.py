def getPrice(ripeness):
    if ripeness >=0 and ripeness <= 25:
        return "Rs. 30 - 40 /kg"
    elif ripeness >= 25 and ripeness <=50:
        return "Rs. 55 - 65 /kg"
    elif ripeness >= 50 and ripeness <=75:
        return "Rs.  65 - 70 /kg"
    else:
        return "Rs 75 - 100 /kg"