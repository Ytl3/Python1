import random

print("Options are: Rock, Paper, Scissors")
score_user=0
score_cmpu=0

while True:
    p1 = input("Player 1, enter your choice: ").strip().lower()
    #computer = random.choice(["rock", "paper", "scissors"])
    computer=random.choice(["rock", "paper", "scissors"])
    print(f"Computer chose: {computer}")
    if p1 == computer:
        print("It's a tie!")
    elif (p1 == "rock" and computer == "scissors") or \
         (p1 == "paper" and computer == "rock") or \
         (p1 == "scissors" and computer == "paper"):
        print("Player 1 wins!")
        score_user+=1
        
    elif (computer == "rock" and p1 == "scissors") or \
         (computer == "paper" and p1 == "rock") or \
         (computer == "scissors" and p1 == "paper"):
        print("Computer wins!")
        score_cmpu+=1
        
    else:
        print("Invalid input. Please enter Rock, Paper, or Scissors.")
    if score_cmpu==3:
        print("Computer wins!!!!!!!")
    elif score_user==3:
        print("Player 1 wins!!!!!!!")
        break
    

