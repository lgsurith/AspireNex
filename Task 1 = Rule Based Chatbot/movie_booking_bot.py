import random
import re
from datetime import datetime, timedelta


#Bot For Movie Booking
class MovieBot:
    def __init__(self):
        self.movies = {
            "Avengers: Endgame": ["Action", "Adventure"],
            "Kill Bill : Vol. 1" : ["Action"],
            "SpiderMan : No Way Home" : ["Action", "Adventure"],
            "The Dark Knight Rises": ["Action", "Thriller"],
            "Harakiri" : ["Action", "Drama"],
            "The Godfather": ["Crime", "Drama"],
            "Inception": ["Sci-Fi", "Thriller"],
            "La La Land": ["Musical", "Romance"],
            "The Shawshank Redemption": ["Drama"],
            "2001 : A Space Odyssey": ["Sci-Fi"],
            "The Matrix": ["Action", "Sci-Fi"],
            "Dune Part Two" : ["Action", "Adventure","Sci-Fi"],
            "Blade Runner 2049" : ["Action", "Sci-Fi"],
            "WHIPLASH" : ["Drama", "Music"],
            "Interstellar" : ["Sci-Fi", "Adventure"],
            "The Social Network" : ["Drama"],
        }
        self.theaters = [
            "The Castro Theatre", 
            "New Beverly Cinema" , 
            "PVR Director's Cut" , 
            "Cine Thisio" , 
            "Alamo Drafthouse" , 
            "Cine De Chef"
        ]
        self.showtimes = ["10:00 AM , 12:10 AM , 2:30 PM", "5:20 PM", "8:40 PM","10:30 PM"]
        self.booking = {}
        self.greetings = ["Hello , Welcome to MovieBot!. How can I help you ?"]
        self.farewells = ["Goodbye!", "Have a great day!", "Enjoy your movie!"]
        self.snacks = {
            "Large Popcorn" : 510 ,
            "Medium Popcorn" : 370 , 
            "Small Popcorn" : 210 ,  
            "Soda" : 100, 
            "Nachos with Salsa" : 220, 
            "Hot Dog" : 140 ,
            "Sandwhich" : 110 , 
            "Cold Coffee" : 100
        }
        self.snacks_combos = {
            "Lone Ranger ": {"items" : ["Medium Popcorn", "Soda"] , "price" : 490}, 
            "Family Pack ": {"items" : ["Large Popcorns" , " Large Popcorns" , "Soda" , "Soda" , "Soda"],"price" : 720},
            "Unlimited Combo" : {"items" : ["Large Popcorn (Refillable)" , "Large Soda (Refillable)"] , "price" : 610}
        }
        self.ticket_price = {
            "Balcony" : 210 , 
            "Gold Class" : 145 , 
            "Silver Class" : 110
        }
    
    def greet(self):
        return self.greetings[0]

    def farewell(self):
        return random.choice(self.farewells)

    #functionality for weekend 
    def is_weekend(self, date_str):
        date = datetime.strptime(date_str, "%d/%m/%Y")
        return date.weekday() >= 5
    
    #to sum up all the prices.
    def calculate_total(self):
        total = self.ticket_price[self.booking['ticket_type']] * self.booking['tickets']
        if 'snacks' in self.booking:
            total += sum(self.snacks[snack] for snack in self.booking['snacks'])
        if 'combos' in self.booking:
            total += sum(self.snacks_combos[combo]['price'] for combo in self.booking['combos'])
        return total
    
    
    def generate_ticket(self):
        total = self.calculate_total()
        ticket = f"Movie: {self.booking['movie']}\n"
        ticket += f"Theater: {self.booking['theater']}\n"
        ticket += f"Date: {self.booking['date']}\n"
        ticket += f"Showtime: {self.booking['showtime']}\n"
        ticket += f"Ticket Details : {self.booking['tickets']} {self.booking['ticket_type']} (₹{self.ticket_price[self.booking['ticket_type']] * self.booking['tickets']})\n"
        if 'snacks' in self.booking:
            ticket += "Snacks:\n"
            for snack in self.booking['snacks']:
                ticket += f"  - {snack} (₹{self.snacks[snack]})\n"
        if 'combos' in self.booking:
            ticket += "Combos:\n"
            for combo in self.booking['combos']:
                ticket += f"  - {combo} (₹{self.snacks_combos[combo]['price']})\n"
        ticket += f"Total: ₹{total}"
        return ticket
    
    def get_response(self, user_input):
        user_input = user_input.lower()

        if any(word in user_input for word in ["hello", "hi", "hey"]):
            return self.greet()

        elif "book" in user_input and "movie" in user_input and "ticket" in user_input:
            return "Great! I can help you book a movie. What genre are you interested in?"

        elif "genre" in user_input or "type of movie" in user_input:
            genres = set(genre for movie_genres in self.movies.values() for genre in movie_genres)
            return f"We have movies in the following genres: {', '.join(genres)}. Which genre would you like?"
        
        elif "snack" in user_input or "snacks" in user_input or "food" in user_input:
            snack_list = ", ".join([f"{snack} (₹{price})" for snack, price in self.snacks.items()])
            combo_list = ", ".join([f"{combo} (₹{details['price']})" for combo, details in self.snacks_combos.items()])
            return f"We have the following snacks: {snack_list}. We also have the following combos: {combo_list}. Would you like to order anything?"
        
        elif any(snack.lower() in user_input for snack in self.snacks):
            ordered_snack = next(snack for snack in self.snacks if snack.lower() in user_input)
            if 'snacks' not in self.booking:
                self.booking['snacks'] = []
            self.booking['snacks'].append(ordered_snack)
            return f"Great! I've added '{ordered_snack}' to your order. Would you like to order anything else?"

        elif any(combo.lower() in user_input for combo in self.snacks_combos):
            ordered_combo = next(combo for combo in self.snacks_combos if combo.lower() in user_input)
            if self.is_weekend(self.booking['date']) or "Unlimited Combo" in ordered_combo:
                if 'combos' not in self.booking:
                    self.booking['combos'] = []
                self.booking['combos'].append(ordered_combo)
                return f"Great! I've added the '{ordered_combo}' to your order. Would you like to order anything else?"
            else:
                return "I'm sorry, the 'Unlimited Combo' is only available on weekends. Would you like to order something else?"
        

        
        elif any(genre.lower() in user_input for genre in set(genre for movie_genres in self.movies.values() for genre in movie_genres)):
            matching_movies = [movie for movie, genres in self.movies.items() if any(genre.lower() in user_input for genre in genres)]
            if matching_movies:
                self.booking['movie'] = random.choice(matching_movies)
                return f"Great choice! How about '{self.booking['movie']}'? Would you like to book this movie?"

        elif "yes" in user_input and 'movie' in self.booking:
            return f"Excellent! Which theater would you prefer? We have: {', '.join(self.theaters)}"

        elif any(theater.lower() in user_input for theater in self.theaters):
            self.booking['theater'] = next(theater for theater in self.theaters if theater.lower() in user_input)
            return f"Good choice! What date would you like to watch the movie? (Please use DD/MM/YYYY format)"

        elif re.match(r'\d{2}/\d{2}/\d{4}', user_input):
            self.booking['date'] = user_input
            return f"Alright! Here are the available showtimes: {', '.join(self.showtimes)}. Which one do you prefer?"

        elif any(showtime.lower() in user_input for showtime in self.showtimes):
            self.booking['showtime'] = next(showtime for showtime in self.showtimes if showtime.lower() in user_input)
            return "Great! How many tickets would you like to book?"

        elif user_input.isdigit():
            self.booking['tickets'] = int(user_input)
            ticket_type = ", ".join([f"{ticket_type} (₹{price})" for ticket_type, price in self.ticket_price.items()])
            return f"Perfect! I've booked {self.booking['tickets']} tickets. Please choose your ticket type: {ticket_type}"
        
        elif any(ticket_type.lower() in user_input for ticket_type in self.ticket_price):
            self.booking['ticket_type'] = next(ticket_type for ticket_type in self.ticket_price if ticket_type.lower() in user_input)
            return f"Got it! You've booked {self.booking['tickets']} tickets in the {self.booking['ticket_type']} section. Would you like to order snacks?"

        elif "no" in user_input or "bye" in user_input or "thank" in user_input:
            return self.farewell()
        
        elif "ticket" in user_input:
            return self.generate_ticket()

        else:
            return "I'm sorry, I didn't understand that. Could you please rephrase or ask something else?"

    
    
def chat_with_bot():
    bot = MovieBot()
    print(bot.greet())

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Bot:", bot.farewell())
            break
        response = bot.get_response(user_input)
        print("Bot:", response)

if __name__ == "__main__":
    chat_with_bot()