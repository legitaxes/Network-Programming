import re

txt = "Hanoror bought 5 portions of orange soil for 13.50 EUR."
print(re.findall("or", txt)) # 'or' in the string
print(re.findall('.', txt)) # any character (aka every character in the string)
print(re.findall('or.', txt)) # 'or' followed by any character (does not show reoccurance)
print(re.findall('..\.', txt)) # any two character followed by a real dot


print()
print("Hello\nWorld")
print(r"Hello\nWorld") # print literal characters (raw chaarcters)

print(re.findall(r"\w", txt)) # match ALL characters except separator characters including digits and special characters
print(re.findall(r"\W", txt)) # match ALL white spaces characters/separators

print(re.findall(r"\d", txt)) # match ALL numbers only
print(re.findall(r"\D", txt)) # match ALL except numbers

print(re.findall(r"\s", txt)) # match ALL separators only [\n, \r, \t]
print(re.findall(r"\S", txt)) # match ALL except separators 


print()
print(re.findall(r'[bcdfghjklmnpqrstvxz]', txt)) # match one character in the set
print(re.findall(r'[^aeiou]', txt)) # match ALL characters except those in the set '^' indicate negation

print(re.findall(r'[0-9a-f]', txt)) # match one character that is '0' to '9' or 'a' to 'f'
print(re.findall(r'[-]', txt)) # match '-' character in the set, if want to match '-', need to place it first

print(re.findall(r'\d+', txt)) # match ALL digits once or more times, '+' is usually used with user defined set or special character 
print(re.findall(r'\w+', txt)) # match ALL characters once or more times, will be able to find all word like character sequence

print(re.findall(r'\w*or\w*', txt)) # match all word that contains 'or'. search for zero or more word characters, followed by 'or' then follwed by zero or more word-characters


print()
print("Eager: It finds the match that starts as early as possible")
print("Greedy: It makes the match as long as possible")
print(re.findall(r'\w*\d', 'abc123def456ghi')) # match zero or more characters follow by 1 digits
print("Above example shows that regex decided to take the match that starts as early as possible and stops as late as possible")
print(re.findall(r'\w*?\d', 'abc123def456ghi')) # '?' character after '*' makes algorithm lazy instead of greedy. starts as soon as possible but ends on the first occurance


print()
mtxt = 'jox r.nohre@jth.hj.se, bjox@se, adam@example.com, jox@jox@jox.com.'
print(re.findall(r'\w+@\w+', mtxt)) # extract words that contains @
print(re.findall(r'\w+@\w+\.\w+', mtxt)) # extract emails that contains only one @ in the word
# extract emails that does not contain multiple @ in the same word
print(re.findall(r"\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b(?![^\s]*@)", mtxt))



print()

f = open("lab-deliverables\\tabla.html", encoding='utf-8')
txt = f.read()

print(re.findall(r'<td class="svtTablaTime">\s*(\d+\.\d+)\s*</td>\s*<td.*?>\s*<h4.*?>\s*Simpsons\s*</h4>', txt))
print(re.findall(r'<p class="svtXMargin-Bottom-10px">\s*(\w+)</p>', txt))