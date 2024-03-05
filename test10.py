




def checkPalindrome(str):
    n = len(str)
    for i in range(n):
        if not str[i]==str[-i]:
            print("Not a PAL")
            break
        else:    
            print(f"str {str} is a palindrom")        


checkPalindrome("Maths")
checkPalindrome("malayalam")
